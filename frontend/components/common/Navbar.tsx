"use client";

import React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth";
import { useNotificationStore } from "@/store/notifications";
import { Button } from "@/components/ui/Button";

export const Navbar: React.FC = () => {
  const router = useRouter();
  const { user, isAuthenticated, logout } = useAuthStore();
  const { notifications, unreadCount } = useNotificationStore();
  const [dropdownOpen, setDropdownOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    router.push("/auth/login");
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-light bg-white shadow-sm">
      <div className="container-fluid flex-between py-4">
        <Link href="/" className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500"></div>
          <span className="font-bold text-dark">Deliveet</span>
        </Link>

        {isAuthenticated && user ? (
          <div className="flex items-center gap-4">
            <Link href="/notifications" className="relative">
              <button className="relative p-2 text-gray-600 hover:text-primary-500 transition-colors">
                <svg
                  className="h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                  />
                </svg>
                {unreadCount > 0 && (
                  <span className="absolute top-1 right-1 inline-flex items-center justify-center h-5 w-5 rounded-full bg-red-500 text-white text-xs font-bold">
                    {unreadCount}
                  </span>
                )}
              </button>
            </Link>

            <div className="relative">
              <button
                onClick={() => setDropdownOpen(!dropdownOpen)}
                className="flex items-center gap-2 rounded-lg hover:bg-gray-100 p-2 transition-colors"
              >
                <div className="h-8 w-8 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500"></div>
                <span className="hidden sm:inline text-sm font-medium text-dark">
                  {user.first_name}
                </span>
              </button>

              {dropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 rounded-lg border border-light bg-white shadow-lg">
                  <Link
                    href="/profile"
                    className="block px-4 py-2 text-sm text-dark hover:bg-gray-50 rounded-t-lg"
                  >
                    Profile
                  </Link>
                  <Link
                    href="/settings"
                    className="block px-4 py-2 text-sm text-dark hover:bg-gray-50"
                  >
                    Settings
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-b-lg"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex gap-3">
            <Button variant="outline" size="sm" onClick={() => router.push("/auth/login")}>
              Login
            </Button>
            <Button variant="primary" size="sm" onClick={() => router.push("/auth/register")}>
              Register
            </Button>
          </div>
        )}
      </div>
    </nav>
  );
};
