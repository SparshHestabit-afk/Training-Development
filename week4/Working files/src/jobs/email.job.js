const { Queue } = require('bullmq');
const connection = require('./redis.connection');
const logger = require('../utils/logger');

const emailQueue = new Queue('email-queue', {
    connection,
    defaultJobOptions: {
        attempts: 3,
        backoff: {
            type: 'exponential',
            delay: 2000,
        },
        removeOnComplete: true,
        removeOnFail: false,
    },
});

const enqueueEmail = async (payload, req) => {

    const { userId, productId } = payload;
    
     const job = await emailQueue.add('send-email', { userId, productId });

    if (req) {
        logger.info(
            `Email job enqueued (jobId = ${job.id}) for userId = ${userId}`
            , req
        );
    }

    return job;
};

module.exports = {
    emailQueue,
    enqueueEmail,
};