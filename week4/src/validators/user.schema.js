const Joi = require('joi');

exports.createUser = Joi.object({
    firstName: Joi.string().min(2).max(20).required(),
    lastName: Joi.string().min(5).max(30).required(),
    email: Joi.string().email().required(),
    password: Joi.string().min(8).required(),
    status: Joi.string().valid('active', 'inactive').default('active'),
});