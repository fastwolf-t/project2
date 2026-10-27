import pytest
# Импортируем классы из нашего основного файла main.py
from main import Category, Product


@pytest.fixture(autouse=True)
def clean_counters():
    """Фикстура автоматически очищает счетчики классов ПЕРЕД каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Тест создания продукта"""
    prod = Product("Iphone 15", "512GB", 210000.0, 8)
    assert prod.name == "Iphone 15"
    assert prod.description == "512GB"
    assert prod.price == 210000.0
    assert prod.quantity == 8


def test_category_initialization():
    """Тест создания категории"""
    prod = Product("Iphone 15", "512GB", 210000.0, 8)
    cat = Category("Смартфоны", "Описание", [prod])
    
    assert cat.name == "Смартфоны"
    assert cat.description == "Описание"
    assert len(cat.products) == 1


def test_counters():
    """Тест правильности подсчета категорий и продуктов"""
    p1 = Product("Samsung", "256GB", 180000.0, 5)
    p2 = Product("Iphone", "512GB", 210000.0, 8)
    Category("Смартфоны", "Описание 1", [p1, p2])

    p3 = Product("Xiaomi", "1024GB", 31000.0, 14)
    Category("Телевизоры", "Описание 2", [p3])

    assert Category.category_count == 2
    assert Category.product_count == 3
