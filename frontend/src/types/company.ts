export interface Company {
  id: string;
  name: string;
  founded_at: string | null;
  employee_count: number | null;
  revenue: string | null;
  website_url: string | null;
  description: string | null;
  is_own_company: boolean;
  search_keywords: string[];
  created_at: string;
  updated_at: string;
}

export interface CompanyCreate {
  name: string;
  founded_at?: string | null;
  employee_count?: number | null;
  revenue?: string | null;
  website_url?: string | null;
  description?: string | null;
  is_own_company?: boolean;
  search_keywords?: string[];
}

export interface CompanyUpdate {
  name?: string;
  founded_at?: string | null;
  employee_count?: number | null;
  revenue?: string | null;
  website_url?: string | null;
  description?: string | null;
  is_own_company?: boolean;
  search_keywords?: string[];
}
