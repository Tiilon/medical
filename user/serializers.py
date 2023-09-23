from django.contrib.auth import get_user_model
from rest_framework import serializers

from health.models import Patient
from user.models import UserProfile

User = get_user_model()
        
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_name = serializers.CharField(source="user_profile.first_name")
    last_name = serializers.CharField(source="user_profile.last_name")
    gender = serializers.CharField(source="user_profile.gender")
    profile_photo = serializers.ImageField(source="user_profile.bio_file")
    has_profile = serializers.SerializerMethodField()
    uid = serializers.ReadOnlyField(source="user_profile.uid")

    class Meta:
        model = User
        fields = '__all__'
        # fields = [
        #     "uid",
        #     "username",
        #     "email",
        #     "first_name",
        #     "last_name",
        #     "full_name",
        #     "gender",
        #     "profile_photo",
        #     "has_profile"
        # ]

    def get_full_name(self, obj):
        return obj.user_profile.full_name() if hasattr(obj, 'user_profile') else obj.email

    def get_has_profile(self, obj):
        return hasattr(obj, 'user_profile')

    # def to_representation(self, instance):
    #     representation = super(UserSerializer, self).to_representation(instance)
    #     representation["admin"] = instance.is_superuser
    #     return representation

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        

class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio_file']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
class PatientSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(source="profile.uid")
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        models = Patient
        fields = [
            'patient_id',
            'uid',
            'full_name',  
        ]
    
    def get_full_name(self, obj):
        return obj.profile.full_name() if hasattr(obj, 'profile') else obj.patient_id
