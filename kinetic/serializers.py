from rest_framework import serializers
from django.contrib.auth.models import User
from userProfile.models import UserProfile
from workouts.models import Exercise, WorkoutSession, WorkoutSet

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'weight', 'height', 'goal', 'daily_calories_target']
        
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        
    def create(self, validated_data):
        
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        
        if password:
            user.set_password(password)
            user.save()
            
        return user
        
class ExerciseSerializer(serializers.ModelSerializer):
    muscle_group_display = serializers.CharField(source='get_muscle_group_display', read_only=True)
    
    class Meta: 
        model = Exercise
        fields = ['id', 'name', 'muscle_group', 'muscle_group_display', 'image']
        

class WorkoutSetSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    
    class Meta:
        model = WorkoutSet
        fields = ['id', 'exercise', 'exercise_name', 'set_number', 'weight', 'reps']
        
class WorkoutSessionSerializer(serializers.ModelSerializer):
    sets = WorkoutSetSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = WorkoutSession
        fields = ['id', 'user', 'date', 'notes', 'sets']