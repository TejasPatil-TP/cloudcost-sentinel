import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CloudCost Sentinel",
  description: "Multi-cloud FinOps Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <div className="border-b">
          <div className="flex h-16 items-center px-4">
            <div className="font-bold text-xl ml-4 text-blue-600">CloudCost Sentinel</div>
            <nav className="flex items-center space-x-4 lg:space-x-6 mx-6">
              <Link href="/" className="text-sm font-medium transition-colors hover:text-primary">Overview</Link>
              <Link href="/ingestion" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">Data Ingestion</Link>
              <Link href="/budgets" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">Budgets</Link>
              <Link href="/anomalies" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">Anomalies</Link>
            </nav>
          </div>
        </div>
        <main className="flex-1">{children}</main>
      </body>
    </html>
  );
}



