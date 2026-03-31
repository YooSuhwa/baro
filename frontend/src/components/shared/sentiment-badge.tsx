import { SENTIMENT_CONFIG } from "@/lib/constants";
import type { Sentiment } from "@/types/news";
import { Badge } from "@/components/ui/badge";

interface SentimentBadgeProps {
  sentiment: Sentiment;
}

export function SentimentBadge({ sentiment }: SentimentBadgeProps) {
  const config = SENTIMENT_CONFIG[sentiment];
  return (
    <Badge
      variant="secondary"
      className={`${config.bgColor} ${config.color} border-0 font-medium`}
      aria-label={`감성: ${config.label}`}
    >
      {config.label}
    </Badge>
  );
}
