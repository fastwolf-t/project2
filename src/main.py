from abc import ABC, abstractmethod


class PrintInfoMixin:
    """Выводит информацию о создании объекта."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(
            f"Создан объект класса {self.__class__.__name__} "
            f"с параметрами: {args}, {kwargs}"
        )


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех товаров."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевой или отрицательной")

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        raise NotImplementedError


class Product(PrintInfoMixin, BaseProduct):
    """Основной класс товара."""

    @classmethod
    def new_product(cls, product_data: dict):
        return cls(**product_data)

    def __str__(self) -> str:
        return (
            f"{self.name}, {self.price} руб. " f"Остаток: {self.quantity} шт."
        )

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного класса")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс смартфонов."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float = 0,
        model: str = "",
        memory: int = 0,
        color: str = "",
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Категория товаров."""

    category_count = 0
    product_count = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[Product],
    ):
        self.name = name
        self.description = description
        self.__products: list[Product] = []

        Category.category_count += 1

        for product in products:
            self.add_product(product)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products) + (
            "\n" if self.__products else ""
        )

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: " f"{total_quantity} шт."

    def get_products_list(self) -> list[Product]:
        return self.__products.copy()

    def __iter__(self):
        return CategoryIterator(self)


class CategoryIterator:
    """Итератор по товарам категории."""

    def __init__(self, category: Category):
        self._products = category.get_products_list()
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._products):
            raise StopIteration

        product = self._products[self._index]
        self._index += 1
        return product


if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    product2 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
    )
    product3 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
    )

    category1 = Category(
        "Смартфоны",
        "Смартфоны для коммуникации и повседневных задач",
        [product1, product2, product3],
    )

    print(category1)
    print(category1.products)
    print(f"Категорий: {Category.category_count}")
    print(f"Товаров: {Category.product_count}")

    smartphone = Smartphone(
        "Samsung Galaxy S24",
        "256GB, черный",
        120000.0,
        3,
        95.5,
        "Galaxy S24",
        256,
        "Черный",
    )

    grass = LawnGrass(
        "Газонная трава",
        "Устойчивая к засухе",
        1500.0,
        10,
        "Россия",
        "7-14 дней",
        "Зеленый",
    )

    category2 = Category(
        "Разное",
        "Товары разных типов",
        [smartphone, grass],
    )

    print(category2)

    for product in category2:
        print(product)

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
