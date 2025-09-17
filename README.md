# Fijai Church Of Christ Website

A modern, responsive Django web application for Fijai Church Of Christ located in Takoradi, Ghana. This website serves as the digital presence for the church, providing information about services, events, teachings, and enabling community engagement.

## Features

### <à Core Pages
- **Home Page**: Welcome message, upcoming events, latest teachings, and service times
- **About Us**: Church mission, statement of faith, history, and leadership information
- **Contact**: Contact form, location map, and church contact details
- **Events**: Upcoming and past church events with Google Calendar integration
- **Teachings**: Bible study materials with PDF downloads
- **Gallery**: Photo gallery of church events and activities
- **Blog**: Church news and announcements

### =ç Newsletter System
- **Subscriber Management**: Email subscription and management system
- **Newsletter Creation**: Rich text newsletter composition with HTML templates
- **Bulk Sending**: Send newsletters to all active subscribers
- **Statistics Tracking**: Monitor newsletter performance and subscriber counts
- **Professional Templates**: Branded email templates with church styling

### =Å Google Calendar Integration
- **Event Synchronization**: Automatic sync with church Google Calendar
- **Upcoming Events**: Display of upcoming events from Google Calendar
- **Event Management**: Admin interface for managing both local and synced events

### =Ú Teaching Resources
- **PDF Upload/Download**: Secure PDF file management for Bible teachings
- **Teaching Categories**: Organized by series and categories
- **Featured Content**: Highlight important teachings and resources

### =ñ Modern Features
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS
- **Contact Form**: Email contact form with validation
- **Newsletter Signup**: Easy subscription to church newsletters
- **Social Media Integration**: Facebook integration and social links

## Technology Stack

- **Backend**: Django 5.0.8 (Python web framework)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (default, easily configurable for PostgreSQL/MySQL)
- **Email**: Gmail SMTP integration
- **File Storage**: Local file system for media files
- **External APIs**: Google Calendar API for event management

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd churchwebsite
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_EMAIL=fijaichurchofchrist@gmail.com

# Google Calendar (Optional)
GOOGLE_CALENDAR_ID=your-calendar-id

# Django Secret Key
SECRET_KEY=your-secret-key
DEBUG=True
```

### 5. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the website.

## Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/` to manage:

- **Events**: Church events and calendar management
- **Teachings**: Bible study materials and PDF uploads
- **Blog Posts**: Church news and announcements
- **Gallery**: Photo gallery management
- **Newsletter System**: Subscriber and newsletter management
- **Church Information**: Contact details and church information

## Email Configuration

### Gmail Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password for the application
3. Update the `.env` file with your Gmail credentials

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
```

## Google Calendar Integration

### Setup Instructions
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Calendar API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials and save as `credentials.json` in the project root
6. Update the calendar ID in your settings

## Newsletter System Usage

### For Administrators
1. **Add Subscribers**: Go to Admin > Newsletter Subscribers
2. **Create Newsletter**: Go to Admin > Newsletter Issues > Add Newsletter Issue
3. **Send Newsletter**: Select newsletter and use "Send selected newsletters" action
4. **Monitor Statistics**: View subscriber counts and send statistics

### Features
- HTML email templates with church branding
- Subscriber management with active/inactive status
- Newsletter drafts, scheduling, and sending
- Delivery statistics and error tracking
- Unsubscribe functionality

## File Upload Configuration

### Media Files
- **Teachings PDFs**: Stored in `media/teachings/pdfs/`
- **Gallery Images**: Stored in `media/gallery/`
- **Static Files**: CSS, JS, and images in `static/` directory

### File Size Limits
Configure in `settings.py`:
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10MB
```

## Deployment

### Production Settings
1. Set `DEBUG = False` in settings
2. Configure allowed hosts
3. Set up static file serving
4. Configure production database
5. Set up email backend for production
6. Enable HTTPS and security headers

### Environment Variables
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-production-database-url
```

## Church Information

**Fijai Church Of Christ**
- **Address**: I19 Nana Owuo St, Takoradi, Ghana
- **Phone**: +233 24 323 2616
- **Email**: fijaichurchofchrist@gmail.com
- **Facebook**: [Church Facebook Page](https://www.facebook.com/profile.php?id=100070091529316)

### Service Times
- **Sunday Service**: 9:00 AM - 12:00 PM
- **Bible Study**: Tuesday 7:00 PM
- **Prayers/Song Training**: Thursday 7:00 PM

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For technical support or questions about the website, please contact the development team or create an issue in the repository.

## License

This project is designed specifically for Fijai Church Of Christ. Please respect the church's intellectual property and branding.

---

**Built with d for Fijai Church Of Christ Community**