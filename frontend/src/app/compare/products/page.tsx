"use client";

import { GitCompareArrows } from "lucide-react";
import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";

export default function CompareProductsPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="제품 스펙 비교" description="2~6개 제품을 선택하여 스펙을 비교합니다." />
      <EmptyState
        icon={<GitCompareArrows className="h-12 w-12" />}
        title="비교할 제품을 선택해주세요"
        description="제품 목록에서 2개 이상 선택 후 비교하기를 눌러주세요."
        actionLabel="경쟁사 목록 보기"
        actionHref="/companies"
      />
    </div>
  );
}
