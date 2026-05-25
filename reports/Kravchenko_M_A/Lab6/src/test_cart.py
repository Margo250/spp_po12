"""
Тесты для shopping.py
Файл: test_cart.py
"""

from unittest.mock import patch
import pytest
import shopping
from shopping import Cart, log_purchase, apply_coupon


@pytest.fixture
def empty_cart():
    """Фикстура: возвращает пустой экземпляр Cart."""
    return Cart()


def test_add_item(cart):
    """Проверка добавления товара."""
    cart.add_item("Apple", 10.0)
    assert len(cart.items) == 1
    assert cart.items[0]["name"] == "Apple"
    assert cart.items[0]["price"] == 10.0


def test_add_item_negative_price(cart):
    """Проверка выброса ошибки при отрицательной цене."""
    with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
        cart.add_item("Test", -5.0)


def test_total_empty_cart(cart):
    """Проверка общей стоимости пустой корзины."""
    assert cart.total() == 0.0


def test_total_with_items(cart):
    """Проверка общей стоимости с товарами."""
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 15.0)
    cart.add_item("Orange", 25.0)
    assert cart.total() == 50.0


@pytest.mark.parametrize(
    "discount, expected",
    [
        (0, 50.0),
        (50, 25.0),
        (100, 0.0),
    ],
)
def test_apply_discount_valid(cart, discount, expected):
    """Проверка применения валидных скидок."""
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 15.0)
    cart.add_item("Orange", 25.0)
    cart.apply_discount(discount)
    assert cart.total() == expected


@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(cart, discount):
    """Проверка выброса ошибки при невалидной скидке."""
    cart.add_item("Apple", 10.0)
    with pytest.raises(ValueError, match="Скидка должна быть от 0 до 100 процентов"):
        cart.apply_discount(discount)


@patch("shopping.requests.post")
def test_log_purchase_calls_post(mock_post):
    """Проверка, что requests.post вызывается с корректными данными."""
    item = {"name": "Apple", "price": 10.0}
    log_purchase(item)

    mock_post.assert_called_once()
    mock_post.assert_called_once_with("https://example.com/log", json=item, timeout=5)


@patch("shopping.requests.post")
def test_log_purchase_multiple_calls(mock_post):
    """Проверка нескольких вызовов log_purchase."""
    item1 = {"name": "Apple", "price": 10.0}
    item2 = {"name": "Banana", "price": 15.0}

    log_purchase(item1)
    log_purchase(item2)

    assert mock_post.call_count == 2
    mock_post.assert_any_call("https://example.com/log", json=item1, timeout=5)
    mock_post.assert_any_call("https://example.com/log", json=item2, timeout=5)


def test_apply_coupon_save10(cart):
    """Проверка применения купона SAVE10."""
    cart.add_item("Apple", 100.0)
    apply_coupon(cart, "SAVE10")
    assert cart.total() == 90.0
    assert cart.discount_percent == 10


def test_apply_coupon_half(cart):
    """Проверка применения купона HALF."""
    cart.add_item("Apple", 100.0)
    apply_coupon(cart, "HALF")
    assert cart.total() == 50.0
    assert cart.discount_percent == 50


def test_apply_coupon_invalid(cart):
    """Проверка выброса ошибки при невалидном купоне."""
    cart.add_item("Apple", 100.0)
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart, "INVALID")


def test_apply_coupon_multiple_items(cart):
    """Проверка применения купона к корзине с несколькими товарами."""
    cart.add_item("Apple", 100.0)
    cart.add_item("Banana", 50.0)
    apply_coupon(cart, "HALF")
    assert cart.total() == 75.0


def test_apply_coupon_with_monkeypatch(monkeypatch):
    """Проверка, что monkeypatch позволяет изменить словарь купонов."""
    test_cart = Cart()
    test_cart.add_item("Apple", 100.0)

    test_coupons = {"TEST20": 20, "TEST30": 30}

    def mock_apply_coupon(cart_obj, code):
        cart_obj.apply_discount(test_coupons.get(code, 0))

    monkeypatch.setattr("shopping.apply_coupon", mock_apply_coupon)

    shopping.apply_coupon(test_cart, "TEST20")
    assert test_cart.total() == 80.0


def test_apply_coupon_with_patch_dict():
    """Проверка использования patch.dict для мока словаря купонов."""

    def test_func(cart_obj, code):
        coupons = {"NEW": 25}
        if code in coupons:
            cart_obj.apply_discount(coupons[code])
        else:
            raise ValueError("Invalid coupon")

    test_cart = Cart()
    test_cart.add_item("Apple", 100.0)
    test_func(test_cart, "NEW")
    assert test_cart.total() == 75.0


def test_apply_discount_and_coupon_combined(cart):
    """Проверка последовательного применения скидки и купона."""
    cart.add_item("Apple", 100.0)
    cart.apply_discount(10)
    assert cart.total() == 90.0

    apply_coupon(cart, "HALF")
    assert cart.total() == 50.0


def test_coupon_does_not_affect_other_carts():
    """Проверка, что купон влияет только на конкретную корзину."""
    cart1 = Cart()
    cart2 = Cart()

    cart1.add_item("Apple", 100.0)
    cart2.add_item("Apple", 100.0)

    apply_coupon(cart1, "HALF")

    assert cart1.total() == 50.0
    assert cart2.total() == 100.0
