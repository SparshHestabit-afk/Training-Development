const User = require('../models/User');

class UserRepository {
    
    create(data) {
        return User.create(data);
    }

    findById(id) {
        return User.findById(id);
    }

    findPaginated({status = 'active', limit = 10, cursor}) {
        const query = { status };

        if(cursor) {
            query.createdAt = {$lt: cursor};
        }

        return User.find(query).sort({ createdAt: -1 }).limit(limit);
    }

    update(id,data) {
        return User.findByIdAndUpdate(id,data,{ new: true });
    }

    delete(id) {
        return User.findByIdAndDelete(id);
    }
}

module.exports = new UserRepository();