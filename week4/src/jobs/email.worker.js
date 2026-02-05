const connection = require('./redis.connection');
const { Worker } = require('bullmq');
const logger = require('../utils/logger');

const User = require('../models/User');
const Product = require('../models/Product');

logger.info('Email worker starting.....');

const worker = new Worker(
    'email-queue',
    async (job) => {
        
        const { userId, productId } = job.data;

        logger.info(`Processing Email Job ${job.id}`, { requestId: job.id });

        await new Promise(res => setTimeout(res, 1000));

        logger.info(
            `Email sent for job ${job.id}`,
            { requestId: job.id }
        );
    },
    { connection },
);
logger.info('Email worker started');


worker.on('completed', (job) => {
    logger.info(`Email job success: ${job.id} `,
        {
            requestId: job?.id,
        });
});

worker.on('failed', (job, err) => {
    logger.error(`Email Job failed: ${job?.id} - ${err.message}`,
        {
            requestId: job?.id,
        });
});