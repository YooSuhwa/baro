"use client";

import { use } from "react";
import Link from "next/link";
import { ArrowLeft, Pencil, Package, Newspaper } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { PageHeader } from "@/components/shared/page-header";
import { useCompany } from "@/hooks/queries/use-companies";

export default function CompanyDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { data: company, isLoading } = useCompany(id);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-48 rounded-lg" />
        <Skeleton className="h-32 rounded-lg" />
      </div>
    );
  }

  if (!company) {
    return <div className="py-16 text-center text-slate-500">회사를 찾을 수 없습니다.</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Link href="/companies" className="text-slate-400 hover:text-slate-600 motion-safe:transition-colors">
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <PageHeader
          title={company.name}
          actions={
            <Link
              href={`/admin/companies/${id}/edit`}
              className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 motion-safe:transition-colors min-h-[44px]"
            >
              <Pencil className="h-4 w-4" aria-hidden="true" />
              수정
            </Link>
          }
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">회사 정보</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
            <div>
              <dt className="text-slate-500">설립일</dt>
              <dd className="font-medium">{company.founded_at || "-"}</dd>
            </div>
            <div>
              <dt className="text-slate-500">사원수</dt>
              <dd className="font-medium">{company.employee_count ? `${company.employee_count}명` : "-"}</dd>
            </div>
            <div>
              <dt className="text-slate-500">매출</dt>
              <dd className="font-medium">{company.revenue || "-"}</dd>
            </div>
            <div>
              <dt className="text-slate-500">웹사이트</dt>
              <dd className="font-medium">
                {company.website_url ? (
                  <a href={company.website_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                    {company.website_url}
                  </a>
                ) : "-"}
              </dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-slate-500">검색 키워드</dt>
              <dd className="font-medium flex gap-2 flex-wrap mt-1">
                {company.search_keywords.length > 0
                  ? company.search_keywords.map((kw) => (
                      <span key={kw} className="inline-flex items-center rounded-md bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">
                        {kw}
                      </span>
                    ))
                  : "-"}
              </dd>
            </div>
          </dl>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Package className="h-4 w-4" aria-hidden="true" />
              소속 제품
            </CardTitle>
            <Link href={`/admin/products/new?company_id=${id}`} className="text-sm text-blue-600 hover:underline">
              + 제품 추가
            </Link>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-slate-500 text-center py-4">제품 목록은 준비 중입니다.</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Newspaper className="h-4 w-4" aria-hidden="true" />
              관련 뉴스
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-slate-500 text-center py-4">뉴스 목록은 준비 중입니다.</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
