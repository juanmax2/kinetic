from rest_framework import serializers
from django.contrib.auth.models import User
from userProfile.models import UserProfile
from workouts.models import Exercise, WorkoutSession, WorkoutSet, Routine, RoutineExercise


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'age', 'weight', 'height', 'goal', 'daily_calories_target']
        
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
        

class RoutineExerciseSerializer(serializers.ModelSerializer):
    
    exercise_detail = serializers.StringRelatedField(source='exercise', read_only=True)
    
    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())
    
    class Meta:
        model = RoutineExercise
        fields = ['id', 'exercise', 'exercise_detail', 'order', 'target_sets', 'target_reps']
        

class RoutineSerializer(serializers.ModelSerializer):
    routine_exercises = RoutineExerciseSerializer(many=True)
    
    class Meta:
        model = Routine
        fields = ['id', 'user', 'name', 'description', 'created_at', 'routine_exercises']
        read_only_fields = ['user', 'created_at']
        
    def create(self, validated_data):
        exercises_data = validated_data.pop('routine_exercises', [])
        
        user = self.context['request'].user
        routine = Routine.objects.create(user=user, **validated_data)

        for index, exercise_data in enumerate(exercises_data):
            RoutineExercise.objects.create(
                routine=routine,
                order=index,
                **exercise_data
            )
        return routine
        