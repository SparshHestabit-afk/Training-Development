const userService = require('../services/user.service');
const logger = require('../utils/logger');

class UserController {
    async createUser (req, res, next) {
        try {
            const user = await userService.createUser(req.body);

            logger.info(`User created: {user._id}`, req);

            res.status(201).json({
                success: true,
                message: 'User Created',
                data: user,
            });

        } catch (err) {
            logger.error(err.message, req);
            next(err);
        }
    }

    async getAllUsers (req, res, next) {
        try {
            const result = await userService.getAllUsers(req.query);

            if (!result) {
                return res.status(404).json({
                    success: false,
                    message: 'Failed to Fetch Users',
                });
            }

            res.json({
                success: true,
                data: result.users,
                pagination: result.pagination,
            });
            
        } catch (err) {
            logger.error(err.message, req);
            next(err);
        }
    }

    async getUser (req, res, next) {
        try{
            const user = await userService.findById(req.param.id);

            if (!user) {
                return res.status(404).json({
                    success: false,
                    message: 'User not Found',
                });
            }

            res.json({
                success: true,
                data: user,
            });

        } catch (err) {
            logger.error(err.message, req);
            next(err);
        }
    }
}

module.exports = new UserController();