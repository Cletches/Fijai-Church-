from django.core.mail import send_mail
from django.template import Template, Context
from django.conf import settings
from django.utils import timezone
from .models import NewsletterSubscriber, NewsletterIssue


def get_newsletter_template():
    """Get the HTML template for newsletters"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            max-width: 600px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header { 
            background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%); 
            color: white; 
            padding: 30px 20px; 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .header h1 { 
            margin: 0; 
            font-size: 28px; 
        }
        .content { 
            padding: 20px; 
            background: #f9f9f9; 
            border-radius: 8px; 
            margin-bottom: 30px; 
        }
        .footer { 
            text-align: center; 
            padding: 20px; 
            font-size: 12px; 
            color: #666; 
            border-top: 1px solid #ddd; 
        }
        .unsubscribe { 
            color: #666; 
            text-decoration: none; 
        }
        a { 
            color: #3b82f6; 
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Fijai Church Of Christ</h1>
        <p>{{ title }}</p>
    </div>
    
    <div class="content">
        {{ content }}
    </div>
    
    <div class="footer">
        <p>This newsletter was sent by Fijai Church Of Christ</p>
        <p>I19 Nana Owuo St, Takoradi, Ghana</p>
        <p>Email: fijaichurchofchrist@gmail.com | Phone: +233 24 323 2616</p>
        <p><a href="{{ unsubscribe_url }}" class="unsubscribe">Unsubscribe from this newsletter</a></p>
    </div>
</body>
</html>
    """


def send_newsletter_issue(newsletter_issue):
    """Send a newsletter issue to all active subscribers"""
    try:
        # Get all active subscribers
        subscribers = NewsletterSubscriber.objects.filter(active=True)
        
        if not subscribers.exists():
            return {
                'success': False,
                'error': 'No active subscribers found',
                'sent_count': 0
            }
        
        # Prepare newsletter content
        template = Template(get_newsletter_template())
        
        sent_count = 0
        failed_emails = []
        
        for subscriber in subscribers:
            try:
                # Create context for each subscriber
                context = Context({
                    'title': newsletter_issue.title,
                    'content': newsletter_issue.content,
                    'subscriber_email': subscriber.email,
                    'unsubscribe_url': f"mailto:fijaichurchofchrist@gmail.com?subject=Unsubscribe&body=Please unsubscribe {subscriber.email} from the newsletter"
                })
                
                # Render the template
                html_content = template.render(context)
                
                # Send email
                send_mail(
                    subject=newsletter_issue.subject,
                    message=f"Newsletter: {newsletter_issue.title}\n\n{newsletter_issue.content}\n\nTo unsubscribe, reply to this email with 'UNSUBSCRIBE' in the subject.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscriber.email],
                    html_message=html_content,
                    fail_silently=False,
                )
                
                sent_count += 1
                print(f"Newsletter sent to {subscriber.email}")
                
            except Exception as e:
                failed_emails.append(f"{subscriber.email}: {str(e)}")
                print(f"Failed to send to {subscriber.email}: {e}")
        
        # Update newsletter statistics
        newsletter_issue.recipients_count = subscribers.count()
        newsletter_issue.sent_count = sent_count
        newsletter_issue.mark_as_sent()
        
        result = {
            'success': True,
            'sent_count': sent_count,
            'total_subscribers': subscribers.count(),
            'failed_emails': failed_emails
        }
        
        if failed_emails:
            result['error'] = f"Failed to send to {len(failed_emails)} emails: {'; '.join(failed_emails[:3])}"
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'sent_count': 0
        }


def send_test_newsletter(newsletter_issue, test_email):
    """Send a test newsletter to a specific email address"""
    try:
        template = Template(get_newsletter_template())
        
        context = Context({
            'title': f"TEST: {newsletter_issue.title}",
            'content': newsletter_issue.content,
            'subscriber_email': test_email,
            'unsubscribe_url': "#"
        })
        
        html_content = template.render(context)
        
        send_mail(
            subject=f"TEST: {newsletter_issue.subject}",
            message=f"TEST Newsletter: {newsletter_issue.title}\n\n{newsletter_issue.content}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[test_email],
            html_message=html_content,
            fail_silently=False,
        )
        
        return {'success': True, 'message': f'Test newsletter sent to {test_email}'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_newsletter_stats():
    """Get newsletter statistics"""
    return {
        'total_subscribers': NewsletterSubscriber.objects.filter(active=True).count(),
        'total_newsletters': NewsletterIssue.objects.count(),
        'sent_newsletters': NewsletterIssue.objects.filter(status='sent').count(),
        'draft_newsletters': NewsletterIssue.objects.filter(status='draft').count(),
    }