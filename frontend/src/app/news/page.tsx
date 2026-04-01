"use client";

import { useState } from "react";
import { Newspaper } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { NewsFeedItem } from "@/app/_components/news-feed-item";
import { useNews } from "@/hooks/queries/use-news";
import { useOwnCompany } from "@/hooks/queries/use-companies";

type NewsTab = "all" | "own" | "competitor";

export default function NewsPage() {
  const [tab, setTab] = useState<NewsTab>("all");
  const { data: ownCompany } = useOwnCompany();

  const newsParams = tab === "own"
    ? { is_own_company: true }
    : tab === "competitor"
      ? { is_own_company: false }
      : {};

  const { data, isLoading } = useNews({ ...newsParams, limit: 50 });

  return (
    <div className="space-y-6">
      <PageHeader title="뉴스 피드" description="수집된 경쟁사 뉴스를 확인합니다." />

      {ownCompany ? (
        <Tabs value={tab} onValueChange={(v) => setTab(v as NewsTab)}>
          <TabsList>
            <TabsTrigger value="all">전체</TabsTrigger>
            <TabsTrigger value="own">자사</TabsTrigger>
            <TabsTrigger value="competitor">경쟁사</TabsTrigger>
          </TabsList>

          <TabsContent value={tab} className="mt-4">
            <NewsContent data={data} isLoading={isLoading} />
          </TabsContent>
        </Tabs>
      ) : (
        <NewsContent data={data} isLoading={isLoading} />
      )}
    </div>
  );
}

function NewsContent({
  data,
  isLoading,
}: {
  data: { items: Parameters<typeof NewsFeedItem>[0]["article"][]; total: number } | undefined;
  isLoading: boolean;
}) {
  if (isLoading) {
    return (
      <div className="space-y-3" role="status" aria-label="뉴스 로딩 중">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-16 rounded-lg" />
        ))}
      </div>
    );
  }

  if (!data || data.items.length === 0) {
    return (
      <EmptyState
        icon={<Newspaper className="h-12 w-12" />}
        title="아직 수집된 뉴스가 없습니다"
        description="경쟁사를 등록하고 뉴스 수집을 시작해보세요."
        actionLabel="경쟁사 등록하기"
        actionHref="/admin/companies/new"
      />
    );
  }

  return (
    <div className="divide-y">
      {data.items.map((article) => (
        <NewsFeedItem key={article.id} article={article} />
      ))}
    </div>
  );
}
