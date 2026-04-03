import express from 'express';
import cors from 'cors';
import authRoutes from './routes/auth.routes.js';
import todoRoutes from './routes/todo.routes.js';

const app = express();

app.use(cors({
    origin: 'https://week5-todo.local:8443',
    credentials: true
}));
app.use(express.json());

app.get('/health', (req, res) => {
    res.status(200).json({ status: "ok" });
})

app.use("/api", authRoutes);
app.use("/api/todos", todoRoutes);

export default app;