import type { CompareResponse } from "@/types/comparison";
import { api } from "./client";

export const comparisonApi = {
  compareProducts: (ids: string[]) =>
    api.get<CompareResponse>(`/products/compare?ids=${ids.join(",")}`),
};
