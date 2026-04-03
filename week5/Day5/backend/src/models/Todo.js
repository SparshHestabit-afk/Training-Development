import mongoose, { mongo } from 'mongoose';

const todoSchema = mongoose.Schema(
    {
        title: {
            type: String,
            required: true,
        }
    },
    { timestamps: true }
);

export default mongoose.model("Todo", todoSchema);