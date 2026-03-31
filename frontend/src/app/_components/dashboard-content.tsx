"use client";

import Link from "next/link";
import { Building2, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/shared/empty-state";
import { useDashboardSummary } from "@/hooks/queries/use-dashboard";
import { CompanyCard } from "./company-card";
import { NewsFeedItem } from "./news-feed-item";

export function DashboardContent() {
  const { data, isLoading, error } = useDashboardSummary();

  if (isLoading) return <DashboardSkeleton />;
  if (error) return <div className="text-red-500">데이터를 불러오는 중 오류가 발생했습니다.</div>;
  if (!data) return null;

  if (data.companies.length === 0) {
    return (
      <EmptyState
        icon={<Building2 className="h-12 w-12" />}
        title="모니터링할 경쟁사를 등록해보세요"
        description="등록 후 뉴스가 자동 수집됩니다."
        actionLabel="경쟁사 등록하기"
        actionHref="/admin/companies/new"
      />
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">경쟁사 현황</h2>
          <Link
            href="/admin/companies/new"
            className="inline-flex items-center gap-1 rounded-lg border px-3 py-1.5 text-sm font-medium hover:bg-gray-50 transition-colors"
          >
            <Plus className="h-4 w-4" />
            경쟁사 등록
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {data.companies.map((company) => (
            <CompanyCard key={company.id} company={company} />
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">최신 뉴스</CardTitle>
              <Link href="/news" className="text-sm text-gray-500 hover:text-gray-900">
                전체 뉴스 보기 &rarr;
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {data.recent_news.length === 0 ? (
              <p className="text-sm text-gray-500 py-4 text-center">
                아직 수집된 뉴스가 없습니다.
              </p>
            ) : (
              data.recent_news.map((article) => (
                <NewsFeedItem key={article.id} article={article} />
              ))
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">스펙 변경 승인</CardTitle>
              {data.pending_spec_changes_count > 0 && (
                <span className="inline-flex items-center justify-center h-5 w-5 rounded-full bg-orange-100 text-orange-600 text-xs font-medium">
                  {data.pending_spec_changes_count}
                </span>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {data.pending_spec_changes_count === 0 ? (
              <p className="text-sm text-gray-500 py-4 text-center">
                검토할 변경 사항이 없습니다.
              </p>
            ) : (
              <div className="space-y-2">
                <p className="text-sm text-gray-600">
                  미승인 {data.pending_spec_changes_count}건
                </p>
                <Link
                  href="/admin/spec-changes"
                  className="block w-full text-center rounded-lg border px-3 py-1.5 text-sm font-medium hover:bg-gray-50 transition-colors"
                >
                  전체 보기
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-32 rounded-lg" />
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Skeleton className="h-64 rounded-lg lg:col-span-2" />
        <Skeleton className="h-64 rounded-lg" />
      </div>
    </div>
  );
}
