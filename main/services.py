import stripe


from config import settings


def get_session(instance):
    """Метод get_session возвращает сессию для оплаты курса или урока по API"""
    stripe.api_key = settings.STRIPE_SECRET_KEY

    name_product = f'{instance.lesson}' if instance.lesson else ""
    name_product += f'{instance.course}' if instance.course else ""

    product = stripe.Product.create(name=f'{name_product}')
    price = stripe.Price.create(
        unit_amount=instance.payment_amount,
        currency='rub',
        product=f'{product.id}',
    )

    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": f"{price.id}",
                "quantity": 1,
            },
        ],
        mode="payment"
    )

    return session


def retrieve_session(session):
    """Метод возвращает объект сессии по API, id который перидался"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.checkout.Session.retrieve(
        session,
    )
