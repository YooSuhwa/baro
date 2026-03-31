import { ExternalLink } from "lucide-react";
import { SentimentBadge } from "@/components/shared/sentiment-badge";
import { timeAgo } from "@/lib/utils";
import type { NewsArticle } from "@/types/news";

interface NewsFeedItemProps {
  article: NewsArticle;
}

export function NewsFeedItem({ article }: NewsFeedItemProps) {
  return (
    <article className="flex items-start gap-3 py-3 border-b last:border-0">
      <div className="pt-0.5">
        <SentimentBadge sentiment={article.sentiment} />
      </div>
      <div className="flex-1 min-w-0">
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm font-medium text-slate-900 hover:text-blue-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:rounded line-clamp-1 flex items-center gap-1 motion-safe:transition-colors"
        >
          {article.title}
          <ExternalLink className="h-3 w-3 flex-shrink-0" aria-hidden="true" />
          <span className="sr-only">(새 탭에서 열림)</span>
        </a>
        {article.summary && (
          <p className="text-xs text-slate-500 mt-0.5 line-clamp-1">{article.summary}</p>
        )}
        <div className="flex items-center gap-2 mt-1 text-xs text-slate-500">
          <time dateTime={article.collected_at}>{timeAgo(article.collected_at)}</time>
          <span aria-hidden="true">&middot;</span>
          <span>{article.source}</span>
        </div>
      </div>
    </article>
  );
}
