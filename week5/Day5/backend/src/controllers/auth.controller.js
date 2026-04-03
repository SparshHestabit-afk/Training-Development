import bcrypt from 'bcrypt';
import User from "../models/User.js";

export async function login( req, res) {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({
            message: "Missing Credentials"
        });
    }

    let user = await User.findOne({ username });

    if (!user) {
        const hashedPassword = await bcrypt.hash(password, 10);

        user = await User.create({
            username,
            password: hashedPassword
        });

        return res.json({
            message: "User created & logged in"
        });
    }

    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
        return res.status(400).json({
            message: "Invalid Password"
        });
    }

    res.json({ message: "Login Successful" });
}