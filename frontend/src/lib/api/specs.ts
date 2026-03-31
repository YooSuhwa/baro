import type { SpecField, SpecFieldCreate, SpecFieldUpdate } from "@/types/spec";
import { api } from "./client";

export const specsApi = {
  list: () => api.get<SpecField[]>("/spec-fields"),

  create: (data: SpecFieldCreate) => api.post<SpecField>("/spec-fields", data),

  update: (id: string, data: SpecFieldUpdate) => api.put<SpecField>(`/spec-fields/${id}`, data),

  delete: (id: string) => api.delete<void>(`/spec-fields/${id}`),
};
