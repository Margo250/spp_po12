"""
Модуль с классами для тестирования.
Файл: shopping.py
"""

import requests


class Cart:
    """Класс корзины покупок."""

    def __init__(self):
        self.items = []
        self.discount_percent = 0

    def add_item(self, item_name: str, price: float):
        """Добавить товар в корзину."""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": item_name, "price": price})

    def total(self) -> float:
        """Вычислить общую стоимость с учетом скидки."""
        subtotal = sum(item["price"] for item in self.items)
        discount = subtotal * (self.discount_percent / 100)
        return subtotal - discount

    def apply_discount(self, percent: float):
        """Применить скидку к корзине."""
        if percent < 0 or percent > 100:
            raise ValueError("Скидка должна быть от 0 до 100 процентов")
        self.discount_percent = percent


def log_purchase(item: dict):
    """Записать покупку в удаленную систему."""
    requests.post("https://example.com/log", json=item, timeout=5)


def apply_coupon(cart: Cart, coupon_code: str):
    """Применить купон к корзине."""
    coupons = {"SAVE10": 10, "HALF": 50}
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
