"use client";

import { FileText } from "lucide-react";
import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";

export default function SpecChangesPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="스펙 변경 승인" description="AI가 감지한 스펙 변경 사항을 검토합니다." />
      <EmptyState
        icon={<FileText className="h-12 w-12" />}
        title="검토할 변경 사항이 없습니다"
        description="뉴스 수집 후 AI가 스펙 변경을 감지하면 여기에 표시됩니다."
      />
    </div>
  );
}
