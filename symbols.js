const fs = require('fs');
const path = require('path');

// Specify the folder containing the JSON files
const folderPath = path.join(__dirname, 'finall'); // Adjust 'finall' to your folder name

function getSymbolsFromFolder(folder) {
    try {
        // Read all files in the folder
        const files = fs.readdirSync(folder);

        // Filter files to only include .json files and extract symbols (filenames without extensions)
        const symbols = files
            .filter(file => path.extname(file) === '.json') // Only .json files
            .map(file => path.basename(file, '.json')); // Remove the extension to get the symbol name

        return symbols;
    } catch (error) {
        console.error('Error reading folder:', error);
        return [];
    }
}

// Get symbols
const symbols = getSymbolsFromFolder(folderPath);

// Log the symbols
console.log('Symbols:', symbols.length);

// Save symbols to a JSON file
const outputFilePath = path.join(__dirname, 'symbols.json'); // File to save the symbols

// Write the symbols array to the JSON file
fs.writeFileSync(outputFilePath, JSON.stringify(symbols, null, 2), 'utf8');
console.log(`Symbols saved to ${outputFilePath}`);
