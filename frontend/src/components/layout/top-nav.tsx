"use client";

import { useState } from "react";
import Link from "next/link";
import { BarChart3, Newspaper, GitCompareArrows, Settings, Menu, X } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger, SheetTitle } from "@/components/ui/sheet";

const NAV_ITEMS = [
  { href: "/news", label: "뉴스 피드", icon: Newspaper },
  { href: "/compare/products", label: "제품 비교", icon: GitCompareArrows },
  { href: "/admin/spec-changes", label: "관리자", icon: Settings },
] as const;

export function TopNav() {
  const [open, setOpen] = useState(false);

  return (
    <header className="border-b bg-white sticky top-0 z-40">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4">
        <Link
          href="/"
          className="flex items-center gap-2 font-bold text-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded"
          aria-label="BARO 홈"
        >
          <BarChart3 className="h-5 w-5 text-blue-600" aria-hidden="true" />
          <span>BARO</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-6" aria-label="메인 메뉴">
          {NAV_ITEMS.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className="flex items-center gap-1.5 text-sm text-slate-600 hover:text-slate-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded px-1 py-1 motion-safe:transition-colors"
            >
              <Icon className="h-4 w-4" aria-hidden="true" />
              {label}
            </Link>
          ))}
        </nav>

        {/* Mobile nav */}
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger
            className="md:hidden inline-flex items-center justify-center min-h-[44px] min-w-[44px] rounded-lg hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 motion-safe:transition-colors"
            aria-label="메뉴 열기"
          >
            <Menu className="h-5 w-5" aria-hidden="true" />
          </SheetTrigger>
          <SheetContent side="right" className="w-64">
            <SheetTitle className="text-lg font-bold mb-6">메뉴</SheetTitle>
            <nav className="flex flex-col gap-1" aria-label="모바일 메뉴">
              {NAV_ITEMS.map(({ href, label, icon: Icon }) => (
                <Link
                  key={href}
                  href={href}
                  onClick={() => setOpen(false)}
                  className="flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium text-slate-700 hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 motion-safe:transition-colors"
                >
                  <Icon className="h-5 w-5" aria-hidden="true" />
                  {label}
                </Link>
              ))}
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
