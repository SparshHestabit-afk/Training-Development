const config = require('./config');
const logger = require('./utils/logger');
const connectDB = require('./loaders/db');
const createApp = require('./loaders/app');

async function startServer() {
	try{
		logger.info(`Environment : ${config.env}`);

		await connectDB();

		const app = createApp();

		app.listen(config.PORT, () => {
			logger.info(`Server started on PORT: ${config.PORT}`);
		});
	} catch (error) {
		logger.error(`Startup Failed : ${error.message}`);
		process.exit(1);
	}
}

startServer();
