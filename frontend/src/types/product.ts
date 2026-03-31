export interface SpecValue {
  id: string;
  spec_field_id: string;
  value: string | null;
}

export interface Product {
  id: string;
  company_id: string;
  name: string;
  released_at: string | null;
  concept: string | null;
  definition: string | null;
  spec_values: SpecValue[];
  created_at: string;
  updated_at: string;
}

export interface ProductCreate {
  company_id: string;
  name: string;
  released_at?: string | null;
  concept?: string | null;
  definition?: string | null;
}

export interface ProductUpdate {
  name?: string;
  released_at?: string | null;
  concept?: string | null;
  definition?: string | null;
}

export interface BulkSpecUpdate {
  specs: { spec_field_id: string; value: string | null }[];
}
