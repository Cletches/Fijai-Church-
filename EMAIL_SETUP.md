# Email Setup Guide for Contact Form

This guide explains how to configure email sending for the church website contact form.

## Current Configuration

The contact form is set up to send emails to `fijaichurchofchrist@gmail.com` when users submit the contact form.

### Development Mode (Current)
- Emails are displayed in the console/terminal
- No actual emails are sent
- Good for testing the functionality

### Production Mode Setup

To enable actual email sending in production, follow these steps:

## 1. Gmail App Password Setup

Since the website will send emails through Gmail, you need to create an App Password:

1. **Sign in to Gmail**: Go to [Gmail](https://gmail.com) and sign in to `fijaichurchofchrist@gmail.com`

2. **Enable 2-Factor Authentication**:
   - Go to Google Account settings
   - Navigate to Security
   - Enable 2-Factor Authentication if not already enabled

3. **Create App Password**:
   - In Google Account settings, go to Security
   - Under "2-Step Verification", click on "App passwords"
   - Select "Mail" as the app and "Other" as the device
   - Name it "Church Website"
   - Copy the generated 16-character password

## 2. Update Django Settings

In `/Users/felixofori/Desktop/churchwebsite/churchwebsite/settings.py`:

1. **Comment out the development email backend**:
   ```python
   # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

2. **Uncomment and configure the production email settings**:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'fijaichurchofchrist@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-16-character-app-password'  # Paste the app password here
   DEFAULT_FROM_EMAIL = 'fijaichurchofchrist@gmail.com'
   ```

## 3. Security Considerations

- **Never commit passwords to version control**
- **Use environment variables for production**:
  ```python
  import os
  EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
  ```

## 4. Testing

1. **Test in development**:
   - Fill out the contact form
   - Check the terminal/console for email output
   
2. **Test in production**:
   - Fill out the contact form
   - Check `fijaichurchofchrist@gmail.com` for received emails

## 5. Features

### Current Contact Form Features:
- **Required fields**: Name, Email, Subject, Message
- **Optional field**: Phone number
- **Subject categories**:
  - General Inquiry
  - Prayer Request
  - Planning to Visit
  - Ministry Information
  - Bible Study Question
  - Event Information
  - Other

### Email Features:
- **Automatic subject line**: "Contact Form: [Subject] - From [Name]"
- **Structured email content** with all form data
- **Reply-to field**: Set to sender's email for easy replies
- **Timestamp**: Shows when the message was submitted
- **Website link**: Includes link back to the website

### User Experience:
- **Success message**: Confirms email was sent
- **Error handling**: Shows friendly error messages
- **Form validation**: Prevents submission of incomplete forms
- **Form persistence**: Retains form data if there's an error

## 6. Troubleshooting

### Common Issues:

1. **"SMTPAuthenticationError"**:
   - Check that 2FA is enabled on the Gmail account
   - Verify the App Password is correct
   - Ensure you're using the App Password, not the regular password

2. **"SMTPConnectTimeoutError"**:
   - Check internet connection
   - Verify Gmail SMTP settings
   - Try port 465 with EMAIL_USE_SSL = True instead of TLS

3. **Emails not being received**:
   - Check spam/junk folder
   - Verify the recipient email address
   - Test with a different recipient email

4. **Form validation errors**:
   - Ensure all required fields are filled
   - Check that email format is valid

## 7. Alternative Email Providers

If Gmail doesn't work, you can use other email providers:

### Microsoft Outlook/Hotmail:
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Yahoo Mail:
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

## 8. Advanced Configuration

For production environments, consider:

- **Environment variables** for sensitive data
- **Email logging** for monitoring
- **Rate limiting** to prevent spam
- **Email templates** for better formatting
- **Backup email addresses** in case primary fails

## Support

If you encounter issues with email setup, the contact form will still work in development mode (console output) for testing purposes.