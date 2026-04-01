import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.domains.company.models import Company
from app.domains.company.repository import CompanyRepository
from app.domains.news.models import NewsArticle
from app.domains.news.repository import NewsRepository
from app.domains.product.repository import ProductRepository
from app.domains.spec_change.models import SpecChangeRequest
from app.domains.spec_field.repository import SpecFieldRepository
from app.integrations.llm.openai_provider import OpenAIProvider
from app.integrations.news_source.google_collector import GoogleNewsCollector
from app.integrations.news_source.interface import NewsSourceCollector
from app.integrations.news_source.naver_collector import NaverNewsCollector

logger = logging.getLogger(__name__)


def _build_collectors() -> list[NewsSourceCollector]:
    collectors: list[NewsSourceCollector] = []

    if settings.NAVER_CLIENT_ID and settings.NAVER_CLIENT_ID != "your-naver-client-id":
        collectors.append(NaverNewsCollector(settings.NAVER_CLIENT_ID, settings.NAVER_CLIENT_SECRET))

    if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "your-google-api-key":
        collectors.append(GoogleNewsCollector(settings.GOOGLE_API_KEY, settings.GOOGLE_CSE_ID))

    return collectors


def _build_llm() -> OpenAIProvider | None:
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "sk-your-key-here":
        return OpenAIProvider(settings.OPENAI_API_KEY, settings.OPENAI_MODEL)
    return None


async def run_collection_pipeline(session: AsyncSession, company_id: uuid.UUID | None = None) -> dict:
    """Run the full news collection + analysis pipeline.

    Returns a summary dict with collected/analyzed/failed counts.
    """
    company_repo = CompanyRepository(session)
    news_repo = NewsRepository(session)

    collectors = _build_collectors()
    if not collectors:
        logger.warning("No news collectors configured (check NAVER/GOOGLE API keys)")
        return {"collected": 0, "analyzed": 0, "errors": ["No news API keys configured"]}

    # Get target companies
    if company_id:
        company = await company_repo.get_by_id(company_id)
        companies = [company] if company else []
    else:
        companies_list, _ = await company_repo.list(offset=0, limit=100)
        companies = companies_list

    total_collected = 0
    total_analyzed = 0
    errors: list[str] = []

    for company in companies:
        try:
            count = await _collect_for_company(company, collectors, news_repo, session)
            total_collected += count
        except Exception as e:
            error_msg = f"Collection failed for {company.name}: {e}"
            logger.error(error_msg)
            errors.append(error_msg)

    # Analyze unanalyzed articles
    llm = _build_llm()
    if llm:
        total_analyzed = await _analyze_articles(session, llm, companies)
    else:
        logger.warning("OpenAI not configured, skipping analysis")

    await session.commit()

    result = {"collected": total_collected, "analyzed": total_analyzed, "errors": errors}
    logger.info(f"Pipeline complete: {result}")
    return result


async def _collect_for_company(
    company: Company,
    collectors: list[NewsSourceCollector],
    news_repo: NewsRepository,
    session: AsyncSession,
) -> int:
    """Collect news for a single company using all collectors."""
    collected = 0
    keywords = [kw.keyword for kw in company.keywords]

    if not keywords:
        logger.info(f"No keywords for company {company.name}, skipping")
        return 0

    for collector in collectors:
        for keyword in keywords:
            try:
                articles = await collector.search(keyword, max_results=10)
                for article in articles:
                    # Dedup by URL
                    if await news_repo.exists_by_url(article.url):
                        continue

                    news = NewsArticle(
                        company_id=company.id,
                        title=article.title,
                        content=article.content,
                        url=article.url,
                        source=article.source_name,
                        sentiment="unknown",
                        published_at=article.published_at,
                        collected_at=datetime.now(timezone.utc),
                    )
                    session.add(news)
                    collected += 1

            except Exception as e:
                logger.error(f"{collector.source_name} failed for keyword '{keyword}': {e}")

    if collected > 0:
        await session.flush()
        logger.info(f"Collected {collected} articles for {company.name}")

    return collected


async def _analyze_articles(
    session: AsyncSession,
    llm: OpenAIProvider,
    companies: list[Company],
) -> int:
    """Analyze unanalyzed articles (sentiment=unknown) with LLM."""
    news_repo = NewsRepository(session)
    product_repo = ProductRepository(session)
    spec_field_repo = SpecFieldRepository(session)

    analyzed = 0

    for company in companies:
        # Get unanalyzed articles for this company
        articles, _ = await news_repo.list_filtered(company_id=company.id, sentiment="unknown", limit=50)

        # Get product names for spec change detection
        products = await product_repo.list_by_company(company.id)
        product_names = [p.name for p in products]

        for article in articles:
            try:
                # Sentiment + summary
                result = await llm.analyze_sentiment(article.title, article.content)
                article.sentiment = result.sentiment
                article.summary = result.summary
                await session.flush()
                analyzed += 1

                # Spec change detection
                if product_names:
                    changes = await llm.detect_spec_changes(article.title, article.content, product_names)
                    for change in changes:
                        # Find matching product
                        matching_product = next((p for p in products if p.name == change.product_name), None)
                        if not matching_product:
                            continue

                        # Find or skip spec field
                        spec_fields = await spec_field_repo.list_all()
                        matching_field = next((f for f in spec_fields if f.field_name == change.field_name), None)
                        if not matching_field:
                            continue

                        spec_change = SpecChangeRequest(
                            product_id=matching_product.id,
                            spec_field_id=matching_field.id,
                            old_value=change.old_value_hint,
                            new_value=change.new_value,
                            source_url=article.url,
                            source_article_id=article.id,
                            status="pending",
                        )
                        session.add(spec_change)

            except Exception as e:
                logger.error(f"Analysis failed for article '{article.title}': {e}")

    if analyzed > 0:
        await session.flush()

    return analyzed
