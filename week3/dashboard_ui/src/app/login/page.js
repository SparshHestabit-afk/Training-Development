'use client';

import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { Life_Savers } from "next/font/google";

export default function Login() {
    const handleSubmit = (e) => {
        e.preventDefault();
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="w-full max-w-md bg-white border border-gray-400 rounded-lg shadow-lg">

                <div className="px-6 py-2 border-b">
                    <h1 className="text-3xl font-bold text-center mb-3">Login / Sign Up</h1>
                </div>

                <form onSubmit={handleSubmit} className="px-6 py-6 space-y-4">

                    <label htmlFor="email" className="mr-10">Enter your email : </label>
                    <Input type="email" placeholder="Enter your email" required />

                    <label htmlFor="password" className="mr-11">Enter password : </label>
                    <Input type="password" placeholder="Enter your password" required />

                    <div className="text-sm text-gray-500">
                        <a href="#" className="text-sm text-blue-600 hover:underline">
                            Forgot your password
                        </a>
                    </div>
                    <div className="ml-28">
                        <Button type="submit" variant="primary">Sign In</Button>
                    </div>
                </form>

            </div>
        </div>
    );
}