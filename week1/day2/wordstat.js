#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);

const getArg = (flag) => {
    const index = args.indexOf(flag);
    return index !== -1 ? args[index + 1] : null;
};

const filePath = getArg("--file");
const topN = parseInt(getArg("--top"), 10) || null;
const minLen = parseInt(getArg("--minLen"), 10) || 0;

if(!filePath) {
    console.error("Error: --file is required");
    process.exit(1);
}

const OUTPUT_DIR = "output";
const LOG_DIR = "logs";
const CONCURRENCY_LEVELS = [1, 4, 8];

fs.mkdirSync(OUTPUT_DIR, { recursive: true });
fs.mkdirSync(LOG_DIR, { recursive: true });

async function processChunk(fd, start, length, minLen) {
  const buffer = Buffer.alloc(length);
  await fd.read(buffer, 0, length, start);

  const text = buffer.toString("utf8");
  const words = text.split(/\W+/);

  const freq = {};
  let totalWords = 0;
  let longest = "";
  let shortest = null;

  for (const word of words) {
    if (!word || word.length < minLen) continue;

    totalWords++;
    freq[word] = (freq[word] || 0) + 1;

    if (word.length > longest.length) longest = word;
    if (!shortest || word.length < shortest.length) shortest = word;
  }

  return { totalWords, freq, longest, shortest };
}

async function runWithConcurrency(concurrency) {
  const stat = fs.statSync(filePath);
  const fileSize = stat.size;
  const chunkSize = Math.ceil(fileSize / concurrency);

  const fd = await fs.promises.open(filePath, "r");
  const tasks = [];

  const startTime = process.hrtime.bigint();

  for (let i = 0; i < concurrency; i++) {
    const start = i * chunkSize;
    const length = Math.min(chunkSize, fileSize - start);
    if (length <= 0) continue;

    tasks.push(processChunk(fd, start, length, minLen));
  }

  const results = await Promise.all(tasks);
  await fd.close();

  const endTime = process.hrtime.bigint();

  return {
    runtimeMs: Number(endTime - startTime) / 1e6,
    results,
  };
}

function mergeResults(chunks) {
  const merged = {
    totalWords: 0,
    freq: {},
    longest: "",
    shortest: null,
  };

  for (const chunk of chunks) {
    merged.totalWords += chunk.totalWords;

    for (const [word, count] of Object.entries(chunk.freq)) {
      merged.freq[word] = (merged.freq[word] || 0) + count;
    }

    if (chunk.longest.length > merged.longest.length) {
      merged.longest = chunk.longest;
    }

    if (!merged.shortest || chunk.shortest.length < merged.shortest.length) {
      merged.shortest = chunk.shortest;
    }
  }

  return merged;
}

(async () => {
  const perfSummary = {};
  let finalMerged;

  for (const concurrency of CONCURRENCY_LEVELS) {
    const { runtimeMs, results } = await runWithConcurrency(concurrency);
    perfSummary[`concurrency_${concurrency}`] = {
      runtimeMs: runtimeMs.toFixed(2),
    };

    if (concurrency === 8) {
      finalMerged = mergeResults(results);
    }
  }

  const topWords = Object.entries(finalMerged.freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN)
    .map(([word, count]) => ({ word, count }));

  const outputStats = {
    totalWords: finalMerged.totalWords,
    uniqueWords: Object.keys(finalMerged.freq).length,
    longestWord: finalMerged.longest,
    shortestWord: finalMerged.shortest,
    topRepeatedWords: topWords,
  };

  fs.writeFileSync(
    "output/stats.json",
    JSON.stringify(outputStats, null, 2)
  );

  fs.writeFileSync(
    "logs/perf-summary.json",
    JSON.stringify(perfSummary, null, 2)
  );

  console.log("Word - Performance stats completed");
})();

