from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exercise(models.Model):
    MUSCLE_GROUPS = [
        ('chest', 'Pecho'),
        ('back', 'Espalda'),
        ('legs', 'Piernas'),
        ('shoulders', 'Hombros'),
        ('arms', 'Brazos'),
        ('core', 'Abdomen'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    muscle_group = models.CharField(max_length=50, choices=MUSCLE_GROUPS)
    image = models.ImageField(upload_to='exercices/', blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.name} ({self.get_muscle_group_display()})"
    

class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_sessions')
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Entreno de {self.user.username} - {self.date}"
    

class WorkoutSet(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    set_number = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    reps = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.exercise.name}: {self.weight}kg x {self.reps}reps (Serie {self.set_number})"