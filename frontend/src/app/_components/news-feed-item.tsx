import { ExternalLink } from "lucide-react";
import { SentimentBadge } from "@/components/shared/sentiment-badge";
import type { NewsArticle } from "@/types/news";

interface NewsFeedItemProps {
  article: NewsArticle;
}

function timeAgo(dateStr: string): string {
  const now = new Date();
  const date = new Date(dateStr);
  const diffMs = now.getTime() - date.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 60) return `${diffMin}분 전`;
  const diffHours = Math.floor(diffMin / 60);
  if (diffHours < 24) return `${diffHours}시간 전`;
  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays}일 전`;
}

export function NewsFeedItem({ article }: NewsFeedItemProps) {
  return (
    <div className="flex items-start gap-3 py-3 border-b last:border-0">
      <div className="pt-0.5">
        <SentimentBadge sentiment={article.sentiment} />
      </div>
      <div className="flex-1 min-w-0">
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm font-medium text-gray-900 hover:text-blue-600 line-clamp-1 flex items-center gap-1"
        >
          {article.title}
          <ExternalLink className="h-3 w-3 flex-shrink-0" />
        </a>
        {article.summary && (
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">{article.summary}</p>
        )}
        <div className="flex items-center gap-2 mt-1 text-xs text-gray-400">
          <span>{timeAgo(article.collected_at)}</span>
          <span>{article.source}</span>
        </div>
      </div>
    </div>
  );
}
