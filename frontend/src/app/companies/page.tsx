"use client";

import Link from "next/link";
import { Building2, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { useCompanies } from "@/hooks/queries/use-companies";

export default function CompaniesPage() {
  const { data, isLoading } = useCompanies();

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-32 rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  const companies = data?.items ?? [];

  return (
    <div className="space-y-6">
      <PageHeader
        title="경쟁사 목록"
        actions={
          <Link
            href="/admin/companies/new"
            className="inline-flex items-center gap-1.5 rounded-lg bg-blue-600 px-3 py-2.5 text-sm font-medium text-white hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 motion-safe:transition-colors min-h-[44px]"
          >
            <Plus className="h-4 w-4" aria-hidden="true" />
            경쟁사 등록
          </Link>
        }
      />

      {companies.length === 0 ? (
        <EmptyState
          icon={<Building2 className="h-12 w-12" />}
          title="등록된 경쟁사가 없습니다"
          description="모니터링할 경쟁사를 등록해보세요."
          actionLabel="경쟁사 등록하기"
          actionHref="/admin/companies/new"
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {companies.map((company) => (
            <Link key={company.id} href={`/companies/${company.id}`} className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded-lg">
              <Card className="hover:shadow-md motion-safe:transition-shadow cursor-pointer h-full">
                <CardHeader className="pb-2">
                  <CardTitle className="text-base flex items-center gap-2">
                    <Building2 className="h-4 w-4 text-slate-500" aria-hidden="true" />
                    {company.name}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm text-slate-600 space-y-1">
                    {company.revenue && <p>매출: {company.revenue}</p>}
                    {company.employee_count && <p>사원수: {company.employee_count}명</p>}
                    <p className="text-xs text-slate-400">키워드: {company.search_keywords.join(", ") || "-"}</p>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
