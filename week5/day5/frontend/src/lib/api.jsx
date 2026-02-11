// const API_URL = process.env.NEXT_PUBLIC_API_URL;
const BASE_URL = '/api';

export async function getTodos() {
    const res = await fetch(`${BASE_URL}/todos`);

    if(!res.ok) {
        throw new Error("Failed to fetch todos");
    }

    return res.json();
}

export async function createTodo(title) {
    const res = await fetch(`${BASE_URL}/todos`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ title }),
    });

    if(!res.ok) {
        throw new Error("Failed to create todo");
    }

    return res.json();
}

export async function loginUser(data) {
    const res = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify( data ),
    });

    if (!res.ok) {
        throw new Error("Login Failed");
    }

    return res.json();
}