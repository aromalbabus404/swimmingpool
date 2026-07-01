from django.db import models

# Create your models here.
from django.db import models


# ===========================
# HERO SECTION
# ===========================
class Hero(models.Model):
    eyebrow = models.CharField(max_length=200)
    heading = models.CharField(max_length=300)
    sub_heading = models.TextField()
    video = models.FileField(upload_to="hero/videos/", blank=True, null=True)
    poster = models.ImageField(upload_to="hero/posters/", blank=True, null=True)

    stat1_value = models.CharField(max_length=50)
    stat1_label = models.CharField(max_length=100)

    stat2_value = models.CharField(max_length=50)
    stat2_label = models.CharField(max_length=100)

    stat3_value = models.CharField(max_length=50)
    stat3_label = models.CharField(max_length=100)

    stat4_value = models.CharField(max_length=50)
    stat4_label = models.CharField(max_length=100)

    def __str__(self):
        return self.heading


# ===========================
# CATEGORY
# ===========================
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ===========================
# PRODUCTS
# ===========================
class Product(models.Model):

    BADGES = (
        ("Best Seller", "Best Seller"),
        ("New", "New"),
        ("Sale", "Sale"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    image = models.ImageField(upload_to="products/")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    mrp = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    badge = models.CharField(
        max_length=30,
        choices=BADGES,
        blank=True
    )

    description = models.TextField(blank=True)

    stock = models.PositiveIntegerField(default=1)

    featured = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ===========================
# PRODUCT SIZE
# ===========================
class ProductSize(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sizes"
    )

    size = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


# ===========================
# GALLERY
# ===========================
class Gallery(models.Model):

    image = models.ImageField(upload_to="gallery/")

    title = models.CharField(
        max_length=200,
        blank=True
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Gallery Image"


# ===========================
# REVIEW
# ===========================
class Review(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    name = models.CharField(max_length=100)

    rating = models.IntegerField(default=5)

    review = models.TextField()

    image = models.ImageField(
        upload_to="reviews/profile/",
        blank=True,
        null=True
    )

    media = models.FileField(
        upload_to="reviews/media/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ===========================
# CONTACT
# ===========================
class Contact(models.Model):

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    message = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ===========================
# ORDER
# ===========================
class Order(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    customer_name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=15)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=20)

    address = models.TextField()

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id} - {self.customer_name}"


# ===========================
# ORDER ITEM
# ===========================
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    size = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.product.name


# ===========================
# SITE SETTINGS
# ===========================
class SiteSetting(models.Model):

    company_name = models.CharField(max_length=200)

    whatsapp = models.CharField(max_length=20)

    phone = models.CharField(max_length=20)

    email = models.EmailField()

    address = models.TextField()

    map_link = models.TextField(blank=True)

    def __str__(self):
        return self.company_name