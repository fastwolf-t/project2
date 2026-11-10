import pytest

from main import (
    BaseProduct,
    Category,
    CategoryIterator,
    LawnGrass,
    Product,
    Smartphone,
)


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасывает счётчики категорий и товаров перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product():
    return Product("Samsung", "Описание товара", 100.0, 10)


@pytest.fixture
def smartphone():
    return Smartphone(
        "Samsung",
        "Описание смартфона",
        100000.0,
        5,
        95.5,
        "S23",
        256,
        "Black",
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        "Газонная трава",
        "Описание травы",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


# BaseProduct и Product

def test_base_product_is_abstract():
    with pytest.raises(TypeError):
        BaseProduct("Товар", "Описание", 100.0, 1)


def test_product_inherits_base_product():
    assert issubclass(Product, BaseProduct)


def test_product_init(product):
    assert product.name == "Samsung"
    assert product.description == "Описание товара"
    assert product.price == 100.0
    assert product.quantity == 10


def test_product_price_is_private(product):
    assert not hasattr(product, "__price")
    assert hasattr(product, "_BaseProduct__price")


def test_product_price_setter(product):
    product.price = 200.0
    assert product.price == 200.0


@pytest.mark.parametrize("invalid_price", [0, -1, -100.5])
def test_product_price_setter_rejects_invalid_value(
    product, invalid_price, capsys
):
    product.price = invalid_price

    captured = capsys.readouterr()
    assert product.price == 100.0
    assert "Цена не должна быть нулевой или отрицательной" in captured.out


def test_new_product():
    product_data = {
        "name": "Samsung",
        "description": "Описание товара",
        "price": 100.0,
        "quantity": 10,
    }

    created_product = Product.new_product(product_data)

    assert isinstance(created_product, Product)
    assert created_product.name == "Samsung"
    assert created_product.price == 100.0


def test_product_str(product):
    assert str(product) == "Samsung, 100.0 руб. Остаток: 10 шт."


def test_product_add(product):
    another_product = Product("Iphone", "Описание", 200.0, 2)

    assert product + another_product == 1400.0


def test_product_add_rejects_non_product(product):
    with pytest.raises(TypeError):
        product + 100


# PrintInfoMixin

def test_mixin_prints_product_creation_info(capsys):
    Product("Samsung", "Описание", 100.0, 2)

    captured = capsys.readouterr()
    assert "Создан объект класса Product" in captured.out
    assert "Samsung" in captured.out
    assert "100.0" in captured.out


def test_mixin_prints_smartphone_creation_info(capsys):
    Smartphone("Samsung", "Описание смартфона", 100000, 5)

    captured = capsys.readouterr()
    assert "Создан объект класса Smartphone" in captured.out


def test_mixin_prints_lawn_grass_creation_info(capsys):
    LawnGrass(
        "Газонная трава",
        "Описание травы",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )

    captured = capsys.readouterr()
    assert "Создан объект класса LawnGrass" in captured.out


# Классы-наследники

def test_smartphone_init(smartphone):
    assert smartphone.name == "Samsung"
    assert smartphone.description == "Описание смартфона"
    assert smartphone.price == 100000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23"
    assert smartphone.memory == 256
    assert smartphone.color == "Black"


def test_lawn_grass_init(lawn_grass):
    assert lawn_grass.name == "Газонная трава"
    assert lawn_grass.description == "Описание травы"
    assert lawn_grass.price == 500.0
    assert lawn_grass.quantity == 20
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7 дней"
    assert lawn_grass.color == "Зеленый"


def test_smartphone_inherits_product(smartphone):
    assert isinstance(smartphone, Product)


def test_lawn_grass_inherits_product(lawn_grass):
    assert isinstance(lawn_grass, Product)


def test_smartphones_can_be_added(smartphone):
    another_smartphone = Smartphone(
        "Iphone",
        "Описание",
        200.0,
        3,
        90.0,
        "15",
        512,
        "White",
    )

    assert smartphone + another_smartphone == 100000.0 * 5 + 200.0 * 3


def test_lawn_grass_products_can_be_added(lawn_grass):
    another_grass = LawnGrass(
        "Газон 2",
        "Описание",
        300.0,
        5,
        "США",
        "5 дней",
        "Зеленый",
    )

    assert lawn_grass + another_grass == 500.0 * 20 + 300.0 * 5


def test_products_of_different_classes_cannot_be_added(
    smartphone, lawn_grass
):
    with pytest.raises(TypeError):
        smartphone + lawn_grass


# Category

def test_category_init(product):
    category = Category("Смартфоны", "Описание категории", [product])

    assert category.name == "Смартфоны"
    assert category.description == "Описание категории"
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_category_counters(product):
    another_product = Product("Iphone", "Описание", 200.0, 5)

    Category("Смартфоны", "Описание", [product, another_product])
    Category("Телевизоры", "Описание", [product])

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_category_add_product(product):
    category = Category("Смартфоны", "Описание", [])
    category.add_product(product)

    assert Category.product_count == 1
    assert "Samsung" in category.products


def test_category_rejects_invalid_product():
    category = Category("Смартфоны", "Описание", [])

    with pytest.raises(TypeError):
        category.add_product("Samsung")


def test_category_products_property(product):
    category = Category("Смартфоны", "Описание", [product])

    assert category.products == (
        "Samsung, 100.0 руб. Остаток: 10 шт.\n"
    )


def test_category_str(product):
    another_product = Product("Iphone", "Описание", 200.0, 3)
    category = Category(
        "Смартфоны", "Описание", [product, another_product]
    )

    assert str(category) == (
        "Смартфоны, количество продуктов: 13 шт."
    )


def test_empty_category_str():
    category = Category("Пустая категория", "Описание", [])

    assert str(category) == (
        "Пустая категория, количество продуктов: 0 шт."
    )


def test_get_products_list_returns_copy(product):
    category = Category("Смартфоны", "Описание", [product])

    products = category.get_products_list()
    products.clear()

    assert "Samsung" in category.products
    assert Category.product_count == 1


def test_category_accepts_product_subclasses(smartphone, lawn_grass):
    category = Category(
        "Разные товары", "Описание", [smartphone, lawn_grass]
    )

    assert "Samsung" in category.products
    assert "Газонная трава" in category.products


# CategoryIterator

def test_category_iterator(product):
    another_product = Product("Iphone", "Описание", 200.0, 3)
    category = Category(
        "Смартфоны", "Описание", [product, another_product]
    )

    iterator = CategoryIterator(category)

    assert next(iterator) is product
    assert next(iterator) is another_product

    with pytest.raises(StopIteration):
        next(iterator)


def test_category_is_iterable(product):
    another_product = Product("Iphone", "Описание", 200.0, 3)
    category = Category(
        "Смартфоны", "Описание", [product, another_product]
    )

    assert list(category) == [product, another_product]


def test_empty_category_iterator():
    category = Category("Пустая категория", "Описание", [])

    with pytest.raises(StopIteration):
        next(iter(category))