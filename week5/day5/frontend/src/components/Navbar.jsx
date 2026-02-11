'use client';

import Link from "next/link";

export default function Navbar() {
    return (
        <nav className="bg-white shadow-md p-4 flex gap-6">
            <Link
                href="/"
                className="text-blue-600 hover: underline"
            > Home </Link>
            <Link
                href="/add"
                className="text-blue-600 hover: underline"
            > Add To - Do </Link>
            <Link
                href="/login"
                className="text-blue-600 hover: underline"
            > Login </Link>
        </nav>
    );
}