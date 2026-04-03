'use client';

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createTodo } from "@/lib/api";

export default function AddTodo() {
    const [title, setTitle] = useState("");
    const [error, setError] = useState(null);
    const router = useRouter();

    async function handleSubmit(e) {
        e.preventDefault();

        try {
            await createTodo(title);
            router.push("/");
        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <div>
            <h1 className="text-2xl font-bold mb-4">
                Add To-Do 
            </h1>

            {error && <p className="text-red-500">{error}</p>}

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <input
                    type="text"
                    placeholder="Enter To-Do Title"
                    value={title}
                    onChange={ (e) => setTitle(e.target.value) }
                    required
                    className="border p-3 rounded"
                />

                <button 
                    type="submit"
                    className="bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
                > ADD </button>
                
            </form>
        </div>
    );
}