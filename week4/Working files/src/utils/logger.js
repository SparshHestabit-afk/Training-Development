const fs = require('fs');
const path = require('path');

const {createLogger, format, transports } = require('winston');

const logDir = path.join(__dirname, '../logs');
if (!fs.existsSync(logDir)) {
	fs.mkdirSync(logDir, { recursive: true });
}

const logFile = (level, message, requestId) => {
	const timestamp = new Date().toISOString();
	const line = `[${timestamp}] [${level.toUpperCase()}] ${requestId ? `[${requestId}]` : ''} ${message}\n`;
	
	fs.appendFileSync(path.join(logDir, `${level}.log`), line);
};

const baseLogger = createLogger({
	level: 'info',
	format: format.combine(
		format.timestamp(),
		format.printf(({ level, message, timestamp }) => {
			return `[${timestamp}] ${level.toUpperCase()}: ${message}`;
		})
	),
	transports: [new transports.Console()],
});

const logger = {
	info: (message, req) => {
		const requestId = req?.requestId;
		baseLogger.info(message);
		logFile('info', message, requestId);
	},
	error: (message, req) => {
		const requestId = req?.requestId;
		baseLogger.error(message);
		logFile('error', message, requestId);
	},
}
module.exports = logger;
