'use client';

import { useState } from "react";
import { loginUser } from "@/lib/api";

export default function Login() {
    const [ form, setForm ] = useState({
        username:"",
        password:"",
    });

    const [ message, setMessage ] = useState(null);
    const [ error, setError ] = useState(null);

    function handleChange(e) {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    }
    
    async function handleSubmit(e) {
        e.preventDefault();

        try {
            const data = await loginUser(form);
            setMessage(data.message || "Login Successful");
            setError(null);
        } catch (err) {
            setError(err.message);
            setMessage(null);
        }
    }

    return (
        <div className="border-gray-400 p-6">
            <h1 className="text-2xl font-bold mb-4">
                Login
            </h1>

            {message && <p className="text-green-600">{message}</p>}
            {error && <p className="text-red-500">{error}</p>}

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <label htmlFor="username">Username :</label>
                <input
                    type="text"
                    name="username"
                    placeholder="Enter your Username....."
                    value={form.username}
                    onChange={handleChange}
                    required
                    className="border p-3 rounded"
                />

                <label htmlFor="password">Password :</label>
                <input
                    type="password"
                    name="password"
                    placeholder="Enter you Password....."
                    value={form.password}
                    onChange={handleChange}
                    required
                    className="border p-3 rounded"
                />

                <button 
                    type="submit"
                    className="bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
                > Login </button>
            </form>
        </div>
    );
}