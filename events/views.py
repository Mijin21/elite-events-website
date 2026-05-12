from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ContactEnquiry, EventBooking

def landing(request):
    import json
    from .models import SiteContent, SiteImage, Service, Testimonial

    def get_content(key, default=''):
        try:
            return SiteContent.objects.get(key=key).value
        except SiteContent.DoesNotExist:
            return default

    # Hero slides from Image Manager
    hero_images = SiteImage.objects.filter(category='hero').order_by('-uploaded_at')

    # Gallery images
    gallery_images = SiteImage.objects.filter(category='gallery').order_by('-uploaded_at')

    # Services
    services = Service.objects.filter(is_active=True).order_by('created_at')

    # Testimonials
    testimonials = Testimonial.objects.filter(is_active=True).order_by('created_at')

    # Contact info
    contact_info = {
        'phone': get_content('contact_phone', '+91 98765 43210'),
        'email': get_content('contact_email', 'hello@eliteevents.in'),
        'address': get_content('contact_address', 'Chennai, Tamil Nadu'),
        'whatsapp': get_content('contact_whatsapp', ''),
        'instagram': get_content('contact_instagram', 'https://instagram.com'),
        'facebook': get_content('contact_facebook', 'https://facebook.com'),
    }

    # Hero content
    hero_content = {
        'badge': get_content('hero_badge', 'Luxury Event Specialists'),
        'title_line1': get_content('hero_title_line1', 'We Craft'),
        'title_line2': get_content('hero_title_line2', 'Unforgettable'),
        'title_line3': get_content('hero_title_line3', 'Moments'),
        'subtitle': get_content('hero_subtitle', 'From intimate gatherings to grand celebrations — every detail designed to perfection, every memory crafted with elegance.'),
        'stat1_num': get_content('hero_stat1_num', '500+'),
        'stat1_label': get_content('hero_stat1_label', 'Events Hosted'),
        'stat2_num': get_content('hero_stat2_num', '98%'),
        'stat2_label': get_content('hero_stat2_label', 'Happy Clients'),
        'stat3_num': get_content('hero_stat3_num', '20+'),
        'stat3_label': get_content('hero_stat3_label', 'Years Experience'),
    }

    return render(request, 'events/landing.html', {
        'hero_images': hero_images,
        'gallery_images': gallery_images,
        'services': services,
        'testimonials': testimonials,
        'contact_info': contact_info,
        'hero_content': hero_content,
    })
def about(request):
    import json
    from .models import SiteContent, SiteImage, Client

    def get_content(key, default=''):
        try:
            return SiteContent.objects.get(key=key).value
        except SiteContent.DoesNotExist:
            return default

    # About text
    about_content = {
    'heading': get_content('about_heading', ''),
    'subheading': get_content('about_subheading', ''),
    'body': get_content('about_body', ''),
    'corporart_title': get_content('corporart_title', "CorporART 24'"),
    'corporart_desc': get_content('corporart_desc', ''),
    'corporart_logo': get_content('corporart_logo', ''),
    'welcome_text': get_content('about_welcome_text', ''),
}

    # About image
    about_image = SiteImage.objects.filter(category='about').order_by('-uploaded_at').first()

    # Clients and Partners
    clients = Client.objects.filter(is_active=True, is_partner=False).order_by('order', 'created_at')
    partners = Client.objects.filter(is_active=True, is_partner=True).order_by('order', 'created_at')

    return render(request, 'events/about.html', {
        'about_content': about_content,
        'about_image': about_image,
        'clients': clients,
        'partners': partners,
    })
def team(request):
    from .models import TeamMember
    members = TeamMember.objects.filter(is_active=True).order_by('created_at')
    return render(request, 'events/team.html', {'team_members': members})
def ourworks(request):
    import json
    from .models import PortfolioItem
    portfolio_items = PortfolioItem.objects.filter(is_featured=False).order_by('-created_at')
    featured_items = PortfolioItem.objects.filter(is_featured=True).order_by('-created_at')

    portfolio_json = json.dumps([{
        'title': p.title,
        'tag': p.category,
        'img': p.image.url if p.image else 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800&q=80',
        'video': p.video_id if p.video_id else '',
    } for p in portfolio_items])

    featured_json = json.dumps([{
        'title': p.title,
        'tag': p.category,
        'img': p.image.url if p.image else 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800&q=80',
        'video': p.video_id if p.video_id else '',
    } for p in featured_items])

    return render(request, 'events/ourworks.html', {
        'portfolio_items_json': portfolio_json,
        'featured_items_json': featured_json,
    })
def contact(request):
    from .models import SiteContent
    def get_content(key, default=''):
        try:
            return SiteContent.objects.get(key=key).value
        except SiteContent.DoesNotExist:
            return default

    contact_info = {
        'phone': get_content('contact_phone', '+91 98843 67772'),
        'email': get_content('contact_email', 'info@eliteevents.com'),
        'address': get_content('contact_address', 'Chennai, Tamil Nadu'),
        'whatsapp': get_content('contact_whatsapp', ''),
        'instagram': get_content('contact_instagram', ''),
        'facebook': get_content('contact_facebook', ''),
    }

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and phone and message:
            ContactEnquiry.objects.create(
                name=name, email=email,
                phone=phone, subject=subject, message=message
            )
            try:
                html_message = render_to_string('events/email_template.html', {
                    'name': name, 'email': email,
                    'phone': phone, 'subject': subject, 'message': message,
                })
                send_mail(
                    subject='✨ Thank you for contacting Elite Events!',
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except:
                pass
    return render(request, 'events/contact.html', {'contact_info': contact_info})
def user_login(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('booking')
        return render(request, 'events/login.html', {'error': True})
    return render(request, 'events/login.html')
def user_register(request):
    if request.method == 'POST':
        name      = request.POST.get('name')
        email     = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'events/register.html', {'error': 'Passwords do not match!'})
        if User.objects.filter(email=email).exists():
            return render(request, 'events/register.html', {'error': 'Email already registered! Please login.'})
        user = User.objects.create_user(username=email, email=email, password=password1)
        user.first_name = name
        user.save()
        login(request, user)
        return redirect('booking')
    return render(request, 'events/register.html')
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def booking(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        event_type = request.POST.get('event_type')
        event_date = request.POST.get('event_date')

        EventBooking.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            event_type=event_type,
            event_date=event_date,
        )

        try:
            html_message = render_to_string('events/booking_confirmation.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'event_type': event_type,
                'event_date': event_date,
            })
            send_mail(
                subject='🎉 Your Booking is Confirmed – Elite Events!',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
        except:
            pass

        return redirect('my_bookings')    
    return render(request, 'events/booking.html', {
        'success': success,
        'user_name': request.user.first_name or request.user.username,
        'user_email': request.user.email,
    }) 
@login_required(login_url='/login/')
def my_bookings(request):
    bookings = EventBooking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'events/my_bookings.html', {'bookings': bookings})
# ================================================================
# ADMIN PANEL VIEWS
# ================================================================
import json
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import (
    ContactEnquiry, EventBooking, Service, PortfolioItem,
    Testimonial, TeamMember, SiteImage, SiteContent, SiteSetting
)

# ── Admin Dashboard Page ──────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def admin_dashboard(request):
    return render(request, 'events/admin_dashboard.html')

# ── Admin Login / Logout ──────────────────────────────────────
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_panel:dashboard')
        return render(request, 'events/admin_login.html', {'error': 'Invalid credentials or not an admin.'})
    return render(request, 'events/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_panel:login')

# ── Helper ────────────────────────────────────────────────────
def ajax_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

# ── Dashboard Stats API ───────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_dashboard_stats(request):
    now = timezone.now()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0)

    total_bookings    = EventBooking.objects.count()
    total_users       = User.objects.filter(is_staff=False).count()
    total_enquiries   = ContactEnquiry.objects.count()
    monthly_bookings  = EventBooking.objects.filter(booked_at__gte=this_month_start).count()
    pending_bookings  = EventBooking.objects.filter(status='pending').count()
    unread_enquiries  = ContactEnquiry.objects.filter(is_read=False).count()

    # Booking trend — last 6 months
    labels, values = [], []
    for i in range(5, -1, -1):
        d = now - timedelta(days=i*30)
        month_start = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if d.month == 12:
            month_end = d.replace(year=d.year+1, month=1, day=1)
        else:
            month_end = d.replace(month=d.month+1, day=1)
        count = EventBooking.objects.filter(booked_at__gte=month_start, booked_at__lt=month_end).count()
        labels.append(d.strftime('%b'))
        values.append(count)

    # Status breakdown
    pending  = EventBooking.objects.filter(status='pending').count()
    approved = EventBooking.objects.filter(status='approved').count()
    rejected = EventBooking.objects.filter(status='rejected').count()

    # Recent bookings
    recent = EventBooking.objects.order_by('-booked_at')[:5]
    recent_bookings = [{'name': b.name, 'event_type': b.get_event_type_display(), 'status': b.status} for b in recent]

    # Activity feed
    activity = []
    for b in EventBooking.objects.order_by('-booked_at')[:3]:
        activity.append({'text': f'New booking from {b.name}', 'time': b.booked_at.strftime('%d %b, %I:%M %p'), 'color': 'gold'})
    for e in ContactEnquiry.objects.order_by('-submitted_at')[:3]:
        activity.append({'text': f'New enquiry from {e.name}', 'time': e.submitted_at.strftime('%d %b, %I:%M %p'), 'color': 'blue'})
    activity.sort(key=lambda x: x['time'], reverse=True)

    return JsonResponse({
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_enquiries': total_enquiries,
        'monthly_bookings': monthly_bookings,
        'pending_bookings': pending_bookings,
        'unread_enquiries': unread_enquiries,
        'booking_trend': {'labels': labels, 'values': values},
        'status_breakdown': {'labels': ['Pending', 'Approved', 'Rejected'], 'values': [pending, approved, rejected]},
        'recent_bookings': recent_bookings,
        'activity': activity,
    })

# ── Bookings API ──────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_bookings_list(request):
    bookings = EventBooking.objects.order_by('-booked_at')
    data = [{'id': b.id, 'name': b.name, 'email': b.email, 'phone': b.phone,
             'event_type': b.get_event_type_display(), 'event_date': str(b.event_date),
             'status': b.status, 'created_at': b.booked_at.strftime('%d %b %Y')} for b in bookings]
    return JsonResponse({'bookings': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_booking_detail(request, pk):
    try:
        b = EventBooking.objects.get(pk=pk)
        return JsonResponse({'id': b.id, 'name': b.name, 'email': b.email, 'phone': b.phone,
                             'event_type': b.get_event_type_display(), 'event_date': str(b.event_date),
                             'status': b.status, 'created_at': b.booked_at.strftime('%d %b %Y'),
                             'message': ''})
    except EventBooking.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_booking_status(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            b = EventBooking.objects.get(pk=pk)
            b.status = data.get('status', b.status)
            b.save()
            return JsonResponse({'success': True})
        except EventBooking.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_booking_delete(request, pk):
    if request.method == 'DELETE':
        EventBooking.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})

# ── Users API ─────────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_users_list(request):
    users = User.objects.filter(is_staff=False).order_by('-date_joined')
    data = [{'id': u.id, 'username': u.get_full_name() or u.username, 'email': u.email,
             'date_joined': u.date_joined.strftime('%d %b %Y'),
             'last_login': u.last_login.strftime('%d %b %Y') if u.last_login else 'Never',
             'is_active': u.is_active} for u in users]
    return JsonResponse({'users': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_user_toggle(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            u = User.objects.get(pk=pk)
            u.is_active = data.get('is_active', u.is_active)
            u.save()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_user_delete(request, pk):
    if request.method == 'DELETE':
        User.objects.filter(pk=pk, is_staff=False).delete()
        return JsonResponse({'success': True})

# ── Enquiries API ─────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_enquiries_list(request):
    enquiries = ContactEnquiry.objects.order_by('-submitted_at')
    data = [{'id': e.id, 'name': e.name, 'email': e.email, 'phone': e.phone,
             'subject': e.subject, 'message': e.message, 'is_read': e.is_read,
             'created_at': e.submitted_at.strftime('%d %b %Y')} for e in enquiries]
    return JsonResponse({'enquiries': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_enquiry_detail(request, pk):
    try:
        e = ContactEnquiry.objects.get(pk=pk)
        return JsonResponse({'id': e.id, 'name': e.name, 'email': e.email, 'phone': e.phone,
                             'subject': e.subject, 'message': e.message, 'is_read': e.is_read,
                             'created_at': e.submitted_at.strftime('%d %b %Y')})
    except ContactEnquiry.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_enquiry_read(request, pk):
    if request.method == 'POST':
        ContactEnquiry.objects.filter(pk=pk).update(is_read=True)
        return JsonResponse({'success': True})

@staff_member_required(login_url='/admin-panel/login/')
def api_enquiry_delete(request, pk):
    if request.method == 'DELETE':
        ContactEnquiry.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})

# ── Content API ───────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_content_get(request):
    def get_val(key, default=''):
        try:
            return SiteContent.objects.get(key=key).value
        except SiteContent.DoesNotExist:
            return default

    import json as _json
    try:
        hero_slides = _json.loads(get_val('hero_slides', '[]'))
    except:
        hero_slides = []

    return JsonResponse({
    'about': {
        'heading': get_val('about_heading'),
        'subheading': get_val('about_subheading'),
        'body': get_val('about_body'),
        'welcome_text': get_val('about_welcome_text'),
    },
    'contact': {
        'phone': get_val('contact_phone'),
        'email': get_val('contact_email'),
        'address': get_val('contact_address'),
        'whatsapp': get_val('contact_whatsapp'),
        'instagram': get_val('contact_instagram'),
        'facebook': get_val('contact_facebook'),
    },
    'corporart': {
        'title': get_val('corporart_title'),
        'desc': get_val('corporart_desc'),
    },
    'hero_content': {
    'badge': get_val('hero_badge'),
    'title_line1': get_val('hero_title_line1'),
    'title_line2': get_val('hero_title_line2'),
    'title_line3': get_val('hero_title_line3'),
    'subtitle': get_val('hero_subtitle'),
    'stat1_num': get_val('hero_stat1_num'),
    'stat1_label': get_val('hero_stat1_label'),
    'stat2_num': get_val('hero_stat2_num'),
    'stat2_label': get_val('hero_stat2_label'),
    'stat3_num': get_val('hero_stat3_num'),
    'stat3_label': get_val('hero_stat3_label'),
},
    'hero_slides': hero_slides,
})
@staff_member_required(login_url='/admin-panel/login/')
def api_content_save(request):
    if request.method == 'POST':
        import json as _json
        data = _json.loads(request.body)

        def set_val(key, value):
            SiteContent.objects.update_or_create(key=key, defaults={'value': value})

        if 'about' in data:
            set_val('about_heading',    data['about'].get('heading', ''))
            set_val('about_subheading', data['about'].get('subheading', ''))
            set_val('about_body',       data['about'].get('body', ''))
            set_val('about_welcome_text', data['about'].get('welcome_text', ''))

        if 'contact' in data:
            for field in ['phone','email','address','whatsapp','instagram','facebook']:
                set_val(f'contact_{field}', data['contact'].get(field, ''))
        if 'corporart' in data:
            set_val('corporart_title', data['corporart'].get('title', ''))
            set_val('corporart_desc',  data['corporart'].get('desc', ''))
        if 'hero_slides' in data:
            set_val('hero_slides', _json.dumps(data['hero_slides']))
        if 'hero_content' in data:
            hc = data['hero_content']
            set_val('hero_badge', hc.get('badge', ''))
            set_val('hero_title_line1', hc.get('title_line1', ''))
            set_val('hero_title_line2', hc.get('title_line2', ''))
            set_val('hero_title_line3', hc.get('title_line3', ''))
            set_val('hero_subtitle', hc.get('subtitle', ''))
            set_val('hero_stat1_num', hc.get('stat1_num', ''))
            set_val('hero_stat1_label', hc.get('stat1_label', ''))
            set_val('hero_stat2_num', hc.get('stat2_num', ''))
            set_val('hero_stat2_label', hc.get('stat2_label', ''))
            set_val('hero_stat3_num', hc.get('stat3_num', ''))
            set_val('hero_stat3_label', hc.get('stat3_label', ''))
        return JsonResponse({'success': True})

# ── Images API ────────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_images_list(request):
    category = request.GET.get('category', 'all')
    qs = SiteImage.objects.all() if category == 'all' else SiteImage.objects.filter(category=category)
    data = [{'id': img.id, 'name': img.name, 'url': img.image.url, 'category': img.category} for img in qs.order_by('-uploaded_at')]
    return JsonResponse({'images': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_images_upload(request):
    if request.method == 'POST':
        files    = request.FILES.getlist('images')
        category = request.POST.get('category', 'gallery')
        if not files:
            return JsonResponse({'error': 'No files provided'}, status=400)
        for f in files:
            SiteImage.objects.create(image=f, category=category, name=f.name)
        return JsonResponse({'success': True, 'count': len(files)})

@staff_member_required(login_url='/admin-panel/login/')
def api_image_delete(request, pk):
    if request.method == 'DELETE':
        try:
            img = SiteImage.objects.get(pk=pk)
            img.image.delete()
            img.delete()
            return JsonResponse({'success': True})
        except SiteImage.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

# ── Services API ──────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_services_list(request):
    items = Service.objects.order_by('-created_at')
    data = [{'id': s.id, 'name': s.name, 'description': s.description,
             'price': str(s.price) if s.price else '', 'is_active': s.is_active} for s in items]
    return JsonResponse({'services': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_service_detail(request, pk):
    try:
        s = Service.objects.get(pk=pk)
        return JsonResponse({'id': s.id, 'name': s.name, 'description': s.description,
                             'price': str(s.price) if s.price else '', 'is_active': s.is_active})
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_service_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Service.objects.create(
            name=data.get('name',''), description=data.get('description',''),
            price=data.get('price') or None, is_active=data.get('is_active', True))
        return JsonResponse({'success': True})

@staff_member_required(login_url='/admin-panel/login/')
def api_service_update(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        Service.objects.filter(pk=pk).update(
            name=data.get('name',''), description=data.get('description',''),
            price=data.get('price') or None, is_active=data.get('is_active', True))
        return JsonResponse({'success': True})

@staff_member_required(login_url='/admin-panel/login/')
def api_service_delete(request, pk):
    if request.method == 'DELETE':
        Service.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})

# ── Portfolio API ─────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_portfolio_list(request):
    items = PortfolioItem.objects.order_by('-created_at')
    data = [{'id': p.id, 'title': p.title, 'category': p.category,
             'date': str(p.date) if p.date else '', 'description': p.description,
             'is_featured': p.is_featured} for p in items]
    return JsonResponse({'items': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_portfolio_detail(request, pk):
    try:
        p = PortfolioItem.objects.get(pk=pk)
        return JsonResponse({'id': p.id, 'title': p.title, 'category': p.category,
                             'date': str(p.date) if p.date else '', 'description': p.description,
                             'is_featured': p.is_featured})
    except PortfolioItem.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_portfolio_create(request):
    if request.method == 'POST':
        item = PortfolioItem.objects.create(
            title=request.POST.get('title',''),
            category=request.POST.get('category',''),
            date=request.POST.get('date') or None,
            description=request.POST.get('description',''),
            video_id=request.POST.get('video_id',''),
            is_featured=request.POST.get('is_featured') == 'true',
        )
        if request.FILES.get('image'):
            item.image = request.FILES['image']
            item.save()
        return JsonResponse({'success': True})

@staff_member_required(login_url='/admin-panel/login/')
def api_portfolio_update(request, pk):
    if request.method == 'POST':
        try:
            item = PortfolioItem.objects.get(pk=pk)
            item.title = request.POST.get('title', item.title)
            item.category = request.POST.get('category', item.category)
            item.date = request.POST.get('date') or None
            item.description = request.POST.get('description', item.description)
            item.video_id = request.POST.get('video_id', item.video_id)
            item.is_featured = request.POST.get('is_featured') == 'true'
            if request.FILES.get('image'):
                item.image = request.FILES['image']
            item.save()
            return JsonResponse({'success': True})
        except PortfolioItem.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_portfolio_delete(request, pk):
    if request.method == 'DELETE':
        PortfolioItem.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})

# ── Testimonials API ──────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_testimonials_list(request):
    items = Testimonial.objects.order_by('-created_at')
    data = [{'id': t.id, 'name': t.name, 'event_type': t.event_type,
             'quote': t.quote, 'rating': t.rating, 'is_active': t.is_active} for t in items]
    return JsonResponse({'testimonials': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_testimonial_detail(request, pk):
    try:
        t = Testimonial.objects.get(pk=pk)
        return JsonResponse({'id': t.id, 'name': t.name, 'event_type': t.event_type,
                             'quote': t.quote, 'rating': t.rating, 'is_active': t.is_active})
    except Testimonial.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_testimonial_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Testimonial.objects.create(
            name=data.get('name',''), event_type=data.get('event_type',''),
            quote=data.get('quote',''), rating=data.get('rating', 5))
        return JsonResponse({'success': True})

@staff_member_required(login_url='/admin-panel/login/')
def api_testimonial_update(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        Testimonial.objects.filter(pk=pk).update(
            name=data.get('name',''), event_type=data.get('event_type',''),
            quote=data.get('quote',''), rating=data.get('rating', 5))
        return JsonResponse({'success': True})

@staff_member_required(login_url='/admin-panel/login/')
def api_testimonial_delete(request, pk):
    if request.method == 'DELETE':
        Testimonial.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})

# ── Team API ──────────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_team_list(request):
    items = TeamMember.objects.order_by('-created_at')
    data = [{'id': m.id, 'name': m.name, 'role': m.role, 'email': m.email,
             'phone': m.phone, 'bio': m.bio, 'is_active': m.is_active} for m in items]
    return JsonResponse({'members': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_team_detail(request, pk):
    try:
        m = TeamMember.objects.get(pk=pk)
        return JsonResponse({'id': m.id, 'name': m.name, 'role': m.role,
                             'email': m.email, 'phone': m.phone, 'bio': m.bio, 'is_active': m.is_active})
    except TeamMember.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_team_create(request):
    if request.method == 'POST':
        member = TeamMember.objects.create(
            name=request.POST.get('name',''),
            role=request.POST.get('role',''),
            email=request.POST.get('email',''),
            phone=request.POST.get('phone',''),
            bio=request.POST.get('bio',''),
        )
        if request.FILES.get('photo'):
            member.photo = request.FILES['photo']
            member.save()
        return JsonResponse({'success': True})
@staff_member_required(login_url='/admin-panel/login/')
def api_team_update(request, pk):
    if request.method == 'POST':
        try:
            member = TeamMember.objects.get(pk=pk)
            member.name  = request.POST.get('name', member.name)
            member.role  = request.POST.get('role', member.role)
            member.email = request.POST.get('email', member.email)
            member.phone = request.POST.get('phone', member.phone)
            member.bio   = request.POST.get('bio', member.bio)
            if request.FILES.get('photo'):
                member.photo = request.FILES['photo']
            member.save()
            return JsonResponse({'success': True})
        except TeamMember.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)
@staff_member_required(login_url='/admin-panel/login/')
def api_team_delete(request, pk):
    if request.method == 'DELETE':
        TeamMember.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})

# ── Settings API ──────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_settings_get(request):
    def get_val(key, default=''):
        try:
            return SiteSetting.objects.get(key=key).value
        except SiteSetting.DoesNotExist:
            return default
    return JsonResponse({
        'general': {
            'site_name': get_val('site_name', 'EventLuxe'),
            'tagline':   get_val('tagline', ''),
            'email':     get_val('email', ''),
            'phone':     get_val('phone', ''),
        },
        'access': {
            'maintenance_mode': get_val('maintenance_mode', 'false') == 'true',
            'booking_enabled':  get_val('booking_enabled', 'true') == 'true',
        }
    })

@staff_member_required(login_url='/admin-panel/login/')
def api_settings_save(request):
    if request.method == 'POST':
        import json as _json
        data = _json.loads(request.body)

        def set_val(key, value):
            SiteSetting.objects.update_or_create(key=key, defaults={'value': str(value)})

        if 'general' in data:
            for field in ['site_name','tagline','email','phone']:
                set_val(field, data['general'].get(field, ''))

        if 'access' in data:
            set_val('maintenance_mode', str(data['access'].get('maintenance_mode', False)).lower())
            set_val('booking_enabled',  str(data['access'].get('booking_enabled', True)).lower())

        return JsonResponse({'success': True})
# ── Clients API ───────────────────────────────────────────────
@staff_member_required(login_url='/admin-panel/login/')
def api_clients_list(request):
    from .models import Client
    clients = Client.objects.all().order_by('order', 'created_at')
    data = [{'id': c.id, 'name': c.name, 'is_partner': c.is_partner,
             'is_active': c.is_active, 'order': c.order,
             'logo': c.logo.url if c.logo else ''} for c in clients]
    return JsonResponse({'clients': data})

@staff_member_required(login_url='/admin-panel/login/')
def api_client_detail(request, pk):
    from .models import Client
    try:
        c = Client.objects.get(pk=pk)
        return JsonResponse({'id': c.id, 'name': c.name, 'is_partner': c.is_partner,
                             'is_active': c.is_active, 'order': c.order,
                             'logo': c.logo.url if c.logo else ''})
    except Client.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_client_create(request):
    if request.method == 'POST':
        from .models import Client
        client = Client.objects.create(
            name=request.POST.get('name', ''),
            order=request.POST.get('order', 0),
            is_partner=request.POST.get('is_partner') == 'true',
            is_active=request.POST.get('is_active') == 'true',
        )
        if request.FILES.get('logo'):
            client.logo = request.FILES['logo']
            client.save()
        return JsonResponse({'success': True})

@staff_member_required(login_url='/admin-panel/login/')
def api_client_update(request, pk):
    if request.method == 'POST':
        from .models import Client
        try:
            client = Client.objects.get(pk=pk)
            client.name = request.POST.get('name', client.name)
            client.order = request.POST.get('order', client.order)
            client.is_partner = request.POST.get('is_partner') == 'true'
            client.is_active = request.POST.get('is_active') == 'true'
            if request.FILES.get('logo'):
                client.logo = request.FILES['logo']
            client.save()
            return JsonResponse({'success': True})
        except Client.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

@staff_member_required(login_url='/admin-panel/login/')
def api_client_delete(request, pk):
    if request.method == 'DELETE':
        from .models import Client
        Client.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})