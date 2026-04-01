import Link from "next/link";
import { Settings, FileText, Building2, Package } from "lucide-react";

const ADMIN_NAV = [
  { href: "/admin/spec-changes", label: "스펙 변경 승인", icon: FileText },
  { href: "/admin/spec-fields", label: "비교 항목 관리", icon: Settings },
  { href: "/admin/companies/new", label: "경쟁사 등록", icon: Building2 },
  { href: "/admin/products/new", label: "제품 등록", icon: Package },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col md:flex-row gap-6">
      <aside className="md:w-56 shrink-0">
        <nav className="flex md:flex-col gap-1 overflow-x-auto md:overflow-visible pb-2 md:pb-0">
          {ADMIN_NAV.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className="flex items-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 motion-safe:transition-colors whitespace-nowrap min-h-[44px]"
            >
              <Icon className="h-4 w-4" aria-hidden="true" />
              {label}
            </Link>
          ))}
        </nav>
      </aside>
      <div className="flex-1 min-w-0">{children}</div>
    </div>
  );
}
