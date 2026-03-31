export type SpecFieldCategory = "company_info" | "product_info" | "tech_spec";
export type SpecFieldType = "text" | "number" | "date" | "url";

export interface SpecField {
  id: string;
  category: SpecFieldCategory;
  field_name: string;
  field_type: SpecFieldType;
  is_template: boolean;
  sort_order: number;
}

export interface SpecFieldCreate {
  category: SpecFieldCategory;
  field_name: string;
  field_type: SpecFieldType;
  is_template?: boolean;
  sort_order?: number;
}

export interface SpecFieldUpdate {
  category?: SpecFieldCategory;
  field_name?: string;
  field_type?: SpecFieldType;
  is_template?: boolean;
  sort_order?: number;
}
