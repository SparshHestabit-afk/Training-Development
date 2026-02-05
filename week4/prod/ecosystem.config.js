const path = require('path');

module.exports = {
    apps: [
        {
            name: 'Week4',
            script: './src/server.js',
            watch: false,
            instances: 'max',
            exec_mode: 'cluster',
            autorestart: true,
            max_memory_restart: '500M',
            env_file: './env.prod',
            out_file: path.resolve(__dirname, './src/logs/info.log'),
            error_file: path.resolve(__dirname, './src/logs/error.log'),
        },
    ],
};