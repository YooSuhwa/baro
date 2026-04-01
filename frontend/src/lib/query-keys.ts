export const queryKeys = {
  companies: {
    all: ["companies"] as const,
    lists: () => [...queryKeys.companies.all, "list"] as const,
    own: () => [...queryKeys.companies.all, "own"] as const,
    detail: (id: string) => [...queryKeys.companies.all, "detail", id] as const,
  },
  products: {
    all: ["products"] as const,
    detail: (id: string) => [...queryKeys.products.all, "detail", id] as const,
    byCompany: (companyId: string) => [...queryKeys.products.all, "company", companyId] as const,
  },
  specFields: {
    all: ["spec-fields"] as const,
  },
  comparison: {
    all: ["comparison"] as const,
    products: (ids: string[]) => [...queryKeys.comparison.all, "products", ...ids] as const,
  },
  news: {
    all: ["news"] as const,
    lists: () => [...queryKeys.news.all, "list"] as const,
    compare: (ids: string[], period: string) => [...queryKeys.news.all, "compare", ...ids, period] as const,
  },
  specChanges: {
    all: ["spec-changes"] as const,
    lists: () => [...queryKeys.specChanges.all, "list"] as const,
  },
  dashboard: {
    all: ["dashboard"] as const,
    summary: () => [...queryKeys.dashboard.all, "summary"] as const,
  },
};
