import type { Metadata } from "next";
import "./globals.css";

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
      <body className="antialiased">{children}</body>
    </html>
  );
}
