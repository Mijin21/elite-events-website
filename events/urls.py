from django.urls import path
from . import views


urlpatterns = [
    # ── Public Pages ──────────────────────────────────────────
    path('', views.landing, name='home'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('our-works/', views.ourworks, name='ourworks'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('booking/', views.booking, name='booking'),
    path('logout/', views.user_logout, name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    # ── Upcoming Events API ───────────────────────────────────────
    path('api/upcoming-events/', views.api_upcoming_events_list, name='api_upcoming_events_list'),
    path('api/upcoming-events/create/', views.api_upcoming_event_create, name='api_upcoming_event_create'),
    path('api/upcoming-events/<int:pk>/', views.api_upcoming_event_detail, name='api_upcoming_event_detail'),
    path('api/upcoming-events/<int:pk>/update/', views.api_upcoming_event_update, name='api_upcoming_event_update'),
    path('api/upcoming-events/<int:pk>/delete/', views.api_upcoming_event_delete, name='api_upcoming_event_delete'),
]