export interface CompareProductInfo {
  id: string;
  name: string;
  company: string;
}

export interface CompareFieldValues {
  field_id: string;
  field_name: string;
  values: Record<string, string | null>;
}

export interface CompareCategory {
  name: string;
  fields: CompareFieldValues[];
}

export interface CompareResponse {
  products: CompareProductInfo[];
  categories: CompareCategory[];
}
