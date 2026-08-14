from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from.views import (
    UserViewSet,
    UserProfileViewSet,
    ExerciseViewSet,
    WorkoutSessionViewSet,
    WorkoutSetViewSet
)

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'workouts', WorkoutSessionViewSet)
router.register(r'workout-sets', WorkoutSetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)