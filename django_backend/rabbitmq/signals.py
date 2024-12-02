from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from store.models import Order
from .producer import publisher


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    if not created:  # Only check if the object is being updated
        # Print the status change
        print(f'Order ID {instance.id} status changed to {instance.status}')
        items = instance.items.all()

        # Check if the status has changed to 'completed'
        if instance.status == 'completed':
            course_ids = [item.course.id for item in items]
            print(f'Collected Course IDs for Order ID {instance.id}: {course_ids}')

            message = {
                'user_id': instance.user.id,
                'course_ids': course_ids # Get all course IDs associated with the order
            }
            # Print the message that will be published
            print(f'Publishing message to RabbitMQ: {message}')

            # Publish the message to RabbitMQ
            publisher.publish_event(message, 'order_creation')

            # Print successful publication
            print(f'Message published for Order ID {instance.id} to RabbitMQ.')
        else:
            print(f'Order ID {instance.id} status changed to {instance.status}, no action taken.')