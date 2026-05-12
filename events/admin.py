from django.contrib import admin
from .models import (
    ContactEnquiry, EventBooking, Service, PortfolioItem,
    Testimonial, TeamMember, SiteImage, SiteContent, SiteSetting, Client,
    UpcomingEvent
)
@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email')

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'event_type', 'event_date', 'booked_at')
    search_fields = ('name', 'email')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_partner', 'is_active', 'order')
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_active')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active')

@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'uploaded_at')

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'updated_at')

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'updated_at')
@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'price_display', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'category')
    list_filter = ('category', 'is_active')