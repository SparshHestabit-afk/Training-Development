const User = require('../models/User');

class UserService {
    //user creating logic
    async createUser(data) {
        const user = await User.create(data);
        return user;
    }

    //fetching all users logic
    async getAllUsers({ page = 1, limit = 20 }) {
        const pageNum = Math.max(Number(page), 1);
        const limitNum = Math.min(Number(limit), 50);

        const users = await User.find({}, { email: 1 })
            .limit(limitNum)
            .skip((pageNum - 1) * limitNum);

        const total = await User.countDocuments();

        return {
            users,
            pagination: {
                total,
                page: pageNum,
                limit: limitNum,
                pages: Math.ceil(total / limitNum),
            },
        };
    }

    //fetching specific user logic
    async getUserById(id) {
        return User.findById(id);
    }
}

module.exports = new UserService();