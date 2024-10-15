from rest_framework import serializers
from .models import Parent
from django.contrib.auth import get_user_model
from .utils.otp import OTP
from rest_framework.exceptions import ValidationError
from .models import Region, City, Child, ChildLevels


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ["id", "name", "regions"]


class ParentSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field="name", queryset=City.objects.all())
    region = serializers.SlugRelatedField(
        slug_field="name", queryset=Region.objects.all()
    )

    class Meta:
        model = Parent
        fields = ["id", "name", "city", "region", "age", "user"]

    def validate(self, data):
        data = super().validate(data)
        city = data.get("city", False)
        region = data.get("region", False)

        # Check if the region's city matches the provided city
        if city and region and region.city != city:
            raise ValidationError(
                "The selected region does not belong to the selected city."
            )

        return data

    def create(self, validated_data):

        parent = Parent.objects.create(**validated_data)

        return parent


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("phoneNumber", "username", "password")

    def create(self, validated_data):

        password = validated_data.pop("password")
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)

        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):

        instance.username = validated_data.get("username", instance.username)

        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()

        return instance


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ["id", "gender", "name", "age", "image", "parent"]

    def update(self, instance, validated_data):

        image = validated_data.pop("image", None)
        if image:
            instance.image = image

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ChildLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChildLevels
        fields = ("id", "child", "stars", "level", "complete")


from phonenumber_field.serializerfields import PhoneNumberField


class PhoneNumberSerializer(serializers.Serializer):
    phoneNumber = PhoneNumberField(region="UZ")
