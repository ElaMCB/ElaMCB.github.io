// Generate weekly analytics report (excluding own visits)
// This script is run by GitHub Actions weekly
// Supports: Google Analytics 4 (free) or local visits.json file

import fs from 'fs';
import path from 'path';

const ANALYTICS_FILE = path.join(process.cwd(), 'analytics', 'visits.json');
const OWN_VISIT_IDENTIFIERS = [
  process.env.OWN_IP_ADDRESSES?.split(',').filter(Boolean) || [],
  process.env.OWN_USER_AGENTS?.split(',').filter(Boolean) || [],
];

function loadLocalAnalytics() {
  try {
    if (fs.existsSync(ANALYTICS_FILE)) {
      return JSON.parse(fs.readFileSync(ANALYTICS_FILE, 'utf8'));
    }
  } catch (error) {
    console.error('Error loading analytics:', error);
  }
  
  return {
    visits: [],
    startDate: new Date().toISOString(),
  };
}

function isOwnVisit(visit) {
  const ip = visit.ip || '';
  const userAgent = visit.userAgent || '';
  
  if (OWN_VISIT_IDENTIFIERS[0]?.some(ownIp => ip.includes(ownIp))) {
    return true;
  }
  
  if (OWN_VISIT_IDENTIFIERS[1]?.some(ownUA => userAgent.includes(ownUA))) {
    return true;
  }
  
  return false;
}

async function getFilteredAnalytics() {
  // Check if using Google Analytics 4
  const ga4PropertyId = process.env.GA4_PROPERTY_ID;
  
  if (ga4PropertyId) {
    console.log('Using Google Analytics 4...');
    try {
      const { fetchGA4Data } = await import('./fetch-ga4-data.js');
      return await fetchGA4Data(ga4PropertyId);
    } catch (error) {
      console.error('Failed to fetch GA4 data, falling back to local analytics:', error);
    }
  }
  
  // Fall back to local analytics file
  console.log('Using local analytics file...');
  const analytics = loadLocalAnalytics();
  
  const ownVisits = analytics.visits.filter(v => v.isOwnVisit || isOwnVisit(v));
  const otherVisits = analytics.visits.filter(v => !v.isOwnVisit && !isOwnVisit(v));
  
  const uniqueVisitors = new Set(otherVisits.map(v => v.fingerprint || v.ip)).size;
  const totalVisits = otherVisits.length;
  
  const dailyVisits = {};
  otherVisits.forEach(visit => {
    const date = new Date(visit.timestamp).toISOString().split('T')[0];
    dailyVisits[date] = (dailyVisits[date] || 0) + 1;
  });
  
  const referrers = {};
  otherVisits.forEach(visit => {
    const ref = visit.referrer || 'Direct';
    referrers[ref] = (referrers[ref] || 0) + 1;
  });
  
  const browsers = {};
  otherVisits.forEach(visit => {
    const browser = visit.browser || 'Unknown';
    browsers[browser] = (browsers[browser] || 0) + 1;
  });
  
  return {
    period: {
      start: analytics.startDate,
      end: new Date().toISOString(),
    },
    total: {
      allVisits: analytics.visits.length,
      ownVisits: ownVisits.length,
      otherVisits: totalVisits,
      uniqueVisitors,
      pageviews: totalVisits, // Approximate
      bounceRate: 0,
    },
    dailyVisits,
    referrers: Object.entries(referrers)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([ref, count]) => ({ referrer: ref, count })),
    browsers: Object.entries(browsers)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([browser, count]) => ({ browser, count })),
  };
}

function generateEmailHTML(report) {
  const weekStart = new Date(report.period.start).toLocaleDateString();
  const weekEnd = new Date(report.period.end).toLocaleDateString();
  
  const last7Days = [];
  for (let i = 6; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    last7Days.push({
      date: date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }),
      visits: report.dailyVisits[dateStr] || 0,
    });
  }
  
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; }
    .content { background: #f5f5f5; padding: 30px; border-radius: 0 0 10px 10px; }
    .stat-box { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .stat-number { font-size: 36px; font-weight: bold; color: #5b7fb8; }
    .stat-label { color: #666; font-size: 14px; margin-top: 5px; }
    .daily-chart { margin: 20px 0; }
    .day-bar { display: flex; align-items: center; margin: 10px 0; }
    .day-label { width: 100px; font-size: 12px; }
    .bar { background: #5b7fb8; height: 30px; border-radius: 4px; display: flex; align-items: center; padding: 0 10px; color: white; font-weight: bold; min-width: 40px; }
    .list-item { padding: 8px 0; border-bottom: 1px solid #eee; }
    .list-item:last-child { border-bottom: none; }
    .footer { text-align: center; margin-top: 30px; color: #999; font-size: 12px; }
    .note { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📊 Weekly Portfolio Analytics Report</h1>
      <p>${weekStart} - ${weekEnd}</p>
    </div>
    <div class="content">
      <div class="note">
        <strong>Note:</strong> This report excludes your own visits. Total visits (including yours) are shown for reference.
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
        <div class="stat-box">
          <div class="stat-number">${report.total.otherVisits}</div>
          <div class="stat-label">Visits (Excluding Yours)</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">${report.total.uniqueVisitors}</div>
          <div class="stat-label">Unique Visitors</div>
        </div>
        ${report.total.pageviews > 0 ? `
        <div class="stat-box">
          <div class="stat-number">${report.total.pageviews}</div>
          <div class="stat-label">Pageviews</div>
        </div>
        ` : ''}
        ${report.total.bounceRate > 0 ? `
        <div class="stat-box">
          <div class="stat-number">${(report.total.bounceRate * 100).toFixed(1)}%</div>
          <div class="stat-label">Bounce Rate</div>
        </div>
        ` : ''}
      </div>
      
      <div class="stat-box">
        <div style="font-size: 14px; color: #666; margin-bottom: 10px;">
          Total Visits (Including Yours): <strong>${report.total.allVisits}</strong> | 
          Your Visits: <strong>${report.total.ownVisits}</strong>
        </div>
      </div>
      
      <div class="stat-box">
        <h3 style="margin-top: 0;">Last 7 Days</h3>
        <div class="daily-chart">
          ${last7Days.map(day => `
            <div class="day-bar">
              <div class="day-label">${day.date}</div>
              <div class="bar" style="width: ${Math.max(day.visits * 20, 40)}px;">
                ${day.visits}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
      
      ${report.referrers.length > 0 ? `
      <div class="stat-box">
        <h3 style="margin-top: 0;">Top Traffic Sources</h3>
        ${report.referrers.map(ref => `
          <div class="list-item">
            <strong>${ref.referrer}</strong> - ${ref.count} visits
          </div>
        `).join('')}
      </div>
      ` : ''}
      
      ${report.browsers.length > 0 ? `
      <div class="stat-box">
        <h3 style="margin-top: 0;">Top Browsers</h3>
        ${report.browsers.map(browser => `
          <div class="list-item">
            <strong>${browser.browser}</strong> - ${browser.count} visits
          </div>
        `).join('')}
      </div>
      ` : ''}
      
      <div class="footer">
        <p>Generated automatically by your portfolio analytics system</p>
        <p>View full analytics: <a href="https://elamcb.github.io/analytics.html">elamcb.github.io/analytics.html</a></p>
      </div>
    </div>
  </div>
</body>
</html>
  `.trim();
}

function generateEmailText(report) {
  const weekStart = new Date(report.period.start).toLocaleDateString();
  const weekEnd = new Date(report.period.end).toLocaleDateString();
  
  return `
WEEKLY PORTFOLIO ANALYTICS REPORT
${weekStart} - ${weekEnd}

Note: This report excludes your own visits. Total visits (including yours) are shown for reference.

VISITS (Excluding Yours): ${report.total.otherVisits}
UNIQUE VISITORS: ${report.total.uniqueVisitors}
${report.total.pageviews > 0 ? `PAGEVIEWS: ${report.total.pageviews}` : ''}
${report.total.bounceRate > 0 ? `BOUNCE RATE: ${(report.total.bounceRate * 100).toFixed(1)}%` : ''}

Total Visits (Including Yours): ${report.total.allVisits}
Your Visits: ${report.total.ownVisits}

TOP TRAFFIC SOURCES:
${report.referrers.map(ref => `  - ${ref.referrer}: ${ref.count} visits`).join('\n')}

TOP BROWSERS:
${report.browsers.map(b => `  - ${b.browser}: ${b.count} visits`).join('\n')}

View full analytics: https://elamcb.github.io/analytics.html
  `.trim();
}

// Main execution (async)
(async () => {
  const report = await getFilteredAnalytics();
  const html = generateEmailHTML(report);
  const text = generateEmailText(report);

  const reportDir = path.join(process.cwd(), 'analytics');
  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }

  fs.writeFileSync(path.join(reportDir, 'weekly-report.html'), html);
  fs.writeFileSync(path.join(reportDir, 'weekly-report.txt'), text);

  console.log('Weekly report generated successfully!');
  console.log(`- Visits (excluding yours): ${report.total.otherVisits}`);
  console.log(`- Unique visitors: ${report.total.uniqueVisitors}`);
  console.log(`- Total visits: ${report.total.allVisits}`);
  if (report.total.pageviews > 0) {
    console.log(`- Pageviews: ${report.total.pageviews}`);
  }
})();
