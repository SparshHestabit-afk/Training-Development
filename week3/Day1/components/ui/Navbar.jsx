'use client';

import Link from "next/link";
import Button from "./Button";
import Input from "./Input";

export default function Navbar({ onToggleSidebar, showHamburger }) {
    return (
        <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-header text-white flex items-center px-6 shadow-md">
            {/* Left Side of Navbar*/}
            <div className="flex items-center gap-6">
                <span className="font-semibold text-lg">
                    <Link href="/">Start Bootstrap</Link>
                </span>

                { showHamburger && (
                    <Button variant="hamburger" onClick={onToggleSidebar}>&#9776;</Button>
                )}
            </div>

            {/* Center of Navbar */}
            <div className="ml-auto flex items-center">
                <Input type="text" placeholder="Search for......" />

                <Button variant="search" size="md">&#128100; &#9660;</Button>
            </div>
        </header>
    );
}
