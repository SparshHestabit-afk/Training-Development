const Joi = require('joi');

const validate = (schema, property = 'body') => {
    return (req, res, next) => {
        
        if (!req[property]) {
            return res.status(400).json({
                success: false,
                message: 'Invalid request payload',
                code: 'VALIDATION_ERROR',
            });
        }
        
        const {error, value} = schema.validate(req[property], {
            abortEarly: false,
            stripUnknown: true,
            allowUnknown: false,
            convert: true,
        });

        if (error) {
            return res.status(400).json({
                success: false,
                message: "Validation Failed",
                code: "VALIDATION_ERROR",
                errors: error.details.map(e => e.message),
            });
        }

        req[property] = value;
        next();
    };
};

module.exports = validate;