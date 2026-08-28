from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    category = models.CharField(max_length=80)
    material = models.CharField(max_length=80)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=20, default='3D')
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=160)
    icon = models.CharField(max_length=20, default='3D')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Gallery(models.Model):
    MEDIA_TYPES = [('image', 'Image'), ('video', 'Video')]
    title = models.CharField(max_length=160)
    image = models.ImageField(upload_to='gallery/', blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    video = models.FileField(upload_to='gallery/', blank=True, validators=[FileExtensionValidator(['mp4', 'webm', 'mov'])])
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Gallery items'

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.media_type == 'image' and not self.image:
            raise ValidationError('An image is required for image gallery items.')
        if self.media_type == 'video' and not self.video:
            raise ValidationError('A video is required for video gallery items.')


class PricingPlan(models.Model):
    name = models.CharField(max_length=80)
    price = models.CharField(max_length=80)
    unit = models.CharField(max_length=120)
    delivery_time = models.CharField(max_length=120)
    features = models.TextField(help_text='Enter one feature per line.')
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def feature_list(self):
        return [feature.strip() for feature in self.features.splitlines() if feature.strip()]

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=120)
    description = models.TextField()
    role = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.customer_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    service = models.CharField(max_length=120)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.email}'
