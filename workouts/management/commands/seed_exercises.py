
import json
import os
from django.core.management.base import BaseCommand
from workouts.models import Exercise

class Command(BaseCommand):
    help = 'Carga masiva de ejercicios desde un archivo JSON'
    
    
    def handle(self, *args, **kwargs):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'exercises.json')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'No se encuentra el archivo en la ruta: {file_path}'))
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            exercises_data = json.load(f)
            
            created_count = 0
            updated_count = 0
            
            for item in exercises_data:
                exercise, created = Exercise.objects.get_or_create(
                    name = item['name'],
                    defaults={
                        'muscle_group': item['muscle_group'],
                        'image': item.get('image')
                    }
                )
                if created:
                    created_count += 1
                else:
                    
                    updated = False
                    if item.get('image') and not exercise.image:
                        exercise.image = item['image']
                        updated = True
                    if updated:
                        exercise.save()
                        updated_count += 1
        self.stdout.write(self.style.SUCCESS(f'Importación completada! Creados: {created_count}, Actualizados: {updated_count}'))
        