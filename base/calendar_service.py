import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarService:
    def __init__(self):
        self.calendar_id = 'fijaichurchofchrist@gmail.com'
        self.service = None
        
    def authenticate(self):
        """Authenticate and create calendar service"""
        creds = None
        token_path = os.path.join(settings.BASE_DIR, 'token.json')
        credentials_path = os.path.join(settings.BASE_DIR, 'credentials.json')
        
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    return False
            else:
                if not os.path.exists(credentials_path):
                    print("credentials.json file not found. Please add Google Calendar credentials.")
                    return False
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
                
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            return True
        except HttpError as error:
            print(f'An error occurred: {error}')
            return False
    
    def get_upcoming_events(self, max_results=10):
        """Fetch upcoming events from Google Calendar"""
        if not self.service and not self.authenticate():
            return []
            
        try:
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                # Extract event data
                event_data = {
                    'google_id': event.get('id'),
                    'title': event.get('summary', 'No Title'),
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'start_time': None,
                    'end_time': None,
                    'date': None,
                    'is_all_day': False,
                    'html_link': event.get('htmlLink', ''),
                }
                
                # Handle start time
                start = event.get('start', {})
                if 'dateTime' in start:
                    # Timed event
                    start_datetime = datetime.datetime.fromisoformat(
                        start['dateTime'].replace('Z', '+00:00')
                    )
                    event_data['start_time'] = start_datetime.time()
                    event_data['date'] = start_datetime.date()
                elif 'date' in start:
                    # All-day event
                    event_data['date'] = datetime.datetime.fromisoformat(start['date']).date()
                    event_data['is_all_day'] = True
                
                # Handle end time
                end = event.get('end', {})
                if 'dateTime' in end:
                    end_datetime = datetime.datetime.fromisoformat(
                        end['dateTime'].replace('Z', '+00:00')
                    )
                    event_data['end_time'] = end_datetime.time()
                elif 'date' in end:
                    # For all-day events, end date is exclusive, so subtract 1 day
                    end_date = datetime.datetime.fromisoformat(end['date']).date()
                    event_data['end_date'] = end_date
                
                formatted_events.append(event_data)
                
            return formatted_events
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def get_calendar_info(self):
        """Get calendar information"""
        if not self.service and not self.authenticate():
            return None
            
        try:
            calendar = self.service.calendars().get(calendarId=self.calendar_id).execute()
            return {
                'name': calendar.get('summary', ''),
                'description': calendar.get('description', ''),
                'timezone': calendar.get('timeZone', ''),
            }
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None


def sync_google_calendar_events():
    """Sync Google Calendar events with local database"""
    from .models import Event
    
    calendar_service = GoogleCalendarService()
    google_events = calendar_service.get_upcoming_events(50)  # Get more events for sync
    
    synced_count = 0
    
    for event_data in google_events:
        # Check if event already exists
        existing_event = Event.objects.filter(google_calendar_id=event_data['google_id']).first()
        
        if existing_event:
            # Update existing event
            existing_event.title = event_data['title']
            existing_event.description = event_data['description']
            existing_event.location = event_data['location']
            existing_event.date = event_data['date']
            if event_data['start_time']:
                existing_event.start_time = event_data['start_time']
            if event_data['end_time']:
                existing_event.end_time = event_data['end_time']
            existing_event.google_calendar_link = event_data['html_link']
            existing_event.save()
        else:
            # Create new event
            Event.objects.create(
                title=event_data['title'],
                description=event_data['description'],
                location=event_data['location'],
                date=event_data['date'],
                start_time=event_data['start_time'] or datetime.time(9, 0),  # Default time
                end_time=event_data['end_time'],
                event_type='service',  # Default type
                google_calendar_id=event_data['google_id'],
                google_calendar_link=event_data['html_link'],
                from_google_calendar=True
            )
        
        synced_count += 1
    
    return synced_count