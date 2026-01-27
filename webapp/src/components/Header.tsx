"use client";

import Link from "next/link";
import { useState } from "react";

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 bg-gradient-kale rounded-xl flex items-center justify-center shadow-sm group-hover:shadow-md transition">
              <span className="text-white font-bold text-lg">KIR</span>
            </div>
            <div className="hidden sm:block">
              <span className="font-semibold text-gray-900">Keeping It Real</span>
              <span className="text-gray-400 text-sm ml-2">Episode Finder</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            <Link
              href="/"
              className="px-4 py-2 text-gray-600 hover:text-kale hover:bg-gray-50 rounded-lg transition font-medium text-sm"
            >
              Find Episodes
            </Link>
            <Link
              href="/episodes"
              className="px-4 py-2 text-gray-600 hover:text-kale hover:bg-gray-50 rounded-lg transition font-medium text-sm"
            >
              All Episodes
            </Link>
            <Link
              href="/insights"
              className="px-4 py-2 text-gray-600 hover:text-kale hover:bg-gray-50 rounded-lg transition font-medium text-sm"
            >
              Insights
            </Link>
            <a
              href="https://www.keepingitrealpod.com"
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 px-4 py-2 bg-kale text-white rounded-lg hover:bg-kale-light transition font-medium text-sm flex items-center space-x-1"
            >
              <span>Listen</span>
              <span className="text-xs">↗</span>
            </a>
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-gray-600 hover:text-kale hover:bg-gray-50 rounded-lg transition"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100 animate-fade-in">
            <nav className="flex flex-col space-y-1">
              <Link
                href="/"
                className="px-4 py-3 text-gray-600 hover:text-kale hover:bg-gray-50 rounded-lg transition font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                Find Episodes
              </Link>
              <Link
                href="/episodes"
                className="px-4 py-3 text-gray-600 hover:text-kale hover:bg-gray-50 rounded-lg transition font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                All Episodes
              </Link>
              <Link
                href="/insights"
                className="px-4 py-3 text-gray-600 hover:text-kale hover:bg-gray-50 rounded-lg transition font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                Insights
              </Link>
              <a
                href="https://www.keepingitrealpod.com"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-3 text-kale font-medium flex items-center space-x-1"
              >
                <span>Listen to Podcast</span>
                <span className="text-xs">↗</span>
              </a>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}
