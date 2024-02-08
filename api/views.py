import requests
from django.db import transaction
from django.db.models import Count
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from .swagger_data import *
from carTire import settings
from shop.models import Product, Order, OrderItem, CartItem, Individual, LegalEntity, Address


@swagger_auto_schema(
    method="get",
    responses={200: openapi.Response(
        description="Пример успешного ответа",
        examples=combined_filters_example
    )}
)
@api_view(["GET"])
def combined_filters(request):
    """
    Возвращает возможные значения фильтров для товаров.
    """
    products = Product.objects.all()
    filters = {
        "width": list(products.values_list("width", flat=True).distinct()),
        "profile": list(products.values_list("profile", flat=True).distinct()),
        "diameter": list(products.values_list("diameter", flat=True).distinct()),
        "season": list(products.values_list("season", flat=True).distinct()),
        "manufacturer": list(products.values_list("manufacturer", flat=True).distinct()),
    }
    return Response(filters)


@api_view(["GET"])
def product_list(request: WSGIRequest):
    """
    Возвращает список товаров, имеет возможность фильтрации.
    Возможные параметры фильтрации: width, profile, diameter, season, manufacturer
    По умолчанию сортировка по популярности.
    """
    products = Product.objects.filter(visible=True)  # Фильтрация видимых товаров

    # Фильтрация по параметрам
    width = request.GET.get("width")
    profile = request.GET.get("profile")
    diameter = request.GET.get("diameter")
    season = request.GET.get("season")
    manufacturer = request.GET.get("manufacturer")

    if width:
        products = products.filter(width=width)
    if profile:
        products = products.filter(profile=profile)
    if diameter:
        products = products.filter(diameter=diameter)
    if season:
        products = products.filter(season=season)
    if manufacturer:
        products = products.filter(manufacturer=manufacturer)

    products = products.annotate(popularity=Count("orderitem")).order_by("-popularity")

    # Сериализация данных
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="get",
    responses={200: openapi.Response(
        description="Пример успешного ответа",
        examples={
            "application/json": product_detail_example,
        },
    )}
)
@api_view(["GET"])
def product_detail(request: WSGIRequest, product_id: int):
    """
    Возвращает информацию о товаре по его ID.
    """
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method="post",
    operation_description="Создание заказа на основе товаров в корзине пользователя",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=create_order_properties,
        required=["contact_info", "address"]
    ),
    responses=create_order_responses,
)
@csrf_exempt
@api_view(["POST"])
def create_order(request):
    """
    Создание заказа.
    """
    session_id = request.session.session_key
    if not session_id or not CartItem.objects.filter(session_id=session_id).exists():
        return Response({"error": "Корзина пуста"}, status=404)

    contact_data = request.data.get("contact_info")
    address_data = request.data.get("address")
    contact_type = contact_data.get("type")
    if contact_type not in ["individual", "legal_entity"]:
        return Response({"error": "Неверный тип контакта"}, status=400)

    with transaction.atomic():

        # Создание заказа
        cart_items = CartItem.objects.filter(session_id=session_id)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(
            total_price=total_price
        )

        # Обработка информации об адресе
        address, _ = Address.objects.get_or_create(**address_data, order=order)

        # Обработка информации о контакте
        if contact_type == "individual":
            contact_info, _ = Individual.objects.get_or_create(**contact_data[contact_type], order=order)
        elif contact_type == "legal_entity":
            contact_info, _ = LegalEntity.objects.get_or_create(**contact_data[contact_type], order=order)

        # Добавление товаров в заказ и очистка корзины
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=item.product, quantity=item.quantity) for item in cart_items
        ])

        text = [f"<b>Заказ №{order.id}</b>\n"
                f"<b>Клиент:</b> {contact_info}\n"
                f"<b>Телефон:</b> {contact_info.phone}\n"
                f"<b>Адрес:</b> {address}\n"
                f"<b>Сумма заказа:</b> {total_price}₽\n\n"
                f"<b>Товары:</b>"]
        for item in cart_items:
            text.append(f"<b>{item.product}</b> - {item.quantity}шт ({item.quantity * item.product.price}₽)")
        cart_items.delete()

    send_telegram_message("\n".join(text))
    return Response({"success": "Заказ создан", "order_id": order.id})


@api_view(["GET"])
def session_manage(request: WSGIRequest):
    """
    Возвращает информацию о сессии.
    """
    # Создаем новую сессию, если она еще не существует
    if not request.session.session_key:
        request.session.save()

    session_key = request.session.session_key

    # Получаем или создаем сессию в базе данных
    session, created = Session.objects.get_or_create(session_key=session_key)

    # Подсчет количества товаров в корзине
    cart_items_count = CartItem.objects.filter(session=session).count()

    return Response({
        "session_id": session.session_key,
        "cart_items_count": cart_items_count,
        "created": created
    })


@swagger_auto_schema(
    method="get",
    responses={200: openapi.Response(
        description="Пример успешного ответа",
        examples=cart_example,

    )}
)
@api_view(["GET"])
def get_cart_items(request):
    """
    Возвращает товары в корзине.
    """
    session_id = request.session.session_key
    if not session_id:
        request.session.save()
        session_id = request.session.session_key

    items = CartItem.objects.filter(session_id=session_id)
    total_price = sum(item.product.price * item.quantity for item in items)

    serializer = CartItemSerializer(items, many=True)
    return Response({
        "items": serializer.data,
        "total_price": total_price
    })


@swagger_auto_schema(
    method="post",
    operation_description="Добавление товара в корзину пользователя",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID продукта"),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Количество товара", default=1)
        },
        required=['product_id'],
        examples={
            "application/json": {
                "product_id": 1,
                "quantity": 2
            }
        }
    ),
    responses={
        200: openapi.Response(description="Товар добавлен в корзину"),
        404: openapi.Response(description="Продукт не найден")
    }
)
@csrf_exempt
@api_view(["POST"])
def add_to_cart(request):
    """
    Добавление товара в корзину
    Пример: {"product_id": 1, "quantity":2}
    """
    session_id = request.session.session_key
    if not session_id:
        request.session.save()
        session_id = request.session.session_key

    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Продукт не найден"}, status=404)

    item, created = CartItem.objects.get_or_create(
        session_id=session_id, product=product, defaults={"quantity": quantity}
    )
    if not created:
        item.quantity += quantity
        item.save()

    return Response({"detail": "Товар добавлен в корзину"})


@csrf_exempt
@api_view(["POST"])
def remove_from_cart(request):
    """
    Удаление товара из корзины.
    Если 'all' установлен в true, удаляет все экземпляры товара. В противном случае удаляет один экземпляр.
    Пример: {"product_id": 1, "all": false} - удалит 1 товар.
    Пример: {"product_id": 1, "all": true} - удалит все единицы товара.
    """
    session_id = request.session.session_key
    if not session_id:
        return Response({"error": "Корзина не найдена"}, status=404)

    product_id = request.data.get("product_id")
    remove_all = request.data.get("all", False)

    try:
        item = CartItem.objects.get(session_id=session_id, product_id=product_id)
        if remove_all:
            # Удаление всех экземпляров товара
            item.delete()
        else:
            # Удаление одного экземпляра товара
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

        return Response({"detail": "Товар(ы) удален(ы) из корзины"})
    except CartItem.DoesNotExist:
        return Response({"error": "Товар в корзине не найден"}, status=404)


@api_view(["GET"])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Возвращает CSRF токен.
    """
    return Response({"detail": "CSRF cookie set"})


def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{settings.logs_bot_token}/sendMessage"
    data = {
        "chat_id": settings.logs_chat_id,
        "text": message,
        "parse_mode": "html",
    }
    response = requests.post(url, data=data)
    return response.json()
