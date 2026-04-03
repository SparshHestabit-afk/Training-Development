const os = require('os');
const path = require('path');

const osType = os.type();
const osRelease = os.release();
const osArch = os.arch();

const cpuCores = os.cpus().length;

const totalMemoryGB =  (os.totalmem() / (1024**3)).toFixed(2);

const upTimeSec = os.uptime();
const hours = Math.floor(upTimeSec /3600);
const minutes  = Math.floor( (upTimeSec % 3600) / 60);
const seconds = Math.floor (upTimeSec % 60);

const currentUser = os.userInfo().username;

const nodePath = process.execPath;

console.log(`OS : ${osType} ${osRelease}`);
console.log(`Architecture : ${osArch}`);
console.log(`CPU Cores : ${cpuCores}`);
console.log(`Total Memory : ${totalMemoryGB} GB`);
console.log(`System UpTime : ${hours}h ${minutes}m ${seconds}s`);
console.log(`Current Logged User : ${currentUser}`);
console.log(`Node Path : ${nodePath}`);
