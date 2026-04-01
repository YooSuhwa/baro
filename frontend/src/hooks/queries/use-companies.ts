"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { companiesApi } from "@/lib/api/companies";
import { queryKeys } from "@/lib/query-keys";
import type { CompanyCreate, CompanyUpdate } from "@/types/company";

export function useCompanies(offset = 0, limit = 20) {
  return useQuery({
    queryKey: [...queryKeys.companies.lists(), offset, limit],
    queryFn: () => companiesApi.list(offset, limit),
  });
}

export function useOwnCompany() {
  return useQuery({
    queryKey: queryKeys.companies.own(),
    queryFn: companiesApi.getOwn,
  });
}

export function useCompany(id: string) {
  return useQuery({
    queryKey: queryKeys.companies.detail(id),
    queryFn: () => companiesApi.get(id),
    enabled: !!id,
  });
}

export function useCreateCompany() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CompanyCreate) => companiesApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.companies.all });
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard.all });
    },
  });
}

export function useUpdateCompany(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CompanyUpdate) => companiesApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.companies.all });
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard.all });
    },
  });
}

export function useDeleteCompany() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => companiesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.companies.all });
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard.all });
    },
  });
}
