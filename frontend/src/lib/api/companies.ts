import type { PaginatedResponse } from "@/types/api";
import type { Company, CompanyCreate, CompanyUpdate } from "@/types/company";
import { api } from "./client";

export const companiesApi = {
  list: (offset = 0, limit = 20) =>
    api.get<PaginatedResponse<Company>>(`/companies?offset=${offset}&limit=${limit}`),

  getOwn: () => api.get<Company | null>("/companies/own"),

  get: (id: string) => api.get<Company>(`/companies/${id}`),

  create: (data: CompanyCreate) => api.post<Company>("/companies", data),

  update: (id: string, data: CompanyUpdate) => api.put<Company>(`/companies/${id}`, data),

  delete: (id: string) => api.delete<void>(`/companies/${id}`),
};
