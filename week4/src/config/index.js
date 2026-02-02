const path = require('path');
const dotenv = require('dotenv');

const env = process.env.NODE_ENV || 'local';

const envMap = {
	local: '.env.local',
	dev: '.env,dev',
	prod: '.env.prod',
};

const envFile = envMap[env];

if (!envFile) {
	throw new Error(`Invalid NODE_ENV : ${env}`);
}

dotenv.config({
	path: path.resolve(process.cwd(), envFile),
})

const requireVars = ['PORT','DB_URI'];

requireVars.forEach((key) => {
	if(!process.env[key]) {
		throw new Error(`Missing required env variable ${key}`);
	}
});

module.exports = {
	env,
	PORT: process.env.PORT,
	DB_URI: process.env.DB_URI,
};
