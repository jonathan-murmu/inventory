from rest_framework import serializers

from .models import Item, Variant, Property


# class BrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Brand
#         fields = ('id', 'brand_name')
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'option', 'value')


class VariantSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True)

    class Meta:
        model = Variant
        fields = ('id', 'variant_name', 'selling_price', 'cost_price',
                  'quantity', 'properties')


class ItemSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Item
        fields = ('id', 'item_name', 'category', 'variants')

    def create(self, validated_data):
        print validated_data
        variants_data = validated_data.pop('variants')
        item = Item.objects.create(**validated_data)
        # item = Item.objects.get(pk=1)

        for variant_data in variants_data:
            properties_data = variant_data.pop('properties')
            variant = Variant.objects.create(item=item, **variant_data)
            for property_data in properties_data:
                Property.objects.create(variant=variant, **property_data)

        return item
