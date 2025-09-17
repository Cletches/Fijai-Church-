from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('teachings/', views.teachings, name='teachings'),
    path('teachings/<int:teaching_id>/', views.teaching_detail, name='teaching_detail'),
    path('teachings/<int:teaching_id>/download/', views.download_pdf, name='download_pdf'),
    path('sermons/', views.sermons, name='sermons'),
    path('sermons/<int:sermon_id>/', views.sermon_detail, name='sermon_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('resources/', views.teachings, name='resources'),  # Link resources to teachings
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
]