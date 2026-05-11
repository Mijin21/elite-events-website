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
]