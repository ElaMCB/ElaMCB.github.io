#!/usr/bin/env node

/**
 * Create First Research Release via GitHub API
 * 
 * This script creates a GitHub release for the AutoTriage Manual Test Assessment Tool
 * 
 * Usage:
 *   GITHUB_TOKEN=your_token node scripts/create-first-release.js
 * 
 * Or set token in environment:
 *   export GITHUB_TOKEN=your_token
 *   node scripts/create-first-release.js
 */

import https from 'https';
import fs from 'fs';
import path from 'path';

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const REPO = 'ElaMCB/ElaMCB.github.io';

if (!GITHUB_TOKEN) {
    console.error('❌ Error: GITHUB_TOKEN environment variable is not set');
    console.error('Please set it with: export GITHUB_TOKEN=your_token_here');
    console.error('Or create a Personal Access Token at: https://github.com/settings/tokens');
    console.error('Required scopes: repo (for private repos) or public_repo (for public repos)');
    process.exit(1);
}

const releaseData = {
    tag_name: 'autotriage-v1.0.0',
    name: 'AutoTriage: Manual Test Assessment Tool - v1.0.0',
    body: `## AutoTriage: Manual Test Assessment Tool

Professional framework for assessing manual regression tests and calculating business value. Analyzes technical feasibility, business impact, and ROI to generate 4-tier automation priorities.

### Features
- Technical feasibility analysis
- Business value calculation
- ROI analysis and prioritization
- 4-tier automation priority system

### Files Included
- \`research/notebooks/autotriage-manual-test-assessment.html\` - Interactive tool
- \`research/notebooks/autotriage-manual-test-assessment.ipynb\` - Jupyter notebook source

### View Research
- [View on Research Page](https://elamcb.github.io/research/)
- [View Source Code](https://github.com/ElaMCB/ElaMCB.github.io/tree/main/research/notebooks)

### Publication Date
Published: September 2025`,
    draft: false,
    prerelease: false
};

function makeRequest(options, data) {
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve({ statusCode: res.statusCode, body: JSON.parse(body) });
                } else {
                    reject({ statusCode: res.statusCode, body: body });
                }
            });
        });
        
        req.on('error', reject);
        if (data) {
            req.write(JSON.stringify(data));
        }
        req.end();
    });
}

async function uploadAsset(uploadUrl, filePath, fileName) {
    return new Promise((resolve, reject) => {
        const fileContent = fs.readFileSync(filePath);
        const url = new URL(uploadUrl);
        url.searchParams.set('name', fileName);
        
        const options = {
            hostname: url.hostname,
            path: url.pathname + url.search,
            method: 'POST',
            headers: {
                'Authorization': `token ${GITHUB_TOKEN}`,
                'Content-Type': 'application/octet-stream',
                'Content-Length': fileContent.length
            }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve({ statusCode: res.statusCode, body: JSON.parse(body) });
                } else {
                    reject({ statusCode: res.statusCode, body: body });
                }
            });
        });
        
        req.on('error', reject);
        req.write(fileContent);
        req.end();
    });
}

async function createRelease() {
    try {
        console.log('🚀 Creating GitHub Release...');
        console.log(`Tag: ${releaseData.tag_name}`);
        console.log(`Title: ${releaseData.name}`);
        console.log('');
        
        const options = {
            hostname: 'api.github.com',
            path: `/repos/${REPO}/releases`,
            method: 'POST',
            headers: {
                'Authorization': `token ${GITHUB_TOKEN}`,
                'User-Agent': 'Research-Release-Creator',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            }
        };
        
        const response = await makeRequest(options, releaseData);
        
        console.log('✅ Release created successfully!');
        console.log(`Release ID: ${response.body.id}`);
        console.log(`Release URL: ${response.body.html_url}`);
        console.log('');
        
        // Upload files
        const uploadUrl = response.body.upload_url.replace('{?name,label}', '');
        const files = [
            { path: 'research/notebooks/autotriage-manual-test-assessment.html', name: 'autotriage-manual-test-assessment.html' },
            { path: 'research/notebooks/autotriage-manual-test-assessment.ipynb', name: 'autotriage-manual-test-assessment.ipynb' }
        ];
        
        console.log('📦 Uploading files...');
        for (const file of files) {
            if (fs.existsSync(file.path)) {
                try {
                    await uploadAsset(uploadUrl, file.path, file.name);
                    console.log(`  ✅ Uploaded: ${file.name}`);
                } catch (error) {
                    console.error(`  ❌ Failed to upload ${file.name}:`, error.statusCode, error.body);
                }
            } else {
                console.log(`  ⚠️  File not found: ${file.path} (skipping)`);
            }
        }
        
        console.log('');
        console.log('🎉 Release created and files uploaded!');
        console.log(`View it at: ${response.body.html_url}`);
        
    } catch (error) {
        console.error('❌ Failed to create release');
        console.error(`HTTP Code: ${error.statusCode}`);
        console.error(`Response: ${error.body}`);
        process.exit(1);
    }
}

createRelease();

