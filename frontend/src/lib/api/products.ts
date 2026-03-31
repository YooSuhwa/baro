import type { Product, ProductCreate, ProductUpdate, BulkSpecUpdate } from "@/types/product";
import { api } from "./client";

export const productsApi = {
  get: (id: string) => api.get<Product>(`/products/${id}`),

  create: (data: ProductCreate) => api.post<Product>("/products", data),

  update: (id: string, data: ProductUpdate) => api.put<Product>(`/products/${id}`, data),

  delete: (id: string) => api.delete<void>(`/products/${id}`),

  listByCompany: (companyId: string) => api.get<Product[]>(`/companies/${companyId}/products`),

  updateSpecs: (id: string, data: BulkSpecUpdate) => api.put<Product>(`/products/${id}/specs`, data),
};
