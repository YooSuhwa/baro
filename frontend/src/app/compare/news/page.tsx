"use client";

import { Newspaper } from "lucide-react";
import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";

export default function CompareNewsPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="뉴스 동향 비교" description="2~4개 회사의 뉴스 동향을 비교합니다." />
      <EmptyState
        icon={<Newspaper className="h-12 w-12" />}
        title="비교할 회사를 선택해주세요"
        description="회사 목록에서 2개 이상 선택 후 비교하기를 눌러주세요."
        actionLabel="경쟁사 목록 보기"
        actionHref="/companies"
      />
    </div>
  );
}
