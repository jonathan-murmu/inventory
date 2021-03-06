from rest_framework import serializers

from .models import Item, Variant, Property, Notification


class PropertySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    last_modified_by = serializers.ReadOnlyField(
        source='last_modified_by.username')

    class Meta:
        model = Property
        fields = ('id', 'option', 'value', 'last_modified_by')


class VariantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    properties = PropertySerializer(many=True)
    last_modified_by = serializers.ReadOnlyField(
        source='last_modified_by.username')

    class Meta:
        model = Variant
        fields = ('id', 'variant_name', 'selling_price', 'cost_price',
                  'quantity', 'properties', 'last_modified_by')


class ItemSerializer(serializers.ModelSerializer):
    """Nested serializer for Item-Variant-Property."""
    id = serializers.IntegerField(required=False)
    variants = VariantSerializer(many=True)
    last_modified_by = serializers.ReadOnlyField(
        source='last_modified_by.username')

    class Meta:
        model = Item
        fields = (
            'id', 'item_name', 'category', 'variants', 'last_modified_by')

    def create(self, validated_data):
        """Create the Item-variant-property at once."""
        variants_data = validated_data.pop('variants')
        item = Item.objects.create(**validated_data)

        # loop through the variant data and create a variant.
        for variant_data in variants_data:
            properties_data = variant_data.pop('properties')
            variant = Variant.objects.create(item=item, **variant_data)
            variant.last_modified_by = item.last_modified_by
            variant.save()

            # loop through the property for a variant and create.
            for property_data in properties_data:
                property = Property.objects.create(variant=variant,
                                                   **property_data)
                property.last_modified_by = item.last_modified_by
                property.save()

        return item

    def update(self, instance, validated_data):
        """Update the Item-variant-property"""
        instance.item_name = validated_data.get('item_name',
                                                instance.item_name)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.category = validated_data.get('category', instance.category)
        instance.last_modified_by = validated_data.get('last_modified_by',
                                                       instance.last_modified_by)
        variants_data = validated_data.get('variants', instance.variants)

        for variant in variants_data:
            variant_id = variant.get('id', None)
            if variant_id:
                try:
                    variant_obj = Variant.objects.get(pk=variant_id,
                                                      item=instance)
                except:
                    continue
                variant_obj.variant_name = variant.get('variant_name',
                                                       variant_obj.variant_name)
                variant_obj.selling_price = variant.get('selling_price',
                                                        variant_obj.selling_price)
                variant_obj.cost_price = variant.get('cost_price',
                                                     variant_obj.cost_price)
                variant_obj.quantity = variant.get('quantity',
                                                   variant_obj.quantity)
                variant_obj.variant_name = variant.get('variant_name',
                                                       variant_obj.variant_name)

                # now save the property of the variant
                properties_data = variant.get('properties',
                                              variant_obj.properties)
                for property in properties_data:
                    property_id = property.get('id', None)
                    if property_id:
                        try:
                            property_obj = Property.objects.get(pk=property_id,
                                                                variant=variant_obj)
                        except:
                            continue
                        property_obj.option = property.get('option',
                                                           property_obj.option)
                        property_obj.value = property.get('value',
                                                          property_obj.value)
                        property_obj.save()
                    else:
                        Property.objects.create(variant=variant_obj,
                                                **property)

                variant_obj.save()
            else:
                Variant.objects.create(item=instance, **variant)

        instance.save()
        return instance


class NotificationSerializer(serializers.ModelSerializer):
    """Notification feed serializer."""
    time = serializers.DateTimeField(read_only=True)
    fields = serializers.CharField(allow_blank=True, allow_null=True,
                                   max_length=255,
                                   required=False)
    action = serializers.ChoiceField(choices=Notification.ACTION_CHOICES)
    item = serializers.CharField(max_length=255)
    user__username = serializers.CharField(max_length=255)

    class Meta:
        model = Notification
        fields = ('time', 'fields', 'action', 'item', 'user__username')
