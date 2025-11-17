/**
 * LLM & Gen AI Research Auto-Discovery System
 * 
 * Scans multiple sources for:
 * - New LLM releases
 * - Groundbreaking Gen AI research papers
 * - Model releases on Hugging Face
 * - GitHub repositories for new LLMs
 * 
 * Usage: node auto-discover-llms.js
 */

const https = require('https');
const fs = require('fs');

// Search keywords for LLMs
const LLM_KEYWORDS = [
    'large language model',
    'LLM release',
    'new language model',
    'foundation model',
    'multimodal LLM',
    'code LLM',
    'instruction tuned',
    'chat model'
];

// ArXiv categories to monitor
const ARXIV_CATEGORIES = [
    'cs.CL',  // Computation and Language
    'cs.AI',  // Artificial Intelligence
    'cs.LG',  // Machine Learning
    'cs.CV'   // Computer Vision (for multimodal)
];

// Existing models to avoid duplicates
const EXISTING_MODELS = [
    'gpt-4',
    'gpt-3.5',
    'claude',
    'llama',
    'mistral',
    'gemini',
    'palm',
    'chinchilla',
    'gopher',
    'jurassic',
    'bloom',
    'opt',
    't5',
    'bert',
    'roberta'
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
                    resolve(data); // Return raw data if not JSON
                }
            });
        }).on('error', reject);
    });
}

/**
 * Search GitHub for new LLM repositories
 */
async function searchGitHub(keyword) {
    try {
        const url = `https://api.github.com/search/repositories?q=${encodeURIComponent(keyword)}+language:python&sort=updated&order=desc&per_page=20`;
        const data = await fetchData(url, {
            'User-Agent': 'LLM-Discovery-Bot',
            'Accept': 'application/vnd.github.v3+json'
        });
        
        return data.items
            .filter(repo => {
                const name = repo.name.toLowerCase();
                const desc = (repo.description || '').toLowerCase();
                
                // Check if it's a new model not in our list
                const isNewModel = !EXISTING_MODELS.some(model => 
                    name.includes(model) || desc.includes(model)
                );
                
                // Filter for significant repositories (stars, recent updates)
                const isSignificant = repo.stargazers_count > 50 || 
                                   (repo.updated_at && new Date(repo.updated_at) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000));
                
                return isNewModel && isSignificant;
            })
            .map(repo => ({
                name: repo.name,
                description: repo.description,
                url: repo.html_url,
                stars: repo.stargazers_count,
                language: repo.language,
                updated: repo.updated_at,
                source: 'GitHub'
            }));
    } catch (error) {
        console.error(`GitHub search error for "${keyword}":`, error.message);
        return [];
    }
}

/**
 * Search ArXiv for new papers
 */
async function searchArXiv(category, maxResults = 50) {
    try {
        const url = `http://export.arxiv.org/api/query?search_query=cat:${category}&sortBy=submittedDate&sortOrder=descending&max_results=${maxResults}`;
        const data = await fetchData(url);
        
        // Parse XML (simplified - in production use proper XML parser)
        const entries = [];
        const entryMatches = data.match(/<entry>[\s\S]*?<\/entry>/g) || [];
        
        entryMatches.forEach(entry => {
            const titleMatch = entry.match(/<title>(.*?)<\/title>/);
            const summaryMatch = entry.match(/<summary>(.*?)<\/summary>/);
            const idMatch = entry.match(/<id>(.*?)<\/id>/);
            const publishedMatch = entry.match(/<published>(.*?)<\/published>/);
            
            if (titleMatch && idMatch) {
                const title = titleMatch[1].replace(/\n/g, ' ').trim();
                const summary = summaryMatch ? summaryMatch[1].replace(/\n/g, ' ').trim() : '';
                const paperId = idMatch[1].split('/').pop();
                const published = publishedMatch ? publishedMatch[1] : '';
                
                // Filter for significant papers (recent, relevant keywords)
                const isRecent = published && new Date(published) > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                const hasRelevantKeywords = /(llm|language model|foundation model|multimodal|instruction|fine.?tun)/i.test(title + ' ' + summary);
                
                if (isRecent && hasRelevantKeywords) {
                    entries.push({
                        name: title,
                        description: summary.substring(0, 300) + (summary.length > 300 ? '...' : ''),
                        url: `https://arxiv.org/abs/${paperId}`,
                        paperId: paperId,
                        published: published,
                        source: 'ArXiv',
                        category: category
                    });
                }
            }
        });
        
        return entries;
    } catch (error) {
        console.error(`ArXiv search error for "${category}":`, error.message);
        return [];
    }
}

/**
 * Search Hugging Face for new models
 */
async function searchHuggingFace() {
    try {
        // Hugging Face API endpoint for models
        const url = 'https://huggingface.co/api/models?sort=updated&direction=-1&limit=50';
        const data = await fetchData(url, {
            'User-Agent': 'LLM-Discovery-Bot'
        });
        
        if (!Array.isArray(data)) return [];
        
        return data
            .filter(model => {
                const name = (model.id || '').toLowerCase();
                const tags = (model.tags || []).map(t => t.toLowerCase());
                
                // Filter for LLM-related models
                const isLLM = tags.some(tag => 
                    tag.includes('llm') || 
                    tag.includes('text-generation') ||
                    tag.includes('language-model') ||
                    tag.includes('foundation-model')
                );
                
                // Check if it's a new model
                const isNewModel = !EXISTING_MODELS.some(existing => 
                    name.includes(existing)
                );
                
                // Recent updates (last 7 days)
                const isRecent = model.updatedAt && 
                               new Date(model.updatedAt) > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                
                return isLLM && isNewModel && isRecent;
            })
            .map(model => ({
                name: model.id || 'Unknown',
                description: model.pipeline_tag || 'Language model',
                url: `https://huggingface.co/${model.id}`,
                downloads: model.downloads || 0,
                likes: model.likes || 0,
                updated: model.updatedAt,
                source: 'Hugging Face'
            }));
    } catch (error) {
        console.error(`Hugging Face search error:`, error.message);
        return [];
    }
}

/**
 * Main discovery function
 */
async function discoverNewLLMs() {
    console.log('🔍 Starting LLM & Gen AI Research discovery...\n');
    
    const discoveries = {
        models: [],
        papers: []
    };
    
    // Search GitHub for new LLM repositories
    console.log('📦 Searching GitHub for new LLM repositories...');
    for (const keyword of LLM_KEYWORDS.slice(0, 3)) { // Limit to avoid rate limits
        console.log(`  Searching: "${keyword}"`);
        const githubResults = await searchGitHub(keyword);
        discoveries.models.push(...githubResults);
        await new Promise(resolve => setTimeout(resolve, 2000)); // Rate limit protection
    }
    
    // Search ArXiv for new papers
    console.log('\n📄 Searching ArXiv for new research papers...');
    for (const category of ARXIV_CATEGORIES) {
        console.log(`  Searching category: ${category}`);
        const arxivResults = await searchArXiv(category, 20);
        discoveries.papers.push(...arxivResults);
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    // Search Hugging Face for new models
    console.log('\n🤗 Searching Hugging Face for new models...');
    const hfResults = await searchHuggingFace();
    discoveries.models.push(...hfResults);
    
    // Remove duplicates
    const uniqueModels = Array.from(
        new Map(discoveries.models.map(item => [item.name, item])).values()
    );
    
    const uniquePapers = Array.from(
        new Map(discoveries.papers.map(item => [item.paperId || item.name, item])).values()
    );
    
    // Sort by relevance/recency
    uniqueModels.sort((a, b) => {
        const scoreA = (a.stars || 0) + (a.downloads || 0) + (a.likes || 0);
        const scoreB = (b.stars || 0) + (b.downloads || 0) + (b.likes || 0);
        return scoreB - scoreA;
    });
    
    uniquePapers.sort((a, b) => {
        const dateA = new Date(a.published || 0);
        const dateB = new Date(b.published || 0);
        return dateB - dateA;
    });
    
    return {
        models: uniqueModels,
        papers: uniquePapers
    };
}

/**
 * Generate markdown report
 */
function generateReport(discoveries) {
    const timestamp = new Date().toISOString().split('T')[0];
    
    let report = `# LLM & Gen AI Research Discoveries - ${timestamp}\n\n`;
    
    report += `## New LLM Models Found: ${discoveries.models.length}\n\n`;
    discoveries.models.forEach((model, index) => {
        report += `### ${index + 1}. ${model.name}\n\n`;
        report += `- **Description**: ${model.description}\n`;
        report += `- **URL**: ${model.url}\n`;
        report += `- **Source**: ${model.source}\n`;
        if (model.stars) report += `- **GitHub Stars**: ${model.stars}\n`;
        if (model.downloads) report += `- **Downloads**: ${model.downloads.toLocaleString()}\n`;
        if (model.likes) report += `- **Likes**: ${model.likes}\n`;
        if (model.updated) report += `- **Updated**: ${model.updated}\n`;
        report += `\n`;
    });
    
    report += `\n---\n\n`;
    report += `## New Research Papers Found: ${discoveries.papers.length}\n\n`;
    discoveries.papers.forEach((paper, index) => {
        report += `### ${index + 1}. ${paper.name}\n\n`;
        report += `- **Description**: ${paper.description}\n`;
        report += `- **URL**: ${paper.url}\n`;
        report += `- **Source**: ${paper.source}\n`;
        if (paper.category) report += `- **Category**: ${paper.category}\n`;
        if (paper.published) report += `- **Published**: ${paper.published}\n`;
        report += `\n`;
    });
    
    report += `\n---\n\n`;
    report += `**Next Steps:**\n`;
    report += `1. Review each model/paper manually\n`;
    report += `2. Test promising models (2-4 hours each)\n`;
    report += `3. Read and summarize key papers\n`;
    report += `4. Update tracking document\n`;
    report += `5. Commit changes\n\n`;
    
    return report;
}

/**
 * Save discoveries to file
 */
function saveDiscoveries(discoveries) {
    const timestamp = new Date().toISOString().split('T')[0];
    
    // Save JSON for programmatic processing
    const jsonFilename = `discoveries-${timestamp}.json`;
    const jsonData = {
        scanDate: timestamp,
        models: discoveries.models,
        papers: discoveries.papers,
        totalModels: discoveries.models.length,
        totalPapers: discoveries.papers.length
    };
    
    fs.writeFileSync(jsonFilename, JSON.stringify(jsonData, null, 2));
    console.log(`📊 JSON data saved to: ${jsonFilename}`);
    
    // Save markdown report
    const mdFilename = `discoveries-${timestamp}.md`;
    const report = generateReport(discoveries);
    fs.writeFileSync(mdFilename, report);
    console.log(`📝 Report saved to: ${mdFilename}`);
}

/**
 * Run the discovery
 */
(async () => {
    try {
        const discoveries = await discoverNewLLMs();
        
        console.log(`\n✅ Discovery complete!`);
        console.log(`📊 Found ${discoveries.models.length} new LLM models`);
        console.log(`📄 Found ${discoveries.papers.length} new research papers\n`);
        
        // Always save scan date, even if no discoveries
        if (discoveries.models.length > 0 || discoveries.papers.length > 0) {
            saveDiscoveries(discoveries);
            
            // Print top discoveries
            if (discoveries.models.length > 0) {
                console.log('\n🔥 Top 5 New Models:\n');
                discoveries.models.slice(0, 5).forEach((model, index) => {
                    console.log(`${index + 1}. ${model.name} (${model.source})`);
                    console.log(`   ${model.url}\n`);
                });
            }
            
            if (discoveries.papers.length > 0) {
                console.log('\n📚 Top 5 New Papers:\n');
                discoveries.papers.slice(0, 5).forEach((paper, index) => {
                    console.log(`${index + 1}. ${paper.name.substring(0, 60)}...`);
                    console.log(`   ${paper.url}\n`);
                });
            }
        } else {
            console.log('No new LLMs or papers discovered this week.');
            // Still save scan date file for tracking
            saveDiscoveries({ models: [], papers: [] });
        }
    } catch (error) {
        console.error('❌ Discovery failed:', error);
        process.exit(1);
    }
})();

