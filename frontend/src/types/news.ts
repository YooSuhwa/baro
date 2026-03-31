export type Sentiment = "positive" | "negative" | "neutral" | "unknown";

export interface NewsArticle {
  id: string;
  company_id: string;
  title: string;
  content: string | null;
  url: string;
  source: string;
  sentiment: Sentiment;
  summary: string | null;
  tags: string[] | null;
  published_at: string | null;
  collected_at: string;
}

export interface NewsFilter {
  company_id?: string;
  sentiment?: Sentiment;
  period?: "1w" | "1m" | "3m";
}

export interface CompanyNewsComparison {
  company_id: string;
  company_name: string;
  sentiment_distribution: Record<string, number>;
  total_count: number;
  articles: NewsArticle[];
}

export interface NewsCompareResponse {
  companies: CompanyNewsComparison[];
  period: string;
}
