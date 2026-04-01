"use client";

import { Newspaper } from "lucide-react";
import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";

export default function NewsPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="뉴스 피드" description="수집된 경쟁사 뉴스를 확인합니다." />
      <EmptyState
        icon={<Newspaper className="h-12 w-12" />}
        title="아직 수집된 뉴스가 없습니다"
        description="경쟁사를 등록하고 뉴스 수집을 시작해보세요."
        actionLabel="경쟁사 등록하기"
        actionHref="/admin/companies/new"
      />
    </div>
  );
}
