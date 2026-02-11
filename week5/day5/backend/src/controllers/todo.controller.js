import Todo from "../models/Todo.js";

export async function getTodos(req, res) {
    const todos = await Todo.find().sort({ createdAt: -1 });

    res.json(todos);
}

export async function createTodo(req, res) {
    const { title } = req.body;

    if (!title ) {
        return res.status(400).json({
            message: "Missing Fields"
        });
    }

    const todo = await Todo.create({ title });

    res.status(201).json(todo);
}
