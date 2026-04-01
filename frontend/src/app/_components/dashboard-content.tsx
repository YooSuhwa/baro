"use client";

import Link from "next/link";
import { AlertCircle, Building2, Crown, Plus, RefreshCw } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/shared/empty-state";
import { useDashboardSummary } from "@/hooks/queries/use-dashboard";
import { CompanyCard } from "./company-card";
import { NewsFeedItem } from "./news-feed-item";

export function DashboardContent() {
  const { data, isLoading, error, refetch } = useDashboardSummary();

  if (isLoading) return <DashboardSkeleton />;

  if (error) {
    return (
      <div role="alert" className="flex flex-col items-center justify-center py-16 text-center">
        <AlertCircle className="h-10 w-10 text-red-400 mb-3" aria-hidden="true" />
        <h3 className="text-lg font-medium text-slate-900">데이터를 불러오지 못했습니다</h3>
        <p className="text-sm text-slate-500 mt-1">잠시 후 다시 시도해주세요.</p>
        <button
          onClick={() => refetch()}
          className="mt-4 inline-flex items-center gap-2 rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 motion-safe:transition-colors min-h-[44px]"
        >
          <RefreshCw className="h-4 w-4" aria-hidden="true" />
          다시 시도
        </button>
      </div>
    );
  }

  if (!data) return null;

  const hasNoData = !data.own_company && data.companies.length === 0;

  if (hasNoData) {
    return (
      <EmptyState
        icon={<Building2 className="h-12 w-12" />}
        title="BARO에 오신 것을 환영합니다"
        description="먼저 자사 정보를 등록하고, 모니터링할 경쟁사를 추가해보세요."
        actionLabel="자사 등록하기"
        actionHref="/admin/companies/new?own=true"
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Own company section */}
      {!data.own_company ? (
        <Card className="border-dashed border-blue-200 bg-blue-50/50">
          <CardContent className="flex items-center justify-between py-4">
            <div className="flex items-center gap-3">
              <Crown className="h-5 w-5 text-blue-500" aria-hidden="true" />
              <div>
                <p className="text-sm font-medium text-slate-900">자사 정보를 등록해보세요</p>
                <p className="text-xs text-slate-500">자사 뉴스를 별도로 관리할 수 있습니다.</p>
              </div>
            </div>
            <Link
              href="/admin/companies/new?own=true"
              className="inline-flex items-center rounded-lg bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 motion-safe:transition-colors min-h-[44px]"
            >
              자사 등록
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div>
          <h2 className="text-lg font-semibold leading-tight mb-3">자사</h2>
          <Link
            href={`/companies/${data.own_company.id}`}
            className="block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded-lg"
          >
            <Card className="border-blue-200 bg-blue-50/30 hover:shadow-md motion-safe:transition-shadow cursor-pointer">
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center gap-2">
                  <Crown className="h-4 w-4 text-blue-500" aria-hidden="true" />
                  {data.own_company.name}
                  <Badge variant="secondary" className="bg-blue-100 text-blue-700 border-0 text-xs">자사</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-4 text-sm text-slate-600">
                  <span>뉴스 {data.own_company.news_count}건</span>
                  <span>제품 {data.own_company.product_count}개</span>
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>
      )}

      {/* Competitor section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold leading-tight">경쟁사 현황</h2>
          <Link
            href="/admin/companies/new"
            className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 motion-safe:transition-colors min-h-[44px]"
          >
            <Plus className="h-4 w-4" aria-hidden="true" />
            경쟁사 등록
          </Link>
        </div>
        {data.companies.length === 0 ? (
          <p className="text-sm text-slate-500 py-8 text-center">등록된 경쟁사가 없습니다.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {data.companies.map((company) => (
              <CompanyCard key={company.id} company={company} />
            ))}
          </div>
        )}
      </div>

      {/* News + Spec Changes */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className="md:col-span-2 lg:col-span-2">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">최신 뉴스</CardTitle>
              <Link href="/news" className="text-sm text-slate-500 hover:text-slate-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded px-1 py-1 motion-safe:transition-colors">
                전체 뉴스 보기 &rarr;
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {data.recent_news.length === 0 ? (
              <p className="text-sm text-slate-500 py-4 text-center">아직 수집된 뉴스가 없습니다.</p>
            ) : (
              data.recent_news.map((article) => <NewsFeedItem key={article.id} article={article} />)
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">스펙 변경 승인</CardTitle>
              {data.pending_spec_changes_count > 0 && (
                <span className="inline-flex items-center justify-center h-5 min-w-[20px] px-1 rounded-full bg-orange-100 text-orange-700 text-xs font-medium" aria-label={`미승인 변경 사항 ${data.pending_spec_changes_count}건`}>
                  {data.pending_spec_changes_count}
                </span>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {data.pending_spec_changes_count === 0 ? (
              <p className="text-sm text-slate-500 py-4 text-center">검토할 변경 사항이 없습니다.</p>
            ) : (
              <div className="space-y-3">
                <p className="text-sm text-slate-600">미승인 {data.pending_spec_changes_count}건</p>
                <Link href="/admin/spec-changes" className="block w-full text-center rounded-lg border border-slate-200 px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 motion-safe:transition-colors min-h-[44px]">
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
    <div className="space-y-6" role="status" aria-label="대시보드 로딩 중">
      <Skeleton className="h-16 rounded-lg" />
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-32 rounded-lg" />
        ))}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Skeleton className="h-64 rounded-lg md:col-span-2 lg:col-span-2" />
        <Skeleton className="h-64 rounded-lg" />
      </div>
      <span className="sr-only">로딩 중...</span>
    </div>
  );
}
