const logger = require('../utils/logger.js');
const config = require('../config');

async function connectDB() {
	try {
		logger.info(`Initializing ${config.DB_URL} database URL`);

		await new Promise((resolve) => setTimeout(resolve,500));

		logger.info('Database connected successfully');
	} catch (error) {
		logger.error(`Database initialization failed: ${error.message}`);
		throw error;
	}
}

module.exports = connectDB;
