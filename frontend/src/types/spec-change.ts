export type SpecChangeStatus = "pending" | "approved" | "rejected";

export interface SpecChangeRequest {
  id: string;
  product_id: string;
  spec_field_id: string;
  old_value: string | null;
  new_value: string;
  source_url: string;
  source_article_id: string | null;
  status: SpecChangeStatus;
  reject_reason: string | null;
  created_at: string;
  reviewed_at: string | null;
}

export interface RejectRequest {
  reason: string;
}
