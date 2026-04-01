"use client";

import { Suspense, useState, useEffect } from "react";
import { use } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Crown, X, Trash2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Skeleton } from "@/components/ui/skeleton";
import { PageHeader } from "@/components/shared/page-header";
import { useCompany, useUpdateCompany, useDeleteCompany } from "@/hooks/queries/use-companies";
import { ApiClientError } from "@/lib/api/client";
import { toast } from "sonner";

export default function EditCompanyPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  return (
    <Suspense fallback={<EditSkeleton />}>
      <EditCompanyForm companyId={id} />
    </Suspense>
  );
}

function EditCompanyForm({ companyId }: { companyId: string }) {
  const router = useRouter();
  const { data: company, isLoading } = useCompany(companyId);
  const updateCompany = useUpdateCompany(companyId);
  const deleteCompany = useDeleteCompany();

  const [isOwnCompany, setIsOwnCompany] = useState(false);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [keywordInput, setKeywordInput] = useState("");
  const [confirmDelete, setConfirmDelete] = useState(false);

  useEffect(() => {
    if (company) {
      setIsOwnCompany(company.is_own_company);
      setKeywords(company.search_keywords);
    }
  }, [company]);

  if (isLoading) return <EditSkeleton />;
  if (!company) return <div className="py-16 text-center text-slate-500">회사를 찾을 수 없습니다.</div>;

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
      await updateCompany.mutateAsync({
        name: form.get("name") as string,
        founded_at: (form.get("founded_at") as string) || undefined,
        employee_count: form.get("employee_count") ? Number(form.get("employee_count")) : undefined,
        revenue: (form.get("revenue") as string) || undefined,
        website_url: (form.get("website_url") as string) || undefined,
        description: (form.get("description") as string) || undefined,
        is_own_company: isOwnCompany,
        search_keywords: keywords,
      });
      toast.success("회사 정보가 수정되었습니다.");
      router.push(`/companies/${companyId}`);
    } catch (err: unknown) {
      if (err instanceof ApiClientError && err.code === "OWN_COMPANY_EXISTS") {
        toast.error("이미 자사가 등록되어 있습니다.");
      } else if (err instanceof ApiClientError && err.code === "DUPLICATE_COMPANY") {
        toast.error("이미 등록된 회사명입니다.");
      } else {
        const message = err instanceof Error ? err.message : "수정에 실패했습니다.";
        toast.error(message);
      }
    }
  };

  const handleDelete = async () => {
    try {
      await deleteCompany.mutateAsync(companyId);
      toast.success("회사가 삭제되었습니다.");
      router.push("/companies");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "삭제에 실패했습니다.";
      toast.error(message);
    }
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="flex items-center gap-3">
        <Link href={`/companies/${companyId}`} className="text-slate-400 hover:text-slate-600 motion-safe:transition-colors">
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <PageHeader title={`${company.name} 수정`} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">회사 정보</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
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
                defaultValue={company.name}
                className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="founded_at" className="block text-sm font-medium text-slate-700 mb-1">설립일</label>
                <input id="founded_at" name="founded_at" type="date" defaultValue={company.founded_at ?? ""} className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label htmlFor="employee_count" className="block text-sm font-medium text-slate-700 mb-1">사원수</label>
                <input id="employee_count" name="employee_count" type="number" defaultValue={company.employee_count ?? ""} className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="revenue" className="block text-sm font-medium text-slate-700 mb-1">매출</label>
                <input id="revenue" name="revenue" defaultValue={company.revenue ?? ""} className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label htmlFor="website_url" className="block text-sm font-medium text-slate-700 mb-1">웹사이트</label>
                <input id="website_url" name="website_url" type="url" defaultValue={company.website_url ?? ""} className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-slate-700 mb-1">설명</label>
              <textarea id="description" name="description" rows={3} defaultValue={company.description ?? ""} className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
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

            <div className="flex items-center justify-between pt-4 border-t">
              {!confirmDelete ? (
                <button
                  type="button"
                  onClick={() => setConfirmDelete(true)}
                  className="inline-flex items-center gap-1.5 rounded-lg px-3 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50 motion-safe:transition-colors min-h-[44px]"
                >
                  <Trash2 className="h-4 w-4" aria-hidden="true" />
                  삭제
                </button>
              ) : (
                <div className="flex items-center gap-2">
                  <span className="text-sm text-red-600">정말 삭제하시겠습니까?</span>
                  <button
                    type="button"
                    onClick={handleDelete}
                    disabled={deleteCompany.isPending}
                    className="rounded-lg bg-red-600 px-3 py-2 text-sm font-medium text-white hover:bg-red-700 motion-safe:transition-colors min-h-[44px] disabled:opacity-50"
                  >
                    {deleteCompany.isPending ? "삭제 중..." : "확인"}
                  </button>
                  <button
                    type="button"
                    onClick={() => setConfirmDelete(false)}
                    className="rounded-lg border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 motion-safe:transition-colors min-h-[44px]"
                  >
                    취소
                  </button>
                </div>
              )}

              <div className="flex gap-3">
                <Link href={`/companies/${companyId}`} className="rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 motion-safe:transition-colors min-h-[44px] inline-flex items-center">
                  취소
                </Link>
                <button
                  type="submit"
                  disabled={updateCompany.isPending}
                  className="rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 motion-safe:transition-colors min-h-[44px] disabled:opacity-50"
                >
                  {updateCompany.isPending ? "저장 중..." : "저장"}
                </button>
              </div>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

function EditSkeleton() {
  return (
    <div className="space-y-6 max-w-2xl" role="status" aria-label="로딩 중">
      <Skeleton className="h-8 w-48" />
      <Skeleton className="h-96 rounded-lg" />
    </div>
  );
}
