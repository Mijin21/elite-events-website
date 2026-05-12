from django.db import models
from django.contrib.auth.models import User

# ── Already existing ──────────────────────────────────────────

class ContactEnquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"


class EventBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    EVENT_CHOICES = [
        ('wedding', 'Wedding'),
        ('corporate', 'Corporate Event'),
        ('birthday', 'Birthday Party'),
        ('engagement', 'Engagement'),
        ('concert', 'Concert'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    event_date = models.DateField()
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.name} - {self.event_type} - {self.event_date}"


# ── New models ────────────────────────────────────────────────

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)      
    video_id = models.CharField(max_length=50, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100, blank=True)
    quote = models.TextField()
    rating = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SiteImage(models.Model):
    CATEGORY_CHOICES = [
        ('hero', 'Hero / Banner'),
        ('portfolio', 'Portfolio'),
        ('team', 'Team'),
        ('about', 'About'),
        ('gallery', 'Gallery'),
    ]
    name = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='site_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='gallery')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.name}"


class SiteContent(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
class Client(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='clients/', blank=True, null=True)
    is_partner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class UpcomingEvent(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='upcoming_events/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='External image URL (Unsplash etc)')
    price_display = models.CharField(max_length=50, help_text='e.g. ₹5,00,000+')
    event_date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'event_date']

    def __str__(self):
        return f"{self.title} — {self.event_date}"

    def get_image(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400&q=80'