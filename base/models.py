from django.db import models
from django.utils import timezone




class Event(models.Model):
    EVENT_TYPES = [
        ('service', 'Service'),
        ('bible_study', 'Bible Study'),
        ('community', 'Community Event'),
        ('special', 'Special Program'),
        ('meeting', 'Meeting'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='service')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    recurring = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    
    # Google Calendar Integration fields
    google_calendar_id = models.CharField(max_length=500, blank=True, null=True, unique=True)
    google_calendar_link = models.URLField(blank=True, null=True)
    from_google_calendar = models.BooleanField(default=False)
    last_synced = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    @property
    def is_from_google_calendar(self):
        return self.from_google_calendar and self.google_calendar_id


class Teaching(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.CharField(max_length=100)
    scripture_reference = models.CharField(max_length=100, blank=True)
    date_created = models.DateField()
    pdf_file = models.FileField(upload_to='teachings/pdfs/', blank=True, null=True)
    description = models.TextField(blank=True)
    series = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, blank=True, help_text="e.g., Bible Study, Sermon Notes, Devotional")
    featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_created']
        verbose_name = "Teaching"
        verbose_name_plural = "Teachings"
    
    def __str__(self):
        return f"{self.title} - {self.date_created}"


# Keep Sermon model for backward compatibility but mark as deprecated
class Sermon(models.Model):
    title = models.CharField(max_length=200)
    speaker = models.CharField(max_length=100)
    scripture_reference = models.CharField(max_length=100, blank=True)
    date_preached = models.DateField()
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    series = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-date_preached']
    
    def __str__(self):
        return f"{self.title} - {self.date_preached}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    date_taken = models.DateField(blank=True, null=True)
    event_related = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_taken']
        verbose_name_plural = "Gallery Images"
    
    def __str__(self):
        return self.title


class ChurchInfo(models.Model):
    name = models.CharField(max_length=200, default="Fijai Church Of Christ")
    mission_statement = models.TextField()
    statement_of_faith = models.TextField()
    history = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    map_embed_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Church Information"
        verbose_name_plural = "Church Information"
    
    def __str__(self):
        return self.name


class ServiceTime(models.Model):
    DAYS_OF_WEEK = [
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    service_name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.get_day_display()} - {self.service_name}"




class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        
    def __str__(self):
        return self.email


class NewsletterIssue(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
    ]
    
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200, help_text="Email subject line")
    content = models.TextField(help_text="Newsletter content (HTML supported)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateTimeField(blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    author = models.CharField(max_length=100, default="Church Admin")
    
    # Statistics
    recipients_count = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Newsletter Issue"
        verbose_name_plural = "Newsletter Issues"
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def get_active_subscribers(self):
        return NewsletterSubscriber.objects.filter(active=True)
    
    def can_send(self):
        return self.status in ['draft', 'scheduled'] and self.content.strip()
    
    def mark_as_sent(self):
        self.status = 'sent'
        self.sent_date = timezone.now()
        self.save()
