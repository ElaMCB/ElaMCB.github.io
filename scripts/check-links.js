#!/usr/bin/env node

/**
 * Simple link checker for markdown files
 * Run with: node scripts/check-links.js
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// Colors for console output
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    reset: '\x1b[0m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

// Extract markdown links from content
function extractLinks(content) {
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    const links = [];
    let match;
    
    while ((match = linkRegex.exec(content)) !== null) {
        const [fullMatch, text, url] = match;
        links.push({ text, url, fullMatch });
    }
    
    return links;
}

// Check if a URL is accessible
function checkUrl(url) {
    return new Promise((resolve) => {
        // Skip relative links and anchors
        if (url.startsWith('#') || url.startsWith('./') || url.startsWith('../') || !url.startsWith('http')) {
            resolve({ url, status: 'skipped', reason: 'relative or anchor link' });
            return;
        }

        const client = url.startsWith('https') ? https : http;
        const timeout = 10000; // 10 seconds

        const req = client.get(url, { timeout }, (res) => {
            if (res.statusCode >= 200 && res.statusCode < 400) {
                resolve({ url, status: 'ok', statusCode: res.statusCode });
            } else {
                resolve({ url, status: 'error', statusCode: res.statusCode });
            }
        });

        req.on('error', (error) => {
            resolve({ url, status: 'error', error: error.message });
        });

        req.on('timeout', () => {
            req.destroy();
            resolve({ url, status: 'timeout' });
        });
    });
}

// Find all markdown files recursively
function findMarkdownFiles(dir, files = []) {
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
            findMarkdownFiles(fullPath, files);
        } else if (item.endsWith('.md')) {
            files.push(fullPath);
        }
    }
    
    return files;
}

// Main function
async function checkLinks() {
    log('🔍 Starting link check...', 'blue');
    
    const markdownFiles = findMarkdownFiles('.');
    log(`Found ${markdownFiles.length} markdown files`, 'blue');
    
    const allLinks = [];
    const linksByFile = {};
    
    // Extract links from all files
    for (const file of markdownFiles) {
        try {
            const content = fs.readFileSync(file, 'utf-8');
            const links = extractLinks(content);
            
            if (links.length > 0) {
                linksByFile[file] = links;
                allLinks.push(...links.map(link => ({ ...link, file })));
            }
        } catch (error) {
            log(`❌ Error reading ${file}: ${error.message}`, 'red');
        }
    }
    
    log(`Found ${allLinks.length} total links`, 'blue');
    
    // Check unique URLs
    const uniqueUrls = [...new Set(allLinks.map(link => link.url))];
    const urlResults = {};
    
    log('\n🌐 Checking URLs...', 'blue');
    
    for (const url of uniqueUrls) {
        process.stdout.write(`Checking: ${url.substring(0, 60)}${url.length > 60 ? '...' : ''} `);
        
        const result = await checkUrl(url);
        urlResults[url] = result;
        
        if (result.status === 'ok') {
            log('✅', 'green');
        } else if (result.status === 'skipped') {
            log('⏭️ (skipped)', 'yellow');
        } else if (result.status === 'timeout') {
            log('⏰ (timeout)', 'yellow');
        } else {
            log(`❌ (${result.statusCode || result.error})`, 'red');
        }
    }
    
    // Report results
    log('\n📊 Results Summary:', 'blue');
    
    const okCount = Object.values(urlResults).filter(r => r.status === 'ok').length;
    const errorCount = Object.values(urlResults).filter(r => r.status === 'error').length;
    const timeoutCount = Object.values(urlResults).filter(r => r.status === 'timeout').length;
    const skippedCount = Object.values(urlResults).filter(r => r.status === 'skipped').length;
    
    log(`✅ Working: ${okCount}`, 'green');
    log(`❌ Broken: ${errorCount}`, errorCount > 0 ? 'red' : 'green');
    log(`⏰ Timeout: ${timeoutCount}`, timeoutCount > 0 ? 'yellow' : 'green');
    log(`⏭️ Skipped: ${skippedCount}`, 'yellow');
    
    // Show broken links by file
    if (errorCount > 0 || timeoutCount > 0) {
        log('\n🚨 Issues Found:', 'red');
        
        for (const [file, links] of Object.entries(linksByFile)) {
            const brokenLinks = links.filter(link => {
                const result = urlResults[link.url];
                return result.status === 'error' || result.status === 'timeout';
            });
            
            if (brokenLinks.length > 0) {
                log(`\n📄 ${file}:`, 'yellow');
                for (const link of brokenLinks) {
                    const result = urlResults[link.url];
                    log(`  ❌ ${link.text} -> ${link.url}`, 'red');
                    log(`     Status: ${result.status} ${result.statusCode ? `(${result.statusCode})` : ''}`, 'red');
                }
            }
        }
    }
    
    log(`\n${errorCount === 0 && timeoutCount === 0 ? '🎉 All links are working!' : '⚠️  Some links need attention'}`, errorCount === 0 && timeoutCount === 0 ? 'green' : 'yellow');
    
    // Exit with error code if broken links found
    process.exit(errorCount > 0 ? 1 : 0);
}

// Run the checker
checkLinks().catch(error => {
    log(`❌ Fatal error: ${error.message}`, 'red');
    process.exit(1);
});



