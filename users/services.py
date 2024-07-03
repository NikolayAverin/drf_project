import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product(product):
    pass


def create_price(amount):
    """Создание цены в страйпе"""
    stripe.Price.create(
        currency="usd",
        unit_amount=1000,
        recurring={"interval": "month"},
        product_data={"name": "Gold Plan"},
    )