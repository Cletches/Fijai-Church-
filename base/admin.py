from django.contrib import admin
from .models import (
    Event, Teaching, Sermon, BlogPost, Gallery, 
    ChurchInfo, ServiceTime, NewsletterSubscriber, NewsletterIssue
)




@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'start_time', 'featured', 'from_google_calendar']
    list_filter = ['event_type', 'date', 'featured', 'from_google_calendar']
    list_editable = ['featured']
    ordering = ['-date', 'start_time']
    readonly_fields = ['google_calendar_id', 'google_calendar_link', 'from_google_calendar', 'last_synced']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'event_type', 'featured')
        }),
        ('Date & Time', {
            'fields': ('date', 'start_time', 'end_time', 'recurring')
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Google Calendar Integration', {
            'fields': ('from_google_calendar', 'google_calendar_id', 'google_calendar_link', 'last_synced'),
            'classes': ('collapse',),
            'description': 'These fields are automatically managed by Google Calendar sync'
        }),
    )
    
    actions = ['sync_with_google_calendar']
    
    def sync_with_google_calendar(self, request, queryset):
        from base.calendar_service import sync_google_calendar_events
        try:
            synced_count = sync_google_calendar_events()
            self.message_user(request, f"Successfully synced {synced_count} events from Google Calendar")
        except Exception as e:
            self.message_user(request, f"Error syncing calendar: {str(e)}", level='ERROR')
    
    sync_with_google_calendar.short_description = "Sync events from Google Calendar"


@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'date_created', 'series', 'category', 'featured', 'has_pdf']
    list_filter = ['teacher', 'date_created', 'series', 'category', 'featured']
    list_editable = ['featured']
    ordering = ['-date_created']
    search_fields = ['title', 'teacher', 'description', 'scripture_reference']
    date_hierarchy = 'date_created'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'teacher', 'date_created', 'featured')
        }),
        ('Content', {
            'fields': ('description', 'scripture_reference', 'pdf_file')
        }),
        ('Organization', {
            'fields': ('series', 'category'),
            'classes': ('collapse',)
        }),
    )
    
    def has_pdf(self, obj):
        return bool(obj.pdf_file)
    has_pdf.boolean = True
    has_pdf.short_description = 'Has PDF'


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'date_preached', 'series']
    list_filter = ['speaker', 'date_preached', 'series']
    ordering = ['-date_preached']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'featured', 'published']
    list_filter = ['author', 'created_at', 'featured', 'published']
    list_editable = ['featured', 'published']
    ordering = ['-created_at']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_taken', 'featured']
    list_filter = ['date_taken', 'featured']
    list_editable = ['featured']
    ordering = ['-date_taken']


@admin.register(ChurchInfo)
class ChurchInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'has_map']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'phone', 'email', 'address')
        }),
        ('About', {
            'fields': ('mission_statement', 'statement_of_faith', 'history'),
            'classes': ('collapse',)
        }),
        ('Map & Location', {
            'fields': ('map_embed_url',),
            'description': 'To add a Google Map: 1) Go to Google Maps, 2) Search for your church, 3) Click Share, 4) Click Embed a map, 5) Copy the src URL from the iframe code and paste it here.'
        }),
        ('Social Media', {
            'fields': ('facebook_url',),
            'classes': ('collapse',)
        }),
    )
    
    def has_map(self, obj):
        return bool(obj.map_embed_url)
    has_map.boolean = True
    has_map.short_description = 'Has Map'


@admin.register(ServiceTime)
class ServiceTimeAdmin(admin.ModelAdmin):
    list_display = ['day', 'service_name', 'start_time', 'end_time']
    list_filter = ['day']
    ordering = ['day', 'start_time']




@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'active']
    list_filter = ['subscribed_at', 'active']
    list_editable = ['active']
    ordering = ['-subscribed_at']
    search_fields = ['email']
    
    actions = ['export_emails', 'activate_subscribers', 'deactivate_subscribers']
    
    def export_emails(self, request, queryset):
        emails = list(queryset.values_list('email', flat=True))
        email_list = ', '.join(emails)
        self.message_user(request, f"Exported {len(emails)} emails: {email_list}")
    export_emails.short_description = "Export selected email addresses"
    
    def activate_subscribers(self, request, queryset):
        count = queryset.update(active=True)
        self.message_user(request, f"Activated {count} subscribers")
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        count = queryset.update(active=False)
        self.message_user(request, f"Deactivated {count} subscribers")
    deactivate_subscribers.short_description = "Deactivate selected subscribers"


@admin.register(NewsletterIssue)
class NewsletterIssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'status', 'author', 'recipients_count', 'sent_count', 'created_at', 'sent_date']
    list_filter = ['status', 'author', 'created_at', 'sent_date']
    list_editable = ['status']
    ordering = ['-created_at']
    search_fields = ['title', 'subject', 'content']
    
    fieldsets = (
        ('Newsletter Content', {
            'fields': ('title', 'subject', 'content', 'author')
        }),
        ('Scheduling & Status', {
            'fields': ('status', 'scheduled_date'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('recipients_count', 'sent_count', 'created_at', 'sent_date'),
            'classes': ('collapse',),
            'description': 'These fields are automatically updated when newsletters are sent'
        }),
    )
    
    readonly_fields = ['created_at', 'sent_date', 'recipients_count', 'sent_count']
    
    actions = ['send_newsletter', 'duplicate_newsletter', 'preview_newsletter']
    
    def send_newsletter(self, request, queryset):
        from .newsletter_service import send_newsletter_issue
        
        sent_count = 0
        for newsletter in queryset:
            if newsletter.can_send():
                try:
                    result = send_newsletter_issue(newsletter)
                    if result['success']:
                        sent_count += 1
                        self.message_user(request, f"Successfully sent '{newsletter.title}' to {result['sent_count']} subscribers")
                    else:
                        self.message_user(request, f"Failed to send '{newsletter.title}': {result['error']}", level='ERROR')
                except Exception as e:
                    self.message_user(request, f"Error sending '{newsletter.title}': {str(e)}", level='ERROR')
            else:
                self.message_user(request, f"Cannot send '{newsletter.title}' - check status and content", level='WARNING')
        
        if sent_count > 0:
            self.message_user(request, f"Sent {sent_count} newsletters successfully")
    
    send_newsletter.short_description = "Send selected newsletters"
    
    def duplicate_newsletter(self, request, queryset):
        for newsletter in queryset:
            newsletter.pk = None
            newsletter.title = f"Copy of {newsletter.title}"
            newsletter.status = 'draft'
            newsletter.sent_date = None
            newsletter.recipients_count = 0
            newsletter.sent_count = 0
            newsletter.save()
        
        self.message_user(request, f"Duplicated {queryset.count()} newsletters as drafts")
    
    duplicate_newsletter.short_description = "Duplicate selected newsletters"
    
    def preview_newsletter(self, request, queryset):
        # This could be enhanced to show a preview
        for newsletter in queryset:
            self.message_user(request, f"Preview for '{newsletter.title}': {newsletter.content[:100]}...")
    
    preview_newsletter.short_description = "Preview selected newsletters"
