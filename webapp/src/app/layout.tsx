import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
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
  title: "Keeping It Real - Episode Finder",
  description: "Find the perfect podcast episode for your real estate challenges. 700+ episodes from top producers.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-50`}
      >
        <nav className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <a href="/" className="text-xl font-bold text-gray-900">
                  Keeping It Real
                </a>
                <span className="ml-2 text-sm text-gray-500">Episode Finder</span>
              </div>
              <div className="flex items-center space-x-4">
                <a href="/problems" className="text-gray-600 hover:text-gray-900">Problems</a>
                <a href="/avatars" className="text-gray-600 hover:text-gray-900">Who You Are</a>
                <a href="/episodes" className="text-gray-600 hover:text-gray-900">All Episodes</a>
              </div>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
