"use client";

import { Settings } from "lucide-react";
import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";

export default function SpecFieldsPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="비교 항목 관리" description="제품 비교에 사용할 항목을 관리합니다." />
      <EmptyState
        icon={<Settings className="h-12 w-12" />}
        title="등록된 비교 항목이 없습니다"
        description="비교 항목을 추가하면 제품 비교표에서 사용할 수 있습니다."
      />
    </div>
  );
}
