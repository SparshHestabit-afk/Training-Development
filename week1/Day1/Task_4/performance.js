const fs = require('fs');
const path = require('path');

const filePath = path.join('/home/sparshagarwal/week1/day1', 'large_test_file.bin');
const logFile = path.join('/home/sparshagarwal/week1/day1', 'logs/day1-perf.json');

function getMemoryUsage() {
    const mem = process.memoryUsage();
    return {
        rss: +(mem.rss / 1024 / 1024).toFixed(2),
        heapUsed: +(mem.heapUsed / 1024 / 1024).toFixed(2),
        heapTotal: +(mem.heapTotal / 1024 / 1024).toFixed(2)
    };
}


console.log('Reading File with Buffer (fs.readFile).....');
let startTime = Date.now();

fs.readFile(filePath, (err,data) => {
	if (err) throw err;

	let endTime = Date.now();
	const bufferResult = {
        method: 'Buffer',
        sizeBytes: data.length,
        timeMs: endTime - startTime,
        memory: getMemoryUsage()
    };

    console.log('fs.readFile completed:', bufferResult);

	console.log('\n Reading File with Stream (fs.createReadStream)...');
	startTime = Date.now();

	const readStream = fs.createReadStream(filePath);
	let totalBytes = 0;

	readStream.on('data', (chunk) => {
		totalBytes += chunk.length;
	});

	readStream.on('end', () => {
		let endTime = Date.now();
		const streamResult = {
            method: 'Stream',
            sizeBytes: totalBytes,
            timeMs: endTime - startTime,
            memory: getMemoryUsage()
        };

        console.log('fs.createReadStream completed:', streamResult);
        
        const logData = { bufferResult, streamResult };

        fs.mkdirSync(path.dirname(logFile), { recursive: true });

        fs.writeFileSync(logFile, JSON.stringify(logData, null, 2));
        console.log(`Performance Benchmark results saved to: ${logFile}`);
        
	});

	readStream.on('error', (err) => {
		console.error('Stream Error: ', err);
	});
});
