import pytest
from main import Product, Category  # Замените your_module на имя вашего файла с кодом


@pytest.fixture(autouse=True)
def reset_counters():
    """Фикстура для сброса счетчиков категорий и продуктов перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_init():
    """Тест корректной инициализации продукта и геттера цены."""
    product = Product("Test Phone", "Description", 50000.0, 10)
    assert product.name == "Test Phone"
    assert product.description == "Description"
    assert product.price == 50000.0
    assert product.quantity == 10
    
    # Проверяем, что атрибут действительно приватный
    with pytest.raises(AttributeError):
        _ = product.__price


def test_product_price_setter_valid():
    """Тест изменения цены на корректное (положительное) значение."""
    product = Product("Test Phone", "Description", 50000.0, 10)
    product.price = 60000.0
    assert product.price == 60000.0


def test_product_price_setter_invalid(capsys):
    """Тест попытки установить некорректную цену (0 или отрицательную)."""
    product = Product("Test Phone", "Description", 50000.0, 10)
    
    # Отрицательная цена
    product.price = -100.0
    assert product.price == 50000.0  # Цена не изменилась
    captured = capsys.readouterr()
    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"

    # Нулевая цена
    product.price = 0
    assert product.price == 50000.0  # Цена не изменилась
    captured = capsys.readouterr()
    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"


def test_new_product_classmethod():
    """Тест создания продукта из словаря через класс-метод."""
    product_data = {
        "name": "Xiaomi",
        "description": "Global Version",
        "price": 20000.0,
        "quantity": 5
    }
    product = Product.new_product(product_data)
    
    assert isinstance(product, Product)
    assert product.name == "Xiaomi"
    assert product.price == 20000.0
    assert product.quantity == 5


def test_category_init_and_counters():
    """Тест инициализации категории и подсчета количества категорий/продуктов."""
    p1 = Product("P1", "D1", 100.0, 2)
    p2 = Product("P2", "D2", 200.0, 3)
    
    category = Category("Smartphones", "Desc", [p1, p2])
    
    assert category.name == "Smartphones"
    assert category.description == "Desc"
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_add_product():
    """Тест метода add_product и изменения счетчика продуктов."""
    p1 = Product("P1", "D1", 100.0, 2)
    category = Category("Smartphones", "Desc", [p1])
    
    assert Category.product_count == 1
    
    p2 = Product("P2", "D2", 200.0, 3)
    category.add_product(p2)
    
    assert Category.product_count == 2


def test_category_products_getter():
    """Тест геттера products на соответствие строгому строковому шаблону."""
    p1 = Product("Samsung", "Desc", 100.0, 5)
    p2 = Product("Iphone", "Desc", 200.0, 8)
    category = Category("Smartphones", "Desc", [p1, p2])
    
    expected_output = (
        "Samsung, 100.0 руб. Остаток: 5 шт.\n"
        "Iphone, 200.0 руб. Остаток: 8 шт.\n"
    )
    assert category.products == expected_output
