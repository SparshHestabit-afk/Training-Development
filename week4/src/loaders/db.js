const logger = require('../utils/logger.js');
const config = require('../config');
const mongoose = require('mongoose');
const User = require('../models/User.js');
const Product = require('../models/Product.js');

async function connectDB() {
	try {
		logger.info(`Initializing ${config.DB_URI} database URI`);

		await new Promise((resolve) => setTimeout(resolve, 500));
		await mongoose.connect(config.DB_URI, {
			autoIndex: true,
		});

		const userCount = await User.countDocuments();
		logger.info(`User documents inside collection:${userCount}`);
		if (userCount === 0) {
			await User.create([
				{
					firstName: 'Sparsh',
					lastName: 'Agarwal',
					email: 'sparsh_agarwal@gmail.com',
					password: 'password123',
					status: 'active'
				},
				{
					firstName: 'Test',
					lastName: 'User 1',
					email: 'test_example_1@gmail.com',
					password: 'test12345_1',
					status: 'inactive'
				},
				{
					firstName: 'Test',
					lastName: 'User 2',
					email: 'test_example_2@gmail.com',
					password: 'test12345_2',
					status: 'active'
				},
				{
					firstName: 'Test',
					lastName: 'User_3',
					email: 'test_example_3@gmail.com',
					password: 'test12345_3',
					status: 'active'
				},
				{
					firstName: 'Test',
					lastName: 'User 4',
					email: 'test_example_4@gmail.com',
					password: 'test12345_4',
					status: 'inactive'
				},
			]);
		}

		const productCount = await Product.countDocuments();
		logger.info(`Product documents inside collection:${productCount}`);
		if (productCount === 0) {
			await Product.create([
				{
					name: "iPhone 17",
					description: "Apple Phone",
					price: 800,
					tags: ["Apple", "Smart-Phone"],
					status: "Active",
					deletedAt: null,
				},
				{
					name: "Samsung Galaxy",
					description: "Samsung Phone",
					price: 650,
					tags: ["Samsung", "Smart-Phone"],
					status: "Inactive",
					deletedAt: null,
				},
				{
					name: "Airbuds M2 Pro",
					description: "Apple Earphone",
					price: 500,
					tags: ["Apple", "Media", "Earphone"],
					status: "Inactive",
					deletedAt: null,
				},
				{
					name: "I-Charger",
					description: "Apple Device-Charger",
					price: 1000,
					tags: ["Apple", "Charger", "Battery", "Appliace"],
					status: "Active",
					deletedAt: null,
				},
				{
					name: "iPhone 17 Pro",
					description: "Apple Phone",
					price: 1200,
					tags: ["Apple", "Smart-Phone", "Pro-Series"],
					status: "Active",
					deletedAt: null,
				},
			]);
		}

		logger.info('Database connected successfully');

	} catch (error) {

		logger.error(`Database initialization failed: ${error.message}`);
		throw error;
		process.exit(1);
	}
}

module.exports = connectDB;
