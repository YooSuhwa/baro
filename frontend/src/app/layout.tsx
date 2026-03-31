import type { Metadata } from "next";
import "./globals.css";
import { AppProviders } from "@/components/providers/app-providers";
import { TopNav } from "@/components/layout/top-nav";

export const metadata: Metadata = {
  title: "BARO - 경쟁사 모니터링 플랫폼",
  description: "경쟁사 실시간 모니터링 & 비교 플랫폼",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased bg-gray-50">
        <AppProviders>
          <TopNav />
          <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>
        </AppProviders>
      </body>
    </html>
  );
}
