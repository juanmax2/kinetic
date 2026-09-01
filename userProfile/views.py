from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

from kinetic.serializers import UserProfileSerializer

# Create your views here.
class CookieTokenObtainPairView(APIView):
    
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        print("--- DATOS RECIBIDOS EN LOGIN ---", request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token_str = str(refresh)
        
        profile_serializer = UserProfileSerializer(user.profile)
        
        response = Response({
            'access': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile': profile_serializer.data
                
            } 
        }, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key='refresh_token',
            value=refresh_token_str,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=7 * 24 * 60 * 60
        )
        
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=60 * 60
        )
        
        return response
    

class CookieTokenRefreshView(APIView):
    
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response({'detail': 'The refresh token was not found.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError):
            return Response({'detail': 'Refresh token invalid or expirated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class CookieTokenLogoutView(APIView):
    
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        response = Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        profile_serializer = UserProfileSerializer(user.profile)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profile': profile_serializer.data
        }, status=status.HTTP_200_OK) 
        
    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        
        if 'username' in data:
            user.username = data['username']
            
        if 'email' in data:
            user.email = data['email']
        user.save()
        
        profile_serializer = UserProfileSerializer(user.profile, data=data, partial=True)
        
        if profile_serializer.is_valid():
            profile = profile_serializer.save()
            profile.daily_calories_target = self.calculate_calories(profile)
            
            profile.save()
            
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile': UserProfileSerializer(profile).data
            }, status=status.HTTP_200_OK)
            
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def calculate_calories(self, profile):
        if not profile.weight or not profile.height or not profile.gender:
            return profile.daily_calories_target
        
        weight = float(profile.weight)
        height = float(profile.height)
        age = profile.age if profile.age else 30
        
        
        if profile.gender == 'M':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
        tdee = bmr * 1.55
        
        if profile.goal == 'cut':
            target = tdee - (tdee * 0.1)
        elif profile.goal == 'bulk':
            target = tdee + (tdee * 0.1)
        else:
            target = tdee

        return int(round(target))
        