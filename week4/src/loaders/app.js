const express = require('express');
const logger = require('../utils/logger.js');

function createApp() {
	const app = express();

	app.use(express.json());
	app.use(express.urlencoded({ extended:true }));

	logger.info('MiddleWare Loaded');

	const router = express.Router();
	let routeCount = 0;

	router.get('/health', (req,res) => {
		res.json({ status: 'OK', message: "Routes are working successfully" });
	});
	routeCount++;

	router.get('/ping', (req,res) => {
		res.json('pong');
	});
	routeCount++;

	app.use('/', router);

	logger.info(`Routes mounted: ${routeCount} endpoints`);

	return app;
}

module.exports = createApp;
