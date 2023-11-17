from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from config.settings import STRIPE_API_KEY

import stripe

from courses.models import Subscription


def get_link_to_pay(obj):

    stripe.api_key = STRIPE_API_KEY

    product = stripe.Product.create(name=obj.pk)

    price = stripe.Price.create(
        unit_amount=obj.price,
        currency="usd",
        recurring={"interval": "month"},
        product=product.id,
    )

    payment_link = stripe.PaymentLink.create(
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            },
        ],
    )

    return payment_link.url

def send_mailing(subscription_pk):
    subscription = Subscription.objects.get(pk=subscription_pk)
    user = subscription.user
    emails = [user.email]
    course = subscription.course

    send_mail(
        subject="Course Updated",
        message=f"Course {course.name} is updated",
        from_email=EMAIL_HOST_USER,
        recipient_list=emails
    )
