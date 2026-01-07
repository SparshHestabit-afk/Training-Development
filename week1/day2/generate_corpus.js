const fs = require('fs');
const path = require('path');

const filePath = path.join('/home/sparshagarwal/Training-Development/week1/day2','corpus.txt');

const lorem = "lorem ipsum dolor sit amet, consectetur adipscing elit";
const targetWordCount = 200000;
let word = [];

while(word.length < targetWordCount) {
	word.push(...lorem.split(' '));
}

let text = word.slice(0, targetWordCount).join(' ');
fs.writeFileSync(filePath, text, 'utf8');

console.log(`Generated Corpus.txt with ${targetWordCount} words`);
