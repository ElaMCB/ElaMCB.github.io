// Server-side analytics collection endpoint
// This will be called via a webhook or API to collect visit data
// For GitHub Pages, we'll use a GitHub Action webhook approach

import https from 'https';
import fs from 'fs';
import path from 'path';

const ANALYTICS_FILE = path.join(process.cwd(), 'analytics', 'visits.json');
const OWN_VISIT_IDENTIFIERS = [
  // Add your own identifiers here - IP addresses, user agents, etc.
  // These will be used to filter out your own visits
  process.env.OWN_IP_ADDRESSES?.split(',') || [],
  process.env.OWN_USER_AGENTS?.split(',') || [],
];

function loadAnalytics() {
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

function saveAnalytics(data) {
  try {
    const dir = path.dirname(ANALYTICS_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(ANALYTICS_FILE, JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Error saving analytics:', error);
  }
}

function isOwnVisit(visit) {
  // Check if this visit matches any of your identifiers
  const ip = visit.ip || '';
  const userAgent = visit.userAgent || '';
  
  // Check IP addresses
  if (OWN_VISIT_IDENTIFIERS[0]?.some(ownIp => ip.includes(ownIp))) {
    return true;
  }
  
  // Check user agents
  if (OWN_VISIT_IDENTIFIERS[1]?.some(ownUA => userAgent.includes(ownUA))) {
    return true;
  }
  
  return false;
}

export function collectVisit(visitData) {
  const analytics = loadAnalytics();
  
  // Mark if it's your own visit (but still store it for total counts)
  const visit = {
    ...visitData,
    timestamp: new Date().toISOString(),
    isOwnVisit: isOwnVisit(visitData),
  };
  
  analytics.visits.push(visit);
  
  // Keep only last 90 days of visits
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - 90);
  analytics.visits = analytics.visits.filter(v => 
    new Date(v.timestamp) > cutoffDate
  );
  
  saveAnalytics(analytics);
  return visit;
}

export function getFilteredAnalytics() {
  const analytics = loadAnalytics();
  
  // Separate own visits from others
  const ownVisits = analytics.visits.filter(v => v.isOwnVisit);
  const otherVisits = analytics.visits.filter(v => !v.isOwnVisit);
  
  // Calculate metrics for others only
  const uniqueVisitors = new Set(otherVisits.map(v => v.fingerprint || v.ip)).size;
  const totalVisits = otherVisits.length;
  
  // Group by date
  const dailyVisits = {};
  otherVisits.forEach(visit => {
    const date = new Date(visit.timestamp).toISOString().split('T')[0];
    dailyVisits[date] = (dailyVisits[date] || 0) + 1;
  });
  
  // Top referrers
  const referrers = {};
  otherVisits.forEach(visit => {
    const ref = visit.referrer || 'Direct';
    referrers[ref] = (referrers[ref] || 0) + 1;
  });
  
  // Top browsers
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

