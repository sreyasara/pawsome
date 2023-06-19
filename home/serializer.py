from rest_framework import serializers
from .models import Address
from auth_login.models import User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        address = Address.objects.create(user=user, **validated_data)
        return address

    def update(self, instance, validated_data):
        instance.address_label = validated_data.get('address_label', instance.address_label)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
