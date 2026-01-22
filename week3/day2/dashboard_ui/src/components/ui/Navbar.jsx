'use client';

import Input from "./Input";

export default function Navbar() {
    return (
        <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-gray-700 text-white flex items-center px-6 shadow-md">
            {/* Left Side of Navbar*/}
            <div className="flex items-center gap-6">
                <span className="font-semibold text-lg">Start Bootstrap</span>
                <button className="text-xl p-6">&#9776;</button>
            </div>

            {/* Center of Navbar */}
            <div className="ml-auto flex items-center">
                <Input type="text" placeholder="Search for......" />
                <button className="bg-blue-500 px-3 py-2 text-sm">
                    &#128269;
                </button>
                <button className="px-6 py-4">&#128100;&#128315;</button>
            </div>
        </header>
    );
}
