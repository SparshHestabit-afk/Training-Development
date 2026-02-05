const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const xss = require('xss-clean');
const hpp = require('hpp');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    standardHeaders: true,
    legacyHeaders: false,
});

const hasNoSQLInjection = (obj) => {
    if (!obj || typeof obj !== 'object') return false;

    return Object.keys(obj).some(key => {
        if (key.startsWith('$') || key.includes('.')) {
            return true;
        }
        if (typeof obj[key] === 'object') {
            return hasNoSQLInjection(obj[key]);
        }
        return false;
    });
};

const sanitizeNoSQL = (obj) => {
    if (!obj || typeof obj !== 'object') return;

    Object.keys(obj).forEach((key) => {

        if (key.startsWith('$') || key.includes('.')) {
            delete obj[key];
            return;
        }

        if (typeof obj[key] === 'object' && obj[key] !== null) {
            sanitizeNoSQL(obj[key]);

            if (Object.keys(obj[key]).length === 0) {
                delete obj[key];
            }
        }

        if (obj[key] === 'null') {
            obj[key] = null;
        }
    });
};

const sanitizeXSS = (obj) => {
    if (!obj || typeof obj !== 'object') return;

    for (const key in obj) {
        if (typeof obj[key] === 'string') {
            obj[key] = xss(obj[key]);
        } else if (typeof obj[key] === 'object') {
            sanitizeXSS(obj[key]);
        }
    }
};

module.exports = (app) => {

    app.use(express.json({ limit: '10kb' }));
    app.use(express.urlencoded({ extended: true, limit: '10kb' }));

    app.use((req, res, next) => {
        if (
            hasNoSQLInjection(req.query) ||
            hasNoSQLInjection(req.body) ||
            hasNoSQLInjection(req.params)
        ) {
            return res.status(400).json({
                success: false,
                message: 'Validation Failed',
                code: 'INVALID_QUERY',
            });
        }
        next();
    });

    app.use((req, res, next) => {

        sanitizeNoSQL(req.query);
        sanitizeNoSQL(req.body);
        sanitizeNoSQL(req.params);

        sanitizeXSS(req.query);
        sanitizeXSS(req.params);
        sanitizeXSS(req.query);

        next();
    });

    app.use(helmet());

    app.use(cors({
        origin: ['http://localhost:3000'],
        methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
        credentials: true,
    }));

    app.use('/products', limiter);

    app.use(hpp({
        whitelist: ['tags', 'status'],
    }));
};