import type { PaginatedResponse } from "@/types/api";
import type { NewsArticle, NewsCompareResponse } from "@/types/news";
import { api } from "./client";

export const newsApi = {
  list: (params?: { company_id?: string; sentiment?: string; period?: string; offset?: number; limit?: number }) => {
    const searchParams = new URLSearchParams();
    if (params?.company_id) searchParams.set("company_id", params.company_id);
    if (params?.sentiment) searchParams.set("sentiment", params.sentiment);
    if (params?.period) searchParams.set("period", params.period);
    searchParams.set("offset", String(params?.offset ?? 0));
    searchParams.set("limit", String(params?.limit ?? 20));
    return api.get<PaginatedResponse<NewsArticle>>(`/news?${searchParams.toString()}`);
  },

  compare: (companyIds: string[], period = "1w") =>
    api.get<NewsCompareResponse>(`/news/compare?company_ids=${companyIds.join(",")}&period=${period}`),

  triggerCollect: (companyId?: string) =>
    api.post<{ message: string }>("/news/collect", { company_id: companyId ?? null }),
};
