from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from store.models import Order
from .producer import publisher

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        message = {
            'user_id': instance.id,
            'username': instance.username
        }
        # Publish the message to RabbitMQ
        publisher.publish_event(message, 'user_creation')

@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    if created:
        message = {
            'order_id': instance.id,
            'user_id': instance.user.id
        }
        # Publish the message to RabbitMQ
        publisher.publish_event( message, 'order_creation')