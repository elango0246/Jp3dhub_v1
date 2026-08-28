from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactMessageForm
from .models import Gallery, Material, PricingPlan, Product, Service, Testimonial


def home(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Thank you! We'll get back to you within 2-4 hours.")
        return redirect('home')

    context = {
        'form': form,
        'products': Product.objects.filter(available=True),
        'featured_products': Product.objects.filter(available=True, featured=True),
        'services': Service.objects.filter(active=True),
        'materials': Material.objects.filter(active=True),
        'gallery': Gallery.objects.filter(active=True),
        'pricing_plans': PricingPlan.objects.filter(active=True),
        'testimonials': Testimonial.objects.filter(active=True),
    }
    return render(request, 'index.html', context)


def products(request):
    return render(request, 'products.html', {'products': Product.objects.filter(available=True)})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(request, 'product_detail.html', {'product': product})


def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! We'll get back to you within 2-4 hours.")
            return redirect('home')
    else:
        form = ContactMessageForm()
    return render(request, 'contact.html', {'form': form})
