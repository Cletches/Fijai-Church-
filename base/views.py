from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from .models import (
    Event, Teaching, Sermon, BlogPost, Gallery, 
    ChurchInfo, ServiceTime, NewsletterSubscriber, NewsletterIssue
)
from .calendar_service import GoogleCalendarService


def home(request):
    church_info = ChurchInfo.objects.first()
    service_times = ServiceTime.objects.all()
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date())[:3]
    latest_teachings = Teaching.objects.all()[:3]
    featured_gallery = Gallery.objects.filter(featured=True)[:6]
    latest_blog_posts = BlogPost.objects.filter(published=True)[:3]
    
    # Try to get recent Google Calendar events if available
    google_events = []
    try:
        calendar_service = GoogleCalendarService()
        google_events = calendar_service.get_upcoming_events(3)
    except Exception as e:
        print(f"Could not fetch Google Calendar events: {e}")
    
    context = {
        'church_info': church_info,
        'service_times': service_times,
        'upcoming_events': upcoming_events,
        'latest_teachings': latest_teachings,
        'featured_gallery': featured_gallery,
        'latest_blog_posts': latest_blog_posts,
        'google_events': google_events,
    }
    return render(request, 'home.html', context)


def about(request):
    church_info = ChurchInfo.objects.first()
    context = {
        'church_info': church_info,
    }
    return render(request, 'about.html', context)


def events(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date())
    past_events = Event.objects.filter(date__lt=timezone.now().date())[:10]
    
    # Get Google Calendar events
    google_events = []
    try:
        calendar_service = GoogleCalendarService()
        google_events = calendar_service.get_upcoming_events(10)
    except Exception as e:
        print(f"Could not fetch Google Calendar events: {e}")
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'google_events': google_events,
    }
    return render(request, 'events.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {'event': event}
    return render(request, 'event_detail.html', context)


def teachings(request):
    teachings_list = Teaching.objects.all()
    series_list = Teaching.objects.values_list('series', flat=True).distinct()
    series_list = [s for s in series_list if s]
    categories_list = Teaching.objects.values_list('category', flat=True).distinct()
    categories_list = [c for c in categories_list if c]
    
    context = {
        'teachings': teachings_list,
        'series_list': series_list,
        'categories_list': categories_list,
    }
    return render(request, 'teachings.html', context)


def teaching_detail(request, teaching_id):
    teaching = get_object_or_404(Teaching, id=teaching_id)
    context = {'teaching': teaching}
    return render(request, 'teaching_detail.html', context)


# Keep sermon views for backward compatibility
def sermons(request):
    sermons_list = Sermon.objects.all()
    series_list = Sermon.objects.values_list('series', flat=True).distinct()
    series_list = [s for s in series_list if s]
    
    context = {
        'sermons': sermons_list,
        'series_list': series_list,
    }
    return render(request, 'sermons.html', context)


def sermon_detail(request, sermon_id):
    sermon = get_object_or_404(Sermon, id=sermon_id)
    context = {'sermon': sermon}
    return render(request, 'sermon_detail.html', context)


def gallery(request):
    gallery_images = Gallery.objects.all()
    context = {'gallery_images': gallery_images}
    return render(request, 'gallery.html', context)




def blog(request):
    blog_posts = BlogPost.objects.filter(published=True)
    context = {'blog_posts': blog_posts}
    return render(request, 'blog.html', context)


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, published=True)
    context = {'post': post}
    return render(request, 'blog_detail.html', context)


def contact(request):
    from django.core.mail import send_mail
    from django.contrib import messages
    from django.conf import settings
    from django.shortcuts import redirect
    
    church_info = ChurchInfo.objects.first()
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '').strip()
            
            print(f"Contact form submission: {name}, {email}, {subject}")  # Debug log
            
            # Validate required fields
            if not name or not email or not subject or not message:
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'contact.html', {'church_info': church_info})
            
            # Prepare email content
            email_subject = f"Contact Form: {subject} - From {name}"
            email_message = f"""
New contact form submission from Fijai Church of Christ website:

Name: {name}
Email: {email}
Phone: {phone if phone else 'Not provided'}
Subject: {subject}

Message:
{message}

---
This message was sent from the church website contact form.
To reply to {name}, send your response to: {email}

Website: {request.build_absolute_uri('/')}
Submitted: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}
            """
            
            # Send email
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            print(f"Email sent successfully to {settings.CONTACT_EMAIL}")  # Debug log
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            
            # Redirect to clear form data after successful submission
            return redirect('contact')
            
        except Exception as e:
            print(f"Email sending error: {e}")  # Debug log
            messages.error(request, f'Sorry, there was an error sending your message: {str(e)}. Please try again or contact us directly.')
    
    context = {'church_info': church_info}
    return render(request, 'contact.html', context)


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            newsletter, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'active': True}
            )
            if created:
                return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
            else:
                return JsonResponse({'success': False, 'message': 'Email already subscribed.'})
        return JsonResponse({'success': False, 'message': 'Please provide a valid email.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def download_pdf(request, teaching_id):
    """Secure PDF download with logging"""
    teaching = get_object_or_404(Teaching, id=teaching_id)
    
    if not teaching.pdf_file:
        return HttpResponse("PDF not found", status=404)
    
    try:
        from django.http import FileResponse
        import os
        
        file_path = teaching.pdf_file.path
        if os.path.exists(file_path):
            # Log the download (optional)
            print(f"PDF downloaded: {teaching.title} by {request.META.get('REMOTE_ADDR', 'Unknown IP')}")
            
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{teaching.title}.pdf"'
            return response
        else:
            return HttpResponse("PDF file not found on server", status=404)
            
    except Exception as e:
        print(f"Error serving PDF: {e}")
        return HttpResponse("Error serving PDF", status=500)