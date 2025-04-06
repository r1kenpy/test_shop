from celery import shared_task
from django.core.mail import send_mail

from .models import Order

MESSAGE = (
    'Dear {first_name},\n\n'
    'You have successfully placed an order.'
    'Your order ID is {order_id}.'
)


@shared_task
def order_created(order_id):

    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = MESSAGE.format(first_name=order.first_name, order_id=order.id)
    mail_send = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_send
