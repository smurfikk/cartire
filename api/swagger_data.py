from drf_yasg import openapi

combined_filters_example = {
    "application/json": {
        "width": [
            1, 2
        ],
        "profile": [
            3, 4
        ],
        "diameter": [
            5, 67, 89
        ],
        "season": [
            "winter studded", "winter non-studded", "summer"
        ],
        "manufacturer": [
            "Компания1", "компания2",
        ]
    }
}
# Individual model fields
individual_properties = {
    'surname': openapi.Schema(type=openapi.TYPE_STRING, description="Фамилия"),
    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Имя"),
    'patronymic': openapi.Schema(type=openapi.TYPE_STRING, description="Отчество"),
    'phone': openapi.Schema(type=openapi.TYPE_STRING, description="Телефон"),
}

# Address model fields
address_properties = {
    'city': openapi.Schema(type=openapi.TYPE_STRING, description="Город"),
    'street': openapi.Schema(type=openapi.TYPE_STRING, description="Улица"),
    'house_number': openapi.Schema(type=openapi.TYPE_STRING, description="Номер дома"),
    'apartment_or_office': openapi.Schema(type=openapi.TYPE_STRING, description="Квартира/Офис"),
    'entrance': openapi.Schema(type=openapi.TYPE_STRING, description="Подъезд"),
    'floor': openapi.Schema(type=openapi.TYPE_STRING, description="Этаж"),
    'intercom': openapi.Schema(type=openapi.TYPE_STRING, description="Домофон"),
    'delivery_comments': openapi.Schema(type=openapi.TYPE_STRING, description="Комментарий курьеру"),
}

create_order_properties = {
    'contact_info': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="Информация о клиенте",
        properties={
            'session_id': openapi.Schema(type=openapi.TYPE_STRING, default="123abc", description="session_id"),
            'type': openapi.Schema(type=openapi.TYPE_STRING, default="individual",
                                   description="Тип клиента: individual или legal_entity"),
            'individual': openapi.Schema(type=openapi.TYPE_OBJECT, properties=individual_properties),
        },
        required=['type']
    ),
    'address': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="Информация об адресе доставки",
        properties=address_properties,
    )
}

create_order_responses = {
    200: openapi.Response(
        description="Заказ успешно создан",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'success': openapi.Schema(type=openapi.TYPE_STRING,
                                          description="Сообщение об успешном создании заказа", default="Заказ создан"),
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID созданного заказа")
            }
        )
    ),
    400: openapi.Response(description="Неверный тип контакта"),
    404: openapi.Response(description="Корзина не найдена")
}

product_detail_example = {
    "id": 1,
    "name": "285/45 R21 113H PIRELLI Scorpion Ice Zero 2 TL Run Flat шип",
    "season": "winter studded",
    "width": 1,
    "load_index": 2,
    "profile": 3,
    "speed_index": "4",
    "diameter": 5,
    "tire_model": "7",
    "product_code": 8,
    "manufacturer": "9",
    "description": "11",
    "price": 12,
    "visible": True,
    "images": [
        "/media/product_images/wheel-1.png",
        "/media/product_images/wheel-2.png"
    ]
}

cart_example = {
    "application/json": {
        "total_price": 1000,
        "items": [
            {
                "id": 1,
                "product": {
                    "id": 1,
                    "name": "285/45 R21 113H PIRELLI Scorpion Ice Zero 2 TL Run Flat шип",
                    "season": "winter studded",
                    "width": 1,
                    "load_index": 2,
                    "profile": 3,
                    "speed_index": "4",
                    "diameter": 5,
                    "tire_model": "7",
                    "product_code": 8,
                    "manufacturer": "9",
                    "description": "11",
                    "price": 12,
                    "images": [
                        "/media/product_images/wheel-1.png",
                        "/media/product_images/wheel-2.png"
                    ]
                },
                "quantity": 2
            },
            {
                "id": 2,
                "product": {
                    "id": 2,
                    "name": "Scorpion Ice Zero 2 TL Run Flat шип",
                    "season": "winter studded",
                    "width": 5,
                    "load_index": 2,
                    "profile": 3,
                    "speed_index": "4",
                    "diameter": 4,
                    "tire_model": "7",
                    "product_code": 8,
                    "manufacturer": "9",
                    "description": "11",
                    "price": 12,
                    "images": [
                        "/media/product_images/wheel-3.png"
                    ]
                },
                "quantity": 4
            },

        ]}
}
