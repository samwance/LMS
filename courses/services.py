import stripe


def get_link_to_pay(obj):

    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

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