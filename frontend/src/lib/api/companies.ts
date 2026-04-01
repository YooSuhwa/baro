import type { PaginatedResponse } from "@/types/api";
import type { Company, CompanyCreate, CompanyUpdate } from "@/types/company";
import { api } from "./client";

export const companiesApi = {
  list: (offset = 0, limit = 20, isOwnCompany?: boolean) => {
    const params = new URLSearchParams({ offset: String(offset), limit: String(limit) });
    if (isOwnCompany !== undefined) params.set("is_own_company", String(isOwnCompany));
    return api.get<PaginatedResponse<Company>>(`/companies?${params.toString()}`);
  },

  getOwn: () => api.get<Company | null>("/companies/own"),

  get: (id: string) => api.get<Company>(`/companies/${id}`),

  create: (data: CompanyCreate) => api.post<Company>("/companies", data),

  update: (id: string, data: CompanyUpdate) => api.put<Company>(`/companies/${id}`, data),

  delete: (id: string) => api.delete<void>(`/companies/${id}`),
};
