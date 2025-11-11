# Playwright Email Report Setup Guide

## GitHub Secrets Configuration

To enable email reports, you need to add the following secrets to your GitHub repository:

### How to Add Secrets
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each of the following secrets:

### Required Secrets

#### For Gmail (Recommended for personal use)

| Secret Name | Value | Example |
|-------------|-------|---------|
| `MAIL_SERVER` | `smtp.gmail.com` | smtp.gmail.com |
| `MAIL_PORT` | `587` | 587 |
| `MAIL_USERNAME` | Your Gmail address | your.email@gmail.com |
| `MAIL_PASSWORD` | Gmail App Password* | xxxx xxxx xxxx xxxx |
| `MAIL_TO` | Recipient email | your.email@gmail.com |
| `MAIL_FROM` | Sender email (same as username) | your.email@gmail.com |

**Important:** For Gmail, you need to use an **App Password**, not your regular password:
1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate a new app password for "Mail"
4. Copy the 16-character password and use it as `MAIL_PASSWORD`

#### For Outlook/Hotmail

| Secret Name | Value |
|-------------|-------|
| `MAIL_SERVER` | `smtp-mail.outlook.com` |
| `MAIL_PORT` | `587` |
| `MAIL_USERNAME` | Your Outlook email |
| `MAIL_PASSWORD` | Your Outlook password |
| `MAIL_TO` | Recipient email |
| `MAIL_FROM` | Your Outlook email |

#### For SendGrid

| Secret Name | Value |
|-------------|-------|
| `MAIL_SERVER` | `smtp.sendgrid.net` |
| `MAIL_PORT` | `587` |
| `MAIL_USERNAME` | `apikey` (literally the word "apikey") |
| `MAIL_PASSWORD` | Your SendGrid API Key |
| `MAIL_TO` | Recipient email |
| `MAIL_FROM` | Verified sender email in SendGrid |

## Workflow Triggers

The workflow runs automatically on:
- **Push** to `main` or `master` branch
- **Pull requests** to `main` or `master` branch
- **Daily schedule** at 9 AM UTC (optional - can be removed)
- **Manual trigger** via GitHub Actions UI

## Testing the Workflow

1. Commit and push the workflow file:
   ```bash
   git add .github/workflows/playwright-tests.yml
   git commit -m "Add Playwright email reporting workflow"
   git push
   ```

2. Go to **Actions** tab in your GitHub repository
3. Select **Playwright Tests with Email Report**
4. Click **Run workflow** to test manually

## What Gets Emailed

- **Subject**: Includes repository name and test status (success/failure)
- **Body**: Contains workflow details, branch, commit info, and link to full run
- **Attachment**: ZIP file containing the complete HTML report

## Viewing the Report

1. Download the attached `playwright-report.zip`
2. Extract the ZIP file
3. Open `index.html` in your browser
4. You'll see an interactive report with:
   - Test results and statistics
   - Screenshots of failures
   - Trace viewer for debugging
   - Timeline of test execution

## Troubleshooting

### Email not sending?
- Check that all secrets are set correctly
- Verify your email provider's SMTP settings
- Check the GitHub Actions logs for error messages

### Tests failing?
- The email will still be sent (even if tests fail)
- Check the HTML report for details
- View the full logs in GitHub Actions

### Want to customize?
- Edit `.github/workflows/playwright-tests.yml`
- Adjust triggers, schedule, or email content as needed
- You can also change `continue-on-error: true` to `false` if you want the workflow to fail when tests fail

## Report Retention

- HTML reports are stored as GitHub Actions artifacts for 30 days
- You can download them directly from the Actions UI if needed
- Email attachments provide a permanent copy

