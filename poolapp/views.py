from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from urllib.parse import quote
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Category, Product, Service, GalleryImage, Testimonial, SiteSettings
)



def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "admin/login.html")



@login_required(login_url='admin_login')
def admin_dashboard(request):
    # Allow only superusers
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        logout(request)
        return redirect("admin_login")

    context = {
        "total_products": Product.objects.count(),
        "total_services": Service.objects.count(),
        "total_gallery": GalleryImage.objects.count(),
        "total_testimonials": Testimonial.objects.count(),
        "site_settings": SiteSettings.load(),
    }

    return render(request, "admin/dashboard.html", context)


@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("admin_login")




def build_whatsapp_link(number, message):
    """
    Builds a wa.me link that opens WhatsApp with a pre-filled message.
    Works on both mobile (opens app) and desktop (opens WhatsApp Web).
    """
    return f"https://wa.me/{number}?text={quote(message)}"


def home(request):
    settings_obj = SiteSettings.load()
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    featured_services = Service.objects.filter(is_active=True, is_featured=True)[:6]
    gallery_images = GalleryImage.objects.filter(is_active=True)[:8]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]

    general_whatsapp_link = build_whatsapp_link(
        settings_obj.whatsapp_number,
        f"Hello {settings_obj.site_name}, I would like to know more about your "
        f"swimming pool construction and accessories."
    )

    context = {
        'featured_products': featured_products,
        'featured_services': featured_services,
        'gallery_images': gallery_images,
        'testimonials': testimonials,
        'general_whatsapp_link': general_whatsapp_link,
    }
    return render(request, 'store/index.html', context)


def product_list(request):
    settings_obj = SiteSettings.load()
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    query = request.GET.get('q')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'query': query or '',
    }
    return render(request, 'store/products.html', context)


def product_detail(request, slug):
    settings_obj = SiteSettings.load()
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    message = (
        f"Hello {settings_obj.site_name}, I am interested in ordering:\n"
        f"*{product.name}*\n"
        f"Price: ₹{product.display_price}\n"
        f"Could you please share more details and availability?"
    )
    whatsapp_link = build_whatsapp_link(settings_obj.whatsapp_number, message)

    context = {
        'product': product,
        'related_products': related_products,
        'whatsapp_link': whatsapp_link,
    }
    return render(request, 'store/product_detail.html', context)


def service_list(request):
    services = Service.objects.filter(is_active=True)
    context = {'services': services}
    return render(request, 'store/services.html', context)


def service_detail(request, slug):
    settings_obj = SiteSettings.load()
    service = get_object_or_404(Service, slug=slug, is_active=True)
    other_services = Service.objects.filter(is_active=True).exclude(pk=service.pk)[:4]

    message = (
        f"Hello {settings_obj.site_name}, I would like to book a *{service.name}* "
        f"service. Please share more details, pricing and available dates."
    )
    whatsapp_link = build_whatsapp_link(settings_obj.whatsapp_number, message)

    context = {
        'service': service,
        'other_services': other_services,
        'whatsapp_link': whatsapp_link,
    }
    return render(request, 'store/service_detail.html', context)


def gallery(request):
    images = GalleryImage.objects.filter(is_active=True)
    context = {'images': images}
    return render(request, 'store/gallery.html', context)


def about(request):
    settings_obj = SiteSettings.load()
    testimonials = Testimonial.objects.filter(is_active=True)
    context = {'testimonials': testimonials}
    return render(request, 'store/about.html', context)


def contact(request):
    settings_obj = SiteSettings.load()
    message = f"Hello {settings_obj.site_name}, I have a query regarding your services."
    whatsapp_link = build_whatsapp_link(settings_obj.whatsapp_number, message)
    context = {'whatsapp_link': whatsapp_link}
    return render(request, 'store/contact.html', context)