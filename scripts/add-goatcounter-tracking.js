#!/usr/bin/env node

/**
 * Add GoatCounter tracking to all research HTML files
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const GOATCOUNTER_SCRIPT = `    <!-- GoatCounter Analytics - Free, Privacy-Friendly -->
    <script data-goatcounter="https://elamcb.goatcounter.com/count"
            async src="//gc.zgo.at/count.js"></script>`;

function getCanonicalUrl(filePath) {
    // Convert file path to canonical URL
    // research/notebooks/file.html -> /research/notebooks/file.html
    // research/file.html -> /research/file.html
    // docs/file.html -> /docs/file.html
    
    const relativePath = path.relative(path.join(__dirname, '..'), filePath);
    const normalized = relativePath.replace(/\\/g, '/');
    return `https://elamcb.github.io/${normalized}`;
}

function addGoatCounterToFile(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Skip if already has GoatCounter
        if (content.includes('goatcounter.com/count')) {
            console.log(`⏭️  Skipping ${filePath} (already has GoatCounter)`);
            return false;
        }
        
        // Find the head tag
        const headMatch = content.match(/<head[^>]*>/i);
        if (!headMatch) {
            console.log(`⚠️  No <head> tag found in ${filePath}`);
            return false;
        }
        
        // Find where to insert (after favicon/stylesheet links, before <style> or closing </head>)
        const insertAfterPattern = /(<link[^>]*stylesheet[^>]*>[\s\n]*)/i;
        const stylePattern = /(<style[^>]*>)/i;
        
        let insertPosition = -1;
        let insertAfter = '';
        
        if (insertAfterPattern.test(content)) {
            const match = content.match(insertAfterPattern);
            insertPosition = match.index + match[0].length;
            insertAfter = match[0];
        } else if (stylePattern.test(content)) {
            const match = content.match(stylePattern);
            insertPosition = match.index;
        } else {
            // Insert before </head>
            const headEnd = content.indexOf('</head>');
            if (headEnd > 0) {
                insertPosition = headEnd;
            }
        }
        
        if (insertPosition === -1) {
            console.log(`⚠️  Could not find insertion point in ${filePath}`);
            return false;
        }
        
        // Get canonical URL
        const canonicalUrl = getCanonicalUrl(filePath);
        const canonicalLink = `    <!-- Canonical link for GoatCounter path tracking -->
    <link rel="canonical" href="${canonicalUrl}">`;
        
        // Insert GoatCounter script and canonical link
        const before = content.substring(0, insertPosition);
        const after = content.substring(insertPosition);
        
        const newContent = before + 
            GOATCOUNTER_SCRIPT + '\n\n' + 
            canonicalLink + '\n' + 
            after;
        
        fs.writeFileSync(filePath, newContent, 'utf8');
        console.log(`✅ Added GoatCounter to ${filePath}`);
        return true;
    } catch (error) {
        console.error(`❌ Error processing ${filePath}:`, error.message);
        return false;
    }
}

function processDirectory(dir) {
    const files = fs.readdirSync(dir);
    let count = 0;
    
    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        
        if (stat.isDirectory()) {
            count += processDirectory(filePath);
        } else if (file.endsWith('.html') && !file.includes('index.html')) {
            if (addGoatCounterToFile(filePath)) {
                count++;
            }
        }
    }
    
    return count;
}

// Main execution
const researchDir = path.join(__dirname, '..', 'research');
const docsDir = path.join(__dirname, '..', 'docs');

console.log('🔍 Adding GoatCounter tracking to research pages...\n');

let total = 0;

if (fs.existsSync(researchDir)) {
    console.log('📁 Processing research/ directory...');
    total += processDirectory(researchDir);
}

if (fs.existsSync(docsDir)) {
    console.log('\n📁 Processing docs/ directory...');
    total += processDirectory(docsDir);
}

console.log(`\n✨ Done! Added GoatCounter to ${total} files.`);

