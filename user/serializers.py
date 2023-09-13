from django.contrib.auth import get_user_model
# from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer
# from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="user_profile.gender")
    # phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.ImageField(source="user_profile.bio_file")
    # country = CountryField(source="profile.country")
    # city = serializers.CharField(source="profile.city")
    # top_seller = serializers.BooleanField(source="profile.top_seller")
    first_name = serializers.CharField(source="user_profile.gender")
    last_name = serializers.CharField(source="user_profile.gender")
    full_name = serializers.CharField(source="user_profile.get_full_name")

    class Meta:
        model = User
        fields = [
            "uid",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "profile_photo"
            # "top_seller"
        ]

    def get_first_name(self, obj):
        return obj.first_name.title()

    def get_last_name(self, obj):
        return obj.last_name.title()
    
    # def get_full_name(self, obj):
    #     return f"{obj.first_name.title()} {obj.last_name.title()}"

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["email","password"]