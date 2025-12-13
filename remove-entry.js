const fs = require('fs');

// Remove from innovations-2025-11-03.json
const data1 = JSON.parse(fs.readFileSync('research/discoveries/innovations-2025-11-03.json', 'utf8'));
data1.discoveries = data1.discoveries.filter(d => d.name !== 'chinese-dictatorship');
fs.writeFileSync('research/discoveries/innovations-2025-11-03.json', JSON.stringify(data1, null, 2));

// Remove from innovations-2025-11-03-simple.json
const data2 = JSON.parse(fs.readFileSync('research/discoveries/innovations-2025-11-03-simple.json', 'utf8'));
data2.discoveries = data2.discoveries.filter(d => d.name !== 'chinese-dictatorship');
fs.writeFileSync('research/discoveries/innovations-2025-11-03-simple.json', JSON.stringify(data2, null, 2));

console.log('Removed chinese-dictatorship entry from both JSON files');

