from rest_framework import serializers
from shop.models import Product, ProductImage, CartItem


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]

    def to_representation(self, instance):
        # Возвращаем только URL изображения
        return instance.image.url


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "manufacturers_code", "season", "width",
            "load_index", "profile", "speed_index", "diameter",
            "homologation", "tire_model", "product_code", "manufacturer",
            "item_with_the_hint", "description", "price", "images"
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity"]

    def create(self, validated_data):
        # Логика для создания нового CartItem
        session_id = self.context['request'].session.session_key
        product_id = validated_data.get('product_id')
        quantity = validated_data.get('quantity', 1)

        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    def to_representation(self, instance):
        """Custom representation for including product details"""
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        return representation
