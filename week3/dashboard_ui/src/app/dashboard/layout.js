'use client';

import Sidebar from "@/components/ui/Sidebar";

export default function DashboardLayout({ children }) {
    return (
        <div className="flex min-h-screen">
            <section className="flex-1 p-6">
                {children}
            </section>

        </div>
    );
}