from django.shortcuts import render
from rest_framework.views import APIView
from user.models import UserProfile
from rest_framework.response import *
from rest_framework import status

from user.serializers import ProfileSerializer


class ProfileView(APIView):
    def get(self):
        pass
    
    def patch(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        other_name = request.data.get('other_name')
        bio_file = request.FILES.get('bio_file')
        phone_num = request.data.get('phone')
        gender = request.data.get('gender')
        address = request.data.get('address')
        profession = request.data.get('profession')
        marital_status = request.data.get('marital_status')
        date_of_birth= request.data.get('date_of_birth')

        try:
            profile=UserProfile.objects.get(user=request.user)
            profile.first_name=first_name,
            profile.last_name=last_name,
            profile.other_name=other_name,
            # bio_file=bio_file,
            profile.phone_num=phone_num,
            profile.gender=gender,
            profile.address=address,
            profile.profession=profession,
            profile.marital_status=marital_status,
            profile.date_of_birth=date_of_birth
            profile.save()
            return Response({'message':'success'}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'failed'}, status=status.HTTP_404_NOT_FOUND)

    # OR


    
    # def put(self, request, format=None):
    #     serializer = ProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)