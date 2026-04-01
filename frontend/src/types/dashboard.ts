import type { NewsArticle } from "./news";

export interface CompanyCard {
  id: string;
  name: string;
  is_own_company: boolean;
  news_count: number;
  product_count: number;
  sentiment_distribution: Record<string, number>;
}

export interface DashboardSummary {
  own_company: CompanyCard | null;
  companies: CompanyCard[];
  recent_news: NewsArticle[];
  pending_spec_changes_count: number;
}
