"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Crown, X } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { PageHeader } from "@/components/shared/page-header";
import { useCreateCompany } from "@/hooks/queries/use-companies";
import { ApiClientError } from "@/lib/api/client";
import { toast } from "sonner";

export default function NewCompanyPage() {
  return (
    <Suspense>
      <NewCompanyForm />
    </Suspense>
  );
}

function NewCompanyForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const isOwnMode = searchParams.get("own") === "true";

  const createCompany = useCreateCompany();
  const [isOwnCompany, setIsOwnCompany] = useState(isOwnMode);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [keywordInput, setKeywordInput] = useState("");

  const addKeyword = () => {
    const kw = keywordInput.trim();
    if (kw && !keywords.includes(kw)) {
      setKeywords([...keywords, kw]);
      setKeywordInput("");
    }
  };

  const removeKeyword = (kw: string) => {
    setKeywords(keywords.filter((k) => k !== kw));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = new FormData(e.currentTarget);

    try {
      await createCompany.mutateAsync({
        name: form.get("name") as string,
        founded_at: (form.get("founded_at") as string) || undefined,
        employee_count: form.get("employee_count") ? Number(form.get("employee_count")) : undefined,
        revenue: (form.get("revenue") as string) || undefined,
        website_url: (form.get("website_url") as string) || undefined,
        description: (form.get("description") as string) || undefined,
        is_own_company: isOwnCompany,
        search_keywords: keywords,
      });
      toast.success(isOwnCompany ? "자사가 등록되었습니다." : "경쟁사가 등록되었습니다.");
      router.push(isOwnCompany ? "/" : "/companies");
    } catch (err: unknown) {
      if (err instanceof ApiClientError && err.code === "OWN_COMPANY_EXISTS") {
        toast.error("이미 자사가 등록되어 있습니다.");
      } else {
        const message = err instanceof Error ? err.message : "등록에 실패했습니다.";
        toast.error(message);
      }
    }
  };

  const title = isOwnCompany ? "자사 등록" : "경쟁사 등록";

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="flex items-center gap-3">
        <Link href={isOwnMode ? "/" : "/companies"} className="text-slate-400 hover:text-slate-600 motion-safe:transition-colors">
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <PageHeader title={title} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">회사 정보</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Own company toggle */}
            <div className="flex items-center gap-3 rounded-lg border border-slate-200 px-3 py-3">
              <Checkbox
                id="is_own_company"
                checked={isOwnCompany}
                onCheckedChange={(checked) => setIsOwnCompany(checked === true)}
              />
              <label htmlFor="is_own_company" className="flex items-center gap-2 text-sm font-medium text-slate-700 cursor-pointer">
                <Crown className="h-4 w-4 text-blue-500" aria-hidden="true" />
                자사로 등록
              </label>
              <span className="text-xs text-slate-400 ml-auto">자사는 1개만 등록 가능</span>
            </div>

            <div>
              <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-1">
                회사명 <span className="text-red-500">*</span>
              </label>
              <input
                id="name"
                name="name"
                required
                className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="예: 사이냅소프트"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="founded_at" className="block text-sm font-medium text-slate-700 mb-1">설립일</label>
                <input id="founded_at" name="founded_at" type="date" className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label htmlFor="employee_count" className="block text-sm font-medium text-slate-700 mb-1">사원수</label>
                <input id="employee_count" name="employee_count" type="number" className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="80" />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="revenue" className="block text-sm font-medium text-slate-700 mb-1">매출</label>
                <input id="revenue" name="revenue" className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="127억(2023)" />
              </div>
              <div>
                <label htmlFor="website_url" className="block text-sm font-medium text-slate-700 mb-1">웹사이트</label>
                <input id="website_url" name="website_url" type="url" className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="https://www.example.com" />
              </div>
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-slate-700 mb-1">설명</label>
              <textarea id="description" name="description" rows={3} className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="회사 설명" />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">검색 키워드</label>
              <div className="flex gap-2">
                <input
                  value={keywordInput}
                  onChange={(e) => setKeywordInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addKeyword(); } }}
                  className="flex-1 rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="키워드 입력 후 Enter"
                />
                <button type="button" onClick={addKeyword} className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 motion-safe:transition-colors min-h-[44px]">
                  추가
                </button>
              </div>
              {keywords.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {keywords.map((kw) => (
                    <span key={kw} className="inline-flex items-center gap-1 rounded-md bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">
                      {kw}
                      <button type="button" onClick={() => removeKeyword(kw)} className="text-slate-400 hover:text-slate-600">
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t">
              <Link href={isOwnMode ? "/" : "/companies"} className="rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 motion-safe:transition-colors min-h-[44px] inline-flex items-center">
                취소
              </Link>
              <button
                type="submit"
                disabled={createCompany.isPending}
                className="rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 motion-safe:transition-colors min-h-[44px] disabled:opacity-50"
              >
                {createCompany.isPending ? "등록 중..." : title}
              </button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
