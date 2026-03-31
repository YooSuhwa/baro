import Link from "next/link";
import { BarChart3, Newspaper, GitCompareArrows, Settings } from "lucide-react";

export function TopNav() {
  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <BarChart3 className="h-5 w-5 text-blue-600" />
          <span>BARO</span>
        </Link>
        <nav className="flex items-center gap-6">
          <Link
            href="/news"
            className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <Newspaper className="h-4 w-4" />
            뉴스 피드
          </Link>
          <Link
            href="/compare/products"
            className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <GitCompareArrows className="h-4 w-4" />
            제품 비교
          </Link>
          <Link
            href="/admin/spec-changes"
            className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <Settings className="h-4 w-4" />
            관리자
          </Link>
        </nav>
      </div>
    </header>
  );
}
