"use client";

import { useQuery } from "@tanstack/react-query";
import { newsApi } from "@/lib/api/news";
import { queryKeys } from "@/lib/query-keys";

interface NewsParams {
  company_id?: string;
  sentiment?: string;
  period?: string;
  is_own_company?: boolean;
  offset?: number;
  limit?: number;
}

export function useNews(params?: NewsParams) {
  return useQuery({
    queryKey: [...queryKeys.news.lists(), params],
    queryFn: () => newsApi.list(params),
  });
}
