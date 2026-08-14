from rest_framework import viewsets
from django.contrib.auth.models import User
from userProfile.models import UserProfile
from workouts.models import Exercise, WorkoutSession, WorkoutSet
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    ExerciseSerializer, 
    WorkoutSessionSerializer, 
    WorkoutSetSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer

class WorkoutSetViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSet.objects.all()
    serializer_class = WorkoutSetSerializer    