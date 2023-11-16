from config.settings import STRIPE_API_KEY

import stripe


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