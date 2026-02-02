const logger = require('../utils/logger.js');
const config = require('../config');
const mongoose = require('mongoose');
const User = require('../models/User.js');

async function connectDB() {
	try {
		logger.info(`Initializing ${config.DB_URI} database URI`);

		await new Promise((resolve) => setTimeout(resolve, 500));
		await mongoose.connect(config.DB_URI, {
			autoIndex: true,
		});
		const userCount = User.countDocuments();
		if (userCount === 0) {
			await User.create(
				{
					firstName: 'Sparsh',
					lastName: 'Agarwal',
					email: 'sparsh_agarwal@gmail.com',
					password: 'password123',
					status: 'active'
				},
				{
					firstName: 'Test',
					lastName: 'User',
					email: 'test_example@gmail.com',
					password: 'test12345',
					status: 'inactive'
				},
			);
		}

		logger.info('Database connected successfully');
	} catch (error) {
		logger.error(`Database initialization failed: ${error.message}`);
		throw error;
		process.exit(1);
	}
}

module.exports = connectDB;
