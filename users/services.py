import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product(name):
    """Создание продукта в страйпе"""
    product = stripe.Product.create(name=name)
    return product


def create_price(amount, name):
    """Создание цены в страйпе"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": name.get("name")},
    )
    return price


def create_session_payment(price):
    """Создание сессии оплаты в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def check_payment(session_id):
    """Проверка статуса оплаты в страйпе"""
    payment_status = stripe.checkout.Session.retrieve(session_id)
    return payment_status.get("payment_status")
