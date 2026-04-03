const express = require('express');
const logger = require('../utils/logger.js');
const tracing = require('../utils/tracking.js');
const security = require('../middlewares/security.js');
const userRoutes = require('../routes/user.routes.js');
const productRoutes = require('../routes/product.routes.js');
const errorMiddleware = require('../middlewares/error.middleware.js');

function createApp() {
	const app = express();

	app.use(express.json());
	app.use(express.urlencoded({ extended:true }));
	
	app.use(tracing);

	security(app);

	logger.info('Security & global middlewares loaded');

	app.use('/users', userRoutes);
	app.use('/products', productRoutes);

	logger.info('Routes mounted');
	
	app.use(errorMiddleware);

	return app;
}

module.exports = createApp;
