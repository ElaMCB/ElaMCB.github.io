// Client-side function to send visit data to server
// This will be added to index.html

async function sendVisitToServer() {
  // Only send if we have a collection endpoint configured
  const COLLECTION_ENDPOINT = window.ANALYTICS_COLLECTION_ENDPOINT;
  if (!COLLECTION_ENDPOINT) {
    // Endpoint not configured, skip server-side collection
    return;
  }

  try {
    const analytics = getAnalytics();
    const fingerprint = getBasicFingerprint();
    const browser = getBrowserInfo();
    
    const visitData = {
      fingerprint: fingerprint,
      userAgent: navigator.userAgent,
      browser: browser,
      referrer: document.referrer || 'Direct Traffic',
      url: window.location.href,
      timestamp: new Date().toISOString(),
      screenSize: `${screen.width}x${screen.height}`,
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    };

    // Send to collection endpoint (non-blocking)
    fetch(COLLECTION_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(visitData),
      keepalive: true, // Ensure request completes even if page unloads
    }).catch(error => {
      // Silently fail - don't break the page if collection fails
      console.debug('Analytics collection failed:', error);
    });
  } catch (error) {
    // Silently fail - analytics collection should never break the page
    console.debug('Analytics collection error:', error);
  }
}

// Call this after initAnalytics()
// Add to index.html: sendVisitToServer();

