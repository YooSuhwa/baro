import Link from "next/link";
import { Building2, Newspaper, Package } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SENTIMENT_CONFIG } from "@/lib/constants";
import type { CompanyCard as CompanyCardType } from "@/types/dashboard";

interface CompanyCardProps {
  company: CompanyCardType;
}

export function CompanyCard({ company }: CompanyCardProps) {
  const total = Object.values(company.sentiment_distribution).reduce((a, b) => a + b, 0);
  const dominant = total > 0
    ? (Object.entries(company.sentiment_distribution).sort(([, a], [, b]) => b - a)[0]?.[0] ?? "unknown")
    : "unknown";
  const config = SENTIMENT_CONFIG[dominant as keyof typeof SENTIMENT_CONFIG] ?? SENTIMENT_CONFIG.unknown;

  return (
    <Link href={`/companies/${company.id}`}>
      <Card className="hover:shadow-md transition-shadow cursor-pointer">
        <CardHeader className="pb-2">
          <CardTitle className="text-base flex items-center gap-2">
            <Building2 className="h-4 w-4 text-gray-400" />
            {company.name}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span className="flex items-center gap-1">
              <Newspaper className="h-3.5 w-3.5" />
              뉴스 {company.news_count}건
            </span>
            <span className="flex items-center gap-1">
              <Package className="h-3.5 w-3.5" />
              제품 {company.product_count}개
            </span>
          </div>
          {total > 0 && (
            <div className="flex items-center gap-1.5">
              <div className={`h-2 w-2 rounded-full ${config.barColor}`} />
              <span className={`text-xs ${config.color}`}>
                {config.label} {Math.round(((company.sentiment_distribution[dominant] ?? 0) / total) * 100)}%
              </span>
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}
