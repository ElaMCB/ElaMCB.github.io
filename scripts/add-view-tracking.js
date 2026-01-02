#!/usr/bin/env node

/**
 * Add view tracking script to all research HTML files
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const VIEW_TRACKING_SCRIPT = `
    <!-- View Tracking Script -->
    <script>
        (function() {
            // Track page view in localStorage
            try {
                const pagePath = window.location.pathname;
                const key = 'view_count_' + pagePath;
                const stored = localStorage.getItem(key);
                const count = stored ? parseInt(stored) : 0;
                localStorage.setItem(key, (count + 1).toString());
                
                // Also track in a global object for immediate access
                window.pageViewCount = count + 1;
            } catch (e) {
                // localStorage not available
            }
        })();
    </script>`;

function addViewTrackingToFile(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Skip if already has view tracking
        if (content.includes('view_count_') || content.includes('pageViewCount')) {
            console.log(`⏭️  Skipping ${filePath} (already has view tracking)`);
            return false;
        }
        
        // Find the closing </head> tag
        const headEnd = content.indexOf('</head>');
        if (headEnd === -1) {
            console.log(`⚠️  No </head> tag found in ${filePath}`);
            return false;
        }
        
        // Insert before </head>
        const before = content.substring(0, headEnd);
        const after = content.substring(headEnd);
        
        const newContent = before + VIEW_TRACKING_SCRIPT + '\n' + after;
        
        fs.writeFileSync(filePath, newContent, 'utf8');
        console.log(`✅ Added view tracking to ${filePath}`);
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
            if (addViewTrackingToFile(filePath)) {
                count++;
            }
        }
    }
    
    return count;
}

// Main execution
const researchDir = path.join(__dirname, '..', 'research');
const docsDir = path.join(__dirname, '..', 'docs');

console.log('🔍 Adding view tracking to research pages...\n');

let total = 0;

if (fs.existsSync(researchDir)) {
    console.log('📁 Processing research/ directory...');
    total += processDirectory(researchDir);
}

if (fs.existsSync(docsDir)) {
    console.log('\n📁 Processing docs/ directory...');
    total += processDirectory(docsDir);
}

console.log(`\n✨ Done! Added view tracking to ${total} files.`);

