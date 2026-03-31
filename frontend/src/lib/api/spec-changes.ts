import type { PaginatedResponse } from "@/types/api";
import type { SpecChangeRequest } from "@/types/spec-change";
import { api } from "./client";

export const specChangesApi = {
  list: (status?: string, offset = 0, limit = 20) => {
    const params = new URLSearchParams({ offset: String(offset), limit: String(limit) });
    if (status) params.set("status", status);
    return api.get<PaginatedResponse<SpecChangeRequest>>(`/spec-changes?${params.toString()}`);
  },

  approve: (id: string) => api.put<SpecChangeRequest>(`/spec-changes/${id}/approve`),

  reject: (id: string, reason: string) =>
    api.put<SpecChangeRequest>(`/spec-changes/${id}/reject`, { reason }),
};
