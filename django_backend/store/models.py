from django.db import models
from courses.models import Course
from accounts.models import User
from uuid import uuid4

class Cart (models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True) # Set on creation
    updated_at = models.DateTimeField(auto_now=True)

class CartItem (models.model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Order (models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(help_text="Price in toman (whole numbers only).")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class OrderItem (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price_at_purchase = models.PositiveIntegerField(help_text="Price in toman (whole numbers only).")