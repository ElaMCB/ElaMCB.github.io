// Client-side function to send visit data to GitHub Gist
// This is the simplest solution that doesn't require external services

async function sendVisitToGist() {
  // Only send if Gist ID is configured
  const GIST_ID = window.ANALYTICS_GIST_ID;
  const GIST_TOKEN = window.ANALYTICS_GIST_TOKEN; // Should be a public read-only token or use a serverless function
  
  if (!GIST_ID) {
    // Gist not configured, skip server-side collection
    return;
  }

  try {
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

    // For security, we'll use a serverless function to write to Gist
    // Or use a public Gist with a read-only token
    // This is a placeholder - actual implementation depends on your setup
    
    const endpoint = `https://api.github.com/gists/${GIST_ID}`;
    
    // Note: Writing to Gist from client-side requires authentication
    // Better approach: Use a serverless function (Vercel/Netlify) as a proxy
    // Or use the webhook approach with repository_dispatch
    
    console.debug('Visit data collected:', visitData);
  } catch (error) {
    console.debug('Analytics collection error:', error);
  }
}

// Alternative: Use repository_dispatch webhook (requires GitHub token)
async function sendVisitViaWebhook() {
  const WEBHOOK_TOKEN = window.ANALYTICS_WEBHOOK_TOKEN;
  const REPO = 'ElaMCB/ElaMCB.github.io'; // Your repo
  
  if (!WEBHOOK_TOKEN) {
    return;
  }

  try {
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

    // Trigger repository_dispatch event
    await fetch(`https://api.github.com/repos/${REPO}/dispatches`, {
      method: 'POST',
      headers: {
        'Authorization': `token ${WEBHOOK_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        event_type: 'collect-visit',
        client_payload: {
          visit_data: visitData,
        },
      }),
    }).catch(error => {
      console.debug('Webhook dispatch failed:', error);
    });
  } catch (error) {
    console.debug('Webhook error:', error);
  }
}

