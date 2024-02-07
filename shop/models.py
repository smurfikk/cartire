from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model, CharField, IntegerField, TextField, ForeignKey, CASCADE, EmailField, \
    DateTimeField, ImageField, BooleanField


class Product(Model):
    seasons = (
        ("winter studded", "Зимние шипованные"),
        ("winter non-studded", "Зимние нешипованные"),
        ("summer", "Летние"),
    )
    name = CharField(max_length=255, verbose_name="Название")
    manufacturers_code = IntegerField(verbose_name="Код производителя")
    season = CharField(max_length=255, choices=seasons, verbose_name="Сезон")
    width = IntegerField(verbose_name="Ширина")
    load_index = IntegerField(verbose_name="Индекс нагрузки")
    profile = IntegerField(verbose_name="Профиль")
    speed_index = CharField(max_length=255, verbose_name="Индекс скорости")
    diameter = IntegerField(verbose_name="Диаметр")
    homologation = CharField(max_length=255, verbose_name="Омологация")
    tire_model = CharField(max_length=255, verbose_name="Модель автошины")
    product_code = IntegerField(verbose_name="Код товара")
    manufacturer = CharField(max_length=255, verbose_name="Производитель")
    item_with_the_hint = IntegerField(verbose_name="Пункт с подсказкой")
    description = TextField(max_length=5000, verbose_name="Описание")
    price = IntegerField(verbose_name="Цена")
    visible = BooleanField(default=True, verbose_name="Видимость")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(Model):
    product = ForeignKey(Product, related_name='images', on_delete=CASCADE, verbose_name="Товар")
    image = ImageField(upload_to='product_images/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"


class Order(Model):
    created = DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    total_price = IntegerField(verbose_name="Общая стоимость")
    statuses = (
        ("created", "Создан"),
        ("complete", "Завершен"),
    )
    status = CharField(max_length=50, choices=statuses, default="created", verbose_name="Статус")

    def __str__(self):
        return f"#{self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Individual(Model):
    order = ForeignKey(Order, on_delete=CASCADE, verbose_name="Заказ")
    surname = CharField(max_length=100, verbose_name="Фамилия")
    name = CharField(max_length=100, verbose_name="Имя")
    patronymic = CharField(max_length=100, verbose_name="Отчество")
    email = EmailField(verbose_name="Email")
    phone = CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"


class LegalEntity(Model):
    order = ForeignKey(Order, on_delete=CASCADE, verbose_name="Заказ")
    surname = CharField(max_length=100, verbose_name="Фамилия")
    name = CharField(max_length=100, verbose_name="Имя")
    patronymic = CharField(max_length=100, verbose_name="Отчество")
    email = EmailField(verbose_name="Email")
    phone = CharField(max_length=20, verbose_name="Телефон")
    registration_number = CharField(max_length=100, verbose_name="ЕГРПОУ")
    legal_address = CharField(max_length=255, verbose_name="Юридический адрес")
    organization_name = CharField(max_length=255, verbose_name="Наименование организации")

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридические лица"


class Address(Model):
    order = ForeignKey(Order, on_delete=CASCADE, verbose_name="Заказ")
    city = CharField(max_length=100, verbose_name="Город")
    street = CharField(max_length=100, verbose_name="Улица")
    house_number = CharField(max_length=20, verbose_name="Номер дома")
    apartment_or_office = CharField(max_length=50, verbose_name="Квартира/Офис")
    entrance = CharField(max_length=10, verbose_name="Подъезд")
    floor = CharField(max_length=10, verbose_name="Этаж")
    intercom = CharField(max_length=20, verbose_name="Домофон")
    delivery_comments = TextField(max_length=1000, blank=True, null=True, verbose_name="Комментарий курьеру")

    def __str__(self):
        return f"{self.city}, {self.street}, дом {self.house_number}, кв {self.apartment_or_office}"

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"


class OrderItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE, verbose_name="Заказ")
    product = ForeignKey(Product, on_delete=CASCADE, verbose_name="Товар")
    quantity = IntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт."

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"


class CartItem(Model):
    session = ForeignKey(Session, on_delete=CASCADE, verbose_name="Сессия")
    product = ForeignKey(Product, on_delete=CASCADE, verbose_name="Товар")
    quantity = IntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        unique_together = ("session", "product")
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
