export interface ApiError {
  error: string;
  message: string;
  details: Record<string, unknown>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  offset: number;
  limit: number;
}
