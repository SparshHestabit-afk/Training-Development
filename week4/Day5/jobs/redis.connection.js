const IORedis = require('ioredis');

const connection = new IORedis({
    host: '127.0.0.1',
    port: 6379,
    maxRetriesPerRequest: null,
    enableReadyCheck: false,
});

connection.on('connect', () => {
    console.log('Redis Connected');
});

connection.on('error', (err) => {
    console.error('Redis error: ', err);
});

module.exports = connection;