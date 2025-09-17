# Google Calendar Integration Setup

This guide will help you set up Google Calendar integration for your church website using the email `fijaichurchofchrist@gmail.com`.

## Setup Steps

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Name it something like "Fijai Church Calendar"

### 2. Enable Google Calendar API
1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Calendar API"
3. Click on it and press "Enable"

### 3. Create Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in app name: "Fijai Church Website"
   - Add your email as a developer email
   - Add scopes: `../auth/calendar.readonly`
4. For Application type, choose "Desktop application"
5. Name it "Church Website Calendar Access"
6. Download the JSON file

### 4. Setup Credentials File
1. Rename the downloaded JSON file to `credentials.json`
2. Place it in your project root directory: `/Users/felixofori/Desktop/churchwebsite/credentials.json`

### 5. Configure Calendar Access
1. Make sure the Google Calendar you want to sync is accessible by `fijaichurchofchrist@gmail.com`
2. If using a different calendar, share it with this email address with "See all event details" permission

### 6. First Time Setup
Run the sync command to authenticate:
```bash
python manage.py sync_calendar --verbose
```

This will:
- Open a browser window for authentication
- Ask you to sign in with `fijaichurchofchrist@gmail.com`
- Grant permission to read calendar events
- Save the authentication token for future use

### 7. Test the Integration
After authentication, you can:
- Visit your website to see Google Calendar events
- Use the Django admin to sync events manually
- Set up automated sync (see below)

## Usage

### Manual Sync
```bash
python manage.py sync_calendar --verbose
```

### Django Admin Sync
1. Go to Django admin `/admin/`
2. Navigate to Events
3. Select events and use "Sync events from Google Calendar" action

### Automated Sync (Optional)
Add to your server's crontab to sync every hour:
```bash
0 * * * * cd /path/to/churchwebsite && python manage.py sync_calendar
```

## Features

### Home Page Integration
- Shows upcoming Google Calendar events alongside local events
- Distinguishes Google Calendar events with blue styling and Google icon
- Direct links to view events in Google Calendar

### Events Page Integration
- Displays both local and Google Calendar events
- Google Calendar events have special blue gradient styling
- Links to view events in Google Calendar

### Admin Integration
- Events synced from Google Calendar are marked as such
- Read-only Google Calendar fields
- Bulk sync action available

## Troubleshooting

### Authentication Issues
- Delete `token.json` and re-run the sync command
- Ensure the correct Google account has calendar access
- Check that the calendar is shared properly

### Calendar Not Found
- Verify the calendar email `fijaichurchofchrist@gmail.com` is correct
- Ensure the calendar exists and is accessible
- Check calendar sharing permissions

### No Events Showing
- Verify events exist in the Google Calendar
- Check that events are in the future
- Run sync command with `--verbose` flag for detailed output

## Security Notes
- Keep `credentials.json` and `token.json` secure
- Add them to `.gitignore` to avoid committing to version control
- The integration only reads calendar data (read-only access)