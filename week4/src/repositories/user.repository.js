const User = require('../models/User');

class UserRepository {
    
    async create(data) {
        return User.create(data);
    }

    async findById(id) {
        return User.findById(id);
    }

    async findPaginated({status = 'active', limit = 10, cursor}) {
        const query = { status };

        if(cursor) {
            query.createdAt = {$lt: cursor};
        }

        return User.find(query).sort({ createdAt: -1 }).limit(limit);
    }

    async update(id,data) {
        return User.findByIdAndUpdate(id,data,{ new: true });
    }

    async delete(id) {
        return User.findByIdAndDelete(id);
    }
}

module.exports = new UserRepository();