'use client';

import { useState, useEffect } from "react";
import { getTodos } from "@/lib/api";

export default function Home() {
  const [ todos, setTodos ] = useState([]);
  const [ error, setError ] = useState(null);

  useEffect( () => {
    async function fetchTodos() {
      try {
        const data = await getTodos();
        setTodos(data);
      } catch (err) {
        setError(err.message);
      }
    }
    fetchTodos();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">
        To-Do List
      </h1>

      {error && <p className="text-red-500"> {error} </p>}

      {todos.length === 0 ? (
        <p>No Todos found</p>
      ) : (
        <ul className="space-y-3">
          {todos.map( (todo) => (
            <li 
              key={todo._id || todo.id} 
              className="bg-white p-4 shadow-md rounded"
            >
              {todo.title}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}