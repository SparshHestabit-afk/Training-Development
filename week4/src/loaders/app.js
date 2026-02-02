const express = require('express');
const logger = require('../utils/logger.js');
const errorMiddleware = require('../middlewares/error.middleware.js');
const productRoutes = require('../routes/product.routes.js');

function createApp() {
	const app = express();

	app.use(express.json());
	app.use(express.urlencoded({ extended:true }));

	logger.info('MiddleWare Loaded');

	app.use('/', productRoutes);

	app.use(errorMiddleware);

	return app;
}

module.exports = createApp;
