import pytest

from main import Product, Category, CategoryIterator


@pytest.fixture
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0


def test_product_init():
    product = Product("Samsung", "Description", 100.0, 10)

    assert product.name == "Samsung"
    assert product.description == "Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_product_price_private():
    product = Product("Samsung", "Description", 100.0, 10)

    assert not hasattr(product, "__price")


def test_product_price_setter():
    product = Product("Samsung", "Description", 100.0, 10)

    product.price = 200.0

    assert product.price == 200.0


def test_product_price_setter_invalid(capsys):
    product = Product("Samsung", "Description", 100.0, 10)

    product.price = -50.0

    captured = capsys.readouterr()

    assert product.price == 100.0
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_new_product():
    product_data = {
        "name": "Samsung",
        "description": "Description",
        "price": 100.0,
        "quantity": 10
    }

    product = Product.new_product(product_data)

    assert product.name == "Samsung"
    assert product.description == "Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_category_init(reset_counters):
    product = Product("Samsung", "Description", 100.0, 10)

    category = Category("Смартфоны", "Описание", [product])

    assert category.name == "Смартфоны"
    assert category.description == "Описание"
    assert category.category_count == 1
    assert category.product_count == 1


def test_category_counters(reset_counters):
    product1 = Product("Samsung", "Description", 100.0, 10)
    product2 = Product("Iphone", "Description", 200.0, 5)

    Category("Смартфоны", "Описание", [product1, product2])
    Category("Телевизоры", "Описание", [product1])

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_add_product():
    Category.category_count = 0
    Category.product_count = 0

    product1 = Product("Samsung", "Description", 100.0, 10)
    product2 = Product("Iphone", "Description", 200.0, 5)

    category = Category("Смартфоны", "Описание", [product1])
    category.add_product(product2)

    assert Category.product_count == 2
    assert "Iphone" in category.products


def test_products_getter():
    product = Product("Samsung", "Description", 100.0, 10)

    category = Category("Смартфоны", "Описание", [product])

    assert category.products == (
        "Samsung, 100.0 руб. Остаток: 10 шт.\n"
    )


# Тесты нового функционала

def test_product_str():
    product = Product("Samsung", "Description", 80, 15)

    assert str(product) == "Samsung, 80 руб. Остаток: 15 шт."


def test_product_add():
    product1 = Product("Samsung", "Description", 100, 10)
    product2 = Product("Iphone", "Description", 200, 2)

    assert product1 + product2 == 1400


def test_product_add_invalid():
    product = Product("Samsung", "Description", 100, 10)

    with pytest.raises(TypeError):
        product + 100


def test_category_str():
    product1 = Product("Samsung", "Description", 100, 5)
    product2 = Product("Iphone", "Description", 200, 8)

    category = Category("Смартфоны", "Описание", [product1, product2])

    assert str(category) == (
        "Смартфоны, количество продуктов: 13 шт."
    )


def test_category_str_empty():
    category = Category("Пустая категория", "Описание", [])

    assert str(category) == (
        "Пустая категория, количество продуктов: 0 шт."
    )


def test_category_iterator():
    product1 = Product("Samsung", "Description", 100, 5)
    product2 = Product("Iphone", "Description", 200, 8)

    category = Category("Смартфоны", "Описание", [product1, product2])

    iterator = CategoryIterator(category)

    assert next(iterator) == product1
    assert next(iterator) == product2

    with pytest.raises(StopIteration):
        next(iterator)


def test_category_for_iteration():
    product1 = Product("Samsung", "Description", 100, 5)
    product2 = Product("Iphone", "Description", 200, 8)

    category = Category("Смартфоны", "Описание", [product1, product2])

    products = [product for product in category]

    assert products == [product1, product2]


def test_category_iterator_empty():
    category = Category("Пустая категория", "Описание", [])

    iterator = iter(category)

    with pytest.raises(StopIteration):
        next(iterator)


def test_category_add_invalid():
    category = Category("Смартфоны", "Описание", [])

    with pytest.raises(TypeError):
        category.add_product("Samsung")