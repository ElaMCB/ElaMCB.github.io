// Fetch analytics data from Google Analytics 4 API
// This script is used by the weekly report workflow

import { google } from 'googleapis';

export async function fetchGA4Data(propertyId) {
  const credentialsJson = process.env.GA4_CREDENTIALS;
  
  if (!credentialsJson) {
    throw new Error('GA4_CREDENTIALS environment variable is required');
  }

  let credentials;
  try {
    credentials = JSON.parse(credentialsJson);
  } catch (error) {
    throw new Error('Failed to parse GA4_CREDENTIALS JSON');
  }

  // Authenticate with Google Analytics
  const auth = new google.auth.GoogleAuth({
    credentials: credentials,
    scopes: ['https://www.googleapis.com/auth/analytics.readonly'],
  });

  const analyticsData = google.analyticsdata('v1beta');

  // Calculate date range (last 7 days)
  const endDate = new Date();
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - 7);
  
  const startDateStr = startDate.toISOString().split('T')[0];
  const endDateStr = endDate.toISOString().split('T')[0];

  try {
    // Get aggregate metrics
    const [aggregateResponse, referrersResponse, browsersResponse, timeseriesResponse] = await Promise.all([
      // Total visitors, sessions, pageviews
      analyticsData.properties.runReport({
        auth: auth,
        property: `properties/${propertyId}`,
        requestBody: {
          dateRanges: [{ startDate: startDateStr, endDate: endDateStr }],
          metrics: [
            { name: 'activeUsers' },
            { name: 'sessions' },
            { name: 'screenPageViews' },
            { name: 'bounceRate' },
            { name: 'averageSessionDuration' },
          ],
        },
      }),
      
      // Top referrers
      analyticsData.properties.runReport({
        auth: auth,
        property: `properties/${propertyId}`,
        requestBody: {
          dateRanges: [{ startDate: startDateStr, endDate: endDateStr }],
          dimensions: [{ name: 'sessionSource' }],
          metrics: [{ name: 'sessions' }],
          orderBys: [{ metric: { metricName: 'sessions' }, desc: true }],
          limit: 10,
        },
      }),
      
      // Top browsers
      analyticsData.properties.runReport({
        auth: auth,
        property: `properties/${propertyId}`,
        requestBody: {
          dateRanges: [{ startDate: startDateStr, endDate: endDateStr }],
          dimensions: [{ name: 'browser' }],
          metrics: [{ name: 'sessions' }],
          orderBys: [{ metric: { metricName: 'sessions' }, desc: true }],
          limit: 10,
        },
      }),
      
      // Daily timeseries
      analyticsData.properties.runReport({
        auth: auth,
        property: `properties/${propertyId}`,
        requestBody: {
          dateRanges: [{ startDate: startDateStr, endDate: endDateStr }],
          dimensions: [{ name: 'date' }],
          metrics: [{ name: 'sessions' }],
        },
      }),
    ]);

    // Parse aggregate data
    const aggregateRow = aggregateResponse.data.rows?.[0];
    const metrics = aggregateRow?.metricValues || [];
    
    const activeUsers = parseInt(metrics[0]?.value || '0', 10);
    const sessions = parseInt(metrics[1]?.value || '0', 10);
    const pageviews = parseInt(metrics[2]?.value || '0', 10);
    const bounceRate = parseFloat(metrics[3]?.value || '0');
    const avgDuration = parseFloat(metrics[4]?.value || '0');

    // Parse daily visits
    const dailyVisits = {};
    if (timeseriesResponse.data.rows) {
      timeseriesResponse.data.rows.forEach(row => {
        const date = row.dimensionValues[0].value;
        const formattedDate = `${date.substring(0, 4)}-${date.substring(4, 6)}-${date.substring(6, 8)}`;
        dailyVisits[formattedDate] = parseInt(row.metricValues[0].value || '0', 10);
      });
    }

    // Parse referrers
    const referrers = (referrersResponse.data.rows || []).map(row => ({
      referrer: row.dimensionValues[0].value || 'Direct',
      count: parseInt(row.metricValues[0].value || '0', 10),
    }));

    // Parse browsers
    const browsers = (browsersResponse.data.rows || []).map(row => ({
      browser: row.dimensionValues[0].value || 'Unknown',
      count: parseInt(row.metricValues[0].value || '0', 10),
    }));

    return {
      period: {
        start: startDateStr,
        end: endDateStr,
      },
      total: {
        allVisits: sessions,
        ownVisits: 0, // GA4 handles IP exclusion via data filters
        otherVisits: sessions, // Already filtered by GA4 data filters
        uniqueVisitors: activeUsers,
        pageviews: pageviews,
        bounceRate: bounceRate,
        visitDuration: avgDuration,
      },
      dailyVisits,
      referrers,
      browsers,
    };
  } catch (error) {
    console.error('Error fetching GA4 data:', error);
    throw error;
  }
}

