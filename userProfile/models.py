from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    USER_GOALS = [
        ('cut', 'Definición'),
        ('bulk', 'Volumen'),
        ('maintenance', 'Mantenimiento'),
    ]
    GENDER_CHOICE = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True, help_text="Edad en años")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kg", blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Altura en cm", blank=True, null=True)
    goal = models.CharField(max_length=20, choices=USER_GOALS, default='maintenance')
    daily_calories_target = models.PositiveIntegerField(default=2000)

    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()