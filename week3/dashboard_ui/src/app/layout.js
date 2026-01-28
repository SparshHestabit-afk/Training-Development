'use client';

import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

import { useState } from "react";
import { usePathname } from "next/navigation";
import Navbar from "@/components/ui/Navbar";
import Sidebar from "@/components/ui/Sidebar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({ children }) {
  const pathName = usePathname();
  const showSidebar = pathName.startsWith("/dashboard") || pathName === "/about" || pathName === "/login";

  const [isSidebarOpen, setIsSidebarOpen] = useState(() => {
    if (pathName.startsWith("/dashboard")) return true;
    if (pathName === "about") return false;
    return true;
  });

  return (
    <html lang="en">
      <body>

        <Navbar
          showHamburger={showSidebar}
          onToggleSidebar={() => setIsSidebarOpen(prev => !prev)}
        />

        {showSidebar && (
          <Sidebar isOpen={isSidebarOpen} />
        )}

        <main className={`pt-16 transition-all duration-300 bg-gray-100 
          ${showSidebar && isSidebarOpen ? "ml-64" : "ml-0"}`}>
          {children}
        </main>

      </body>
    </html>
  );
}
