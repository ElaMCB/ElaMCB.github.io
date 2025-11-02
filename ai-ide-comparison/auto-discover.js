/**
 * AI IDE Auto-Discovery System
 * 
 * This script monitors GitHub, Product Hunt, and Hacker News for new AI IDE announcements
 * Run weekly via GitHub Actions to keep the comparison updated
 * 
 * Usage: node auto-discover.js
 */

const https = require('https');
const fs = require('fs');

// Search keywords for AI IDEs
const SEARCH_KEYWORDS = [
    'AI IDE',
    'AI code editor',
    'AI coding assistant',
    'LLM code editor',
    'copilot alternative',
    'cursor alternative',
    'AI pair programming'
];

// Data sources
const SOURCES = {
    github: {
        url: 'https://api.github.com/search/repositories',
        params: (keyword) => `?q=${encodeURIComponent(keyword)}&sort=stars&order=desc&per_page=10`,
        headers: {
            'User-Agent': 'AI-IDE-Tracker',
            'Accept': 'application/vnd.github.v3+json'
        }
    },
    productHunt: {
        url: 'https://api.producthunt.com/v2/api/graphql',
        // Requires API key - add to GitHub Secrets
    },
    hackerNews: {
        algolia: 'https://hn.algolia.com/api/v1/search',
        params: (keyword) => `?query=${encodeURIComponent(keyword)}&tags=story&hitsPerPage=10`
    }
};

// Existing IDEs to avoid duplicates
const EXISTING_IDES = [
    'cursor',
    'windsurf',
    'codeium',
    'void',
    'continue.dev',
    'github copilot',
    'zed',
    'replit',
    'codewhisperer',
    'tabnine',
    'trae'
];

/**
 * Fetch data from a URL
 */
function fetchData(url, headers = {}) {
    return new Promise((resolve, reject) => {
        https.get(url, { headers }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', reject);
    });
}

/**
 * Search GitHub for new AI IDEs
 */
async function searchGitHub(keyword) {
    try {
        const url = SOURCES.github.url + SOURCES.github.params(keyword);
        const data = await fetchData(url, SOURCES.github.headers);
        
        return data.items
            .filter(repo => {
                const name = repo.name.toLowerCase();
                const desc = (repo.description || '').toLowerCase();
                
                // Check if it's a new IDE not in our list
                return !EXISTING_IDES.some(ide => name.includes(ide) || desc.includes(ide));
            })
            .map(repo => ({
                name: repo.name,
                description: repo.description,
                url: repo.html_url,
                stars: repo.stargazers_count,
                language: repo.language,
                source: 'GitHub'
            }));
    } catch (error) {
        console.error(`GitHub search error for "${keyword}":`, error.message);
        return [];
    }
}

/**
 * Search Hacker News via Algolia
 */
async function searchHackerNews(keyword) {
    try {
        const url = SOURCES.hackerNews.algolia + SOURCES.hackerNews.params(keyword);
        const data = await fetchData(url);
        
        return data.hits
            .filter(hit => {
                const title = (hit.title || '').toLowerCase();
                return !EXISTING_IDES.some(ide => title.includes(ide));
            })
            .map(hit => ({
                name: hit.title,
                description: hit.title,
                url: hit.url || `https://news.ycombinator.com/item?id=${hit.objectID}`,
                points: hit.points,
                source: 'Hacker News'
            }));
    } catch (error) {
        console.error(`Hacker News search error for "${keyword}":`, error.message);
        return [];
    }
}

/**
 * Main discovery function
 */
async function discoverNewIDEs() {
    console.log('🔍 Starting AI IDE discovery...\n');
    
    const discoveries = [];
    
    // Search across all keywords
    for (const keyword of SEARCH_KEYWORDS) {
        console.log(`Searching for: "${keyword}"`);
        
        // GitHub search
        const githubResults = await searchGitHub(keyword);
        discoveries.push(...githubResults);
        
        // Hacker News search
        const hnResults = await searchHackerNews(keyword);
        discoveries.push(...hnResults);
        
        // Rate limit protection
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Remove duplicates
    const uniqueDiscoveries = Array.from(
        new Map(discoveries.map(item => [item.name, item])).values()
    );
    
    // Sort by popularity
    uniqueDiscoveries.sort((a, b) => {
        const scoreA = (a.stars || 0) + (a.points || 0);
        const scoreB = (b.stars || 0) + (b.points || 0);
        return scoreB - scoreA;
    });
    
    return uniqueDiscoveries;
}

/**
 * Generate markdown report
 */
function generateReport(discoveries) {
    const timestamp = new Date().toISOString().split('T')[0];
    
    let report = `# New AI IDE Discoveries - ${timestamp}\n\n`;
    report += `Found ${discoveries.length} potential new AI IDEs:\n\n`;
    
    discoveries.forEach((ide, index) => {
        report += `## ${index + 1}. ${ide.name}\n\n`;
        report += `- **Description**: ${ide.description}\n`;
        report += `- **URL**: ${ide.url}\n`;
        report += `- **Source**: ${ide.source}\n`;
        if (ide.stars) report += `- **GitHub Stars**: ${ide.stars}\n`;
        if (ide.points) report += `- **HN Points**: ${ide.points}\n`;
        if (ide.language) report += `- **Language**: ${ide.language}\n`;
        report += `\n`;
    });
    
    report += `---\n\n`;
    report += `**Next Steps:**\n`;
    report += `1. Review each IDE manually\n`;
    report += `2. Test the IDE for 2-4 hours\n`;
    report += `3. Assign tier (S/A/B)\n`;
    report += `4. Update comparison page\n`;
    report += `5. Commit changes\n\n`;
    
    return report;
}

/**
 * Save discoveries to file
 */
function saveDiscoveries(discoveries) {
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `discoveries-${timestamp}.md`;
    
    const report = generateReport(discoveries);
    fs.writeFileSync(filename, report);
    
    console.log(`\n📝 Report saved to: ${filename}`);
    
    // Save JSON for programmatic processing AND web display
    const jsonFilename = `discoveries-${timestamp}.json`;
    const jsonData = {
        scanDate: timestamp,
        totalDiscoveries: discoveries.length,
        discoveries: discoveries.map(d => ({
            name: d.name,
            description: d.description,
            url: d.url,
            stars: d.stars || null,
            points: d.points || null,
            language: d.language || null,
            source: d.source
        }))
    };
    
    fs.writeFileSync(jsonFilename, JSON.stringify(jsonData.discoveries, null, 2));
    
    console.log(`📊 JSON data saved to: ${jsonFilename}`);
    console.log(`🌐 This file will be automatically displayed on the comparison page`);
}

/**
 * Run the discovery
 */
(async () => {
    try {
        const discoveries = await discoverNewIDEs();
        
        console.log(`\n✅ Discovery complete!`);
        console.log(`📊 Found ${discoveries.length} potential new AI IDEs\n`);
        
        if (discoveries.length > 0) {
            saveDiscoveries(discoveries);
            
            // Print top 5 for quick review
            console.log('\n🔥 Top 5 Discoveries:\n');
            discoveries.slice(0, 5).forEach((ide, index) => {
                console.log(`${index + 1}. ${ide.name} (${ide.source})`);
                console.log(`   ${ide.url}\n`);
            });
        } else {
            console.log('No new IDEs discovered this week.');
        }
    } catch (error) {
        console.error('❌ Discovery failed:', error);
        process.exit(1);
    }
})();

