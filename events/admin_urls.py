from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # ── Admin Pages ───────────────────────────────────────────
    path('', views.admin_dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),

    # ── Dashboard Stats ───────────────────────────────────────
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),

    # ── Bookings ──────────────────────────────────────────────
    path('api/bookings/', views.api_bookings_list, name='api_bookings_list'),
    path('api/bookings/<int:pk>/', views.api_booking_detail, name='api_booking_detail'),
    path('api/bookings/<int:pk>/status/', views.api_booking_status, name='api_booking_status'),
    path('api/bookings/<int:pk>/delete/', views.api_booking_delete, name='api_booking_delete'),

    # ── Users ─────────────────────────────────────────────────
    path('api/users/', views.api_users_list, name='api_users_list'),
    path('api/users/<int:pk>/toggle/', views.api_user_toggle, name='api_user_toggle'),
    path('api/users/<int:pk>/delete/', views.api_user_delete, name='api_user_delete'),

    # ── Enquiries ─────────────────────────────────────────────
    path('api/enquiries/', views.api_enquiries_list, name='api_enquiries_list'),
    path('api/enquiries/<int:pk>/', views.api_enquiry_detail, name='api_enquiry_detail'),
    path('api/enquiries/<int:pk>/read/', views.api_enquiry_read, name='api_enquiry_read'),
    path('api/enquiries/<int:pk>/delete/', views.api_enquiry_delete, name='api_enquiry_delete'),

    # ── Content ───────────────────────────────────────────────
    path('api/content/', views.api_content_get, name='api_content_get'),
    path('api/content/save/', views.api_content_save, name='api_content_save'),

    # ── Images ────────────────────────────────────────────────
    path('api/images/', views.api_images_list, name='api_images_list'),
    path('api/images/upload/', views.api_images_upload, name='api_images_upload'),
    path('api/images/<int:pk>/delete/', views.api_image_delete, name='api_image_delete'),

    # ── Services ──────────────────────────────────────────────
    path('api/services/', views.api_services_list, name='api_services_list'),
    path('api/services/create/', views.api_service_create, name='api_service_create'),
    path('api/services/<int:pk>/', views.api_service_detail, name='api_service_detail'),
    path('api/services/<int:pk>/update/', views.api_service_update, name='api_service_update'),
    path('api/services/<int:pk>/delete/', views.api_service_delete, name='api_service_delete'),

    # ── Portfolio ─────────────────────────────────────────────
    path('api/portfolio/', views.api_portfolio_list, name='api_portfolio_list'),
    path('api/portfolio/create/', views.api_portfolio_create, name='api_portfolio_create'),
    path('api/portfolio/<int:pk>/', views.api_portfolio_detail, name='api_portfolio_detail'),
    path('api/portfolio/<int:pk>/update/', views.api_portfolio_update, name='api_portfolio_update'),
    path('api/portfolio/<int:pk>/delete/', views.api_portfolio_delete, name='api_portfolio_delete'),

    # ── Testimonials ──────────────────────────────────────────
    path('api/testimonials/', views.api_testimonials_list, name='api_testimonials_list'),
    path('api/testimonials/create/', views.api_testimonial_create, name='api_testimonial_create'),
    path('api/testimonials/<int:pk>/', views.api_testimonial_detail, name='api_testimonial_detail'),
    path('api/testimonials/<int:pk>/update/', views.api_testimonial_update, name='api_testimonial_update'),
    path('api/testimonials/<int:pk>/delete/', views.api_testimonial_delete, name='api_testimonial_delete'),

    # ── Team ──────────────────────────────────────────────────
    path('api/team/', views.api_team_list, name='api_team_list'),
    path('api/team/create/', views.api_team_create, name='api_team_create'),
    path('api/team/<int:pk>/', views.api_team_detail, name='api_team_detail'),
    path('api/team/<int:pk>/update/', views.api_team_update, name='api_team_update'),
    path('api/team/<int:pk>/delete/', views.api_team_delete, name='api_team_delete'),

    # ── Settings ──────────────────────────────────────────────
    path('api/settings/', views.api_settings_get, name='api_settings_get'),
    path('api/settings/save/', views.api_settings_save, name='api_settings_save'),
    # ── Clients ───────────────────────────────────────────────────
    path('api/clients/', views.api_clients_list, name='api_clients_list'),
    path('api/clients/create/', views.api_client_create, name='api_client_create'),
    path('api/clients/<int:pk>/', views.api_client_detail, name='api_client_detail'),
    path('api/clients/<int:pk>/update/', views.api_client_update, name='api_client_update'),
    path('api/clients/<int:pk>/delete/', views.api_client_delete, name='api_client_delete'),
]