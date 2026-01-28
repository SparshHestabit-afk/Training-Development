'use client';

const USERS = [
    { id: 1, name: "John Doe", email: "john@example.com", role: "Admin", status: "Active" },
    { id: 2, name: "Jane Smith", email: "jane@example.com", role: "User", status: "Active" },
    { id: 3, name: "Robert Brown", email: "robert@example.com", role: "Moderator", status: "Inactive" },
    { id: 4, name: "Emily Davis", email: "emily@example.com", role: "User", status: "Active" },
    { id: 5, name: "Michael Lee", email: "michael@example.com", role: "User", status: "Inactive" },
    { id: 6, name: "Sarah Wilson", email: "sarah@example.com", role: "Admin", status: "Active" },
    { id: 7, name: "David Miller", email: "david@example.com", role: "User", status: "Active" },
    { id: 8, name: "Olivia Taylor", email: "olivia@example.com", role: "User", status: "Inactive" },
    { id: 9, name: "James Anderson", email: "james@example.com", role: "Moderator", status: "Inactive" },
    { id: 10, name: "Sophia Thomas", email: "sophia@example.com", role: "User", status: "Active" },
    { id: 11, name: "Daniel Jackson", email: "daniel@example.com", role: "User", status: "Active" },
    { id: 12, name: "Isabella White", email: "isabella@example.com", role: "User", status: "Inactive" },
    { id: 13, name: "Matthew Harris", email: "matthew@example.com", role: "Admin", status: "Active" },
    { id: 14, name: "Ava Martin", email: "ava@example.com", role: "User", status: "Active" },
    { id: 15, name: "Chris Thompson", email: "chris@example.com", role: "Moderator", status: "Active" },
    { id: 16, name: "Natalie Garcia", email: "natalie@example.com", role: "User", status: "Inactive" },
];
import { useState } from "react";
import Input from "./Input";

export default function UsersTable() {
    const [search, setSearch] = useState("");
    const [entries, setEntries] = useState(10);

    const filterUsers = USERS.filter(user =>
        user.name.toLowerCase().includes(search.toLowerCase()) ||
        user.email.toLowerCase().includes(search.toLowerCase())
    );

    const visibleEntries = filterUsers.slice(0, entries);

    return (
        <>
            <div className="flex justify-between">
                <div className="px-4 py-2 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div className="flex items-center gap-2">
                        <span className="text-md">Search : </span>
                        <Input
                            type="text"
                            placeholder="Search users"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                </div>
                <div className="flex flex-col md:flex-row md:items-center md:justify-center gap-2 mr-4">
                    <span>Show </span>
                    <select
                        value={entries}
                        onChange={(e) => setEntries(Number(e.target.value))}
                        className="border border-gray-400 rounded-md px-2 py-1 focus:outline-none focus:ring-2 focus: ring-blue-500">
                        <option value={100}>All</option>
                        <option value={10}>10</option>
                        <option value={20}>20</option>
                        <option value={30}>30</option>
                        <option value={40}>40</option>
                        <option value={50}>50</option>
                    </select>

                    <span> Enteries</span>
                </div>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-md border border-gray-200">
                    <thead className="bg-gray-100 text-gray-700">
                        <tr>
                            <th className="px-4 py-2 bg-slate-600 italic text-white border border-gray-300">ID</th>
                            <th className="px-4 py-2 bg-slate-600 italic text-white border border-gray-300">Name</th>
                            <th className="px-4 py-2 bg-slate-600 italic text-white border border-gray-300">Email</th>
                            <th className="px-4 py-2 bg-slate-600 italic text-white border border-gray-300">Role</th>
                            <th className="px-4 py-2 bg-slate-600 italic text-white border border-gray-300">Status</th>
                        </tr>
                    </thead>

                    <tbody>
                        {visibleEntries.map((user) => (
                            <tr
                                key={user.id}
                                className="hover:bg-gray-50 transition"
                            >

                                <td className="px-4 py-2 text-center border border-gray-600">{user.id}</td>
                                <td className="px-4 py-2 text-center border border-gray-600 font-medium">{user.name}</td>
                                <td className="px-4 py-2 text-center border border-gray-600">{user.email}</td>
                                <td className="px-4 py-2 text-center border border-gray-600">{user.role}</td>
                                <td className="px-4 py-2 border border-gray-600">
                                    <span
                                        className={`px-2 py-1 rounded text-sm font-medium 
                                    ${user.status === "Active" ? " ml-20 bg-green-500 text-green-700"
                                                : "ml-20 bg-red-500 text-red-700"}`}
                                    ></span><span className="ml-4 italic">{user.status}</span>
                                </td>
                            </tr>
                        ))}

                        {filterUsers.length === 0 && (
                            <tr>
                                <td colSpan="6" className="px-4 py-6 text-center text-gray-500">
                                    No Users Found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

        </>
    );
}