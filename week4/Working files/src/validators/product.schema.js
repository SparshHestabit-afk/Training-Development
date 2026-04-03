const Joi = require('joi');

exports.createProduct = Joi.object({
    name: Joi.string().min(5).max(30).required(),
    description: Joi.string().min(10).max(50).required(),
    price: Joi.number().positive().required(),
    tags: Joi.array().items(Joi.string()).min(1).required(),
    status: Joi.string().valid('Active', 'Inactive').default('Active'),
});

exports.getProducts = Joi.object({
    search: Joi.string().trim().min(1).optional(),
    minPrice: Joi.number().min(0),
    maxPrice: Joi.number().min(0),
    tags: Joi.alternatives().try(
        Joi.string().pattern(/^[a-zA-Z0-9,\s-]+$/),
        Joi.array().items(Joi.string())
    ).optional(),
    status: Joi.alternatives().try(
        Joi.string().valid('Active, Inactive'),
        Joi.array().items(Joi.string().valid('Active', 'Inactive')) ,
    ),
    ratings: Joi.number(),
    sort: Joi.string().pattern(/^[a-zA-Z]+:(asc|desc)$/).optional(),
    page: Joi.number().min(1),
    limit: Joi.number().min(1).max(25),
    includeDeleted: Joi.boolean().truthy('true').falsy('false').default(false),
}).unknown(false);