'use client';

import Card from "@/components/ui/Card";
import UsersTable from "@/components/ui/UsersTable";
import { useState } from "react";

export default function Users() {
    const [search, setSearch] = useState("");

    return (
        <div className="space-y-6">

            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold">Users</h1>
            </div>

            <Card title="Users List" variant="table">
                <UsersTable search={search} />
            </Card>
        </div>
    );
}