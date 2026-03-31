import type { DashboardSummary } from "@/types/dashboard";
import { api } from "./client";

export const dashboardApi = {
  getSummary: () => api.get<DashboardSummary>("/dashboard/summary"),
};
