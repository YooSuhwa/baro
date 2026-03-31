export const SENTIMENT_CONFIG = {
  positive: { label: "긍정", color: "text-green-600", bgColor: "bg-green-100", barColor: "bg-green-500" },
  negative: { label: "부정", color: "text-red-600", bgColor: "bg-red-100", barColor: "bg-red-500" },
  neutral: { label: "중립", color: "text-yellow-600", bgColor: "bg-yellow-100", barColor: "bg-yellow-500" },
  unknown: { label: "미분류", color: "text-gray-500", bgColor: "bg-gray-100", barColor: "bg-gray-400" },
} as const;

export const CATEGORY_LABELS: Record<string, string> = {
  company_info: "회사 정보",
  product_info: "제품 정보",
  tech_spec: "기술 스펙",
};

export const PERIOD_OPTIONS = [
  { value: "1w", label: "최근 1주" },
  { value: "1m", label: "최근 1개월" },
  { value: "3m", label: "최근 3개월" },
];

export const MAX_COMPARE_PRODUCTS = 6;
export const MIN_COMPARE_PRODUCTS = 2;
export const MAX_COMPARE_COMPANIES = 4;
export const MIN_COMPARE_COMPANIES = 2;
