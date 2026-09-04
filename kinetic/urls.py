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
    WorkoutSetViewSet,
    RoutineViewSet
)

from userProfile.views import (
    CookieTokenObtainPairView,
    CookieTokenLogoutView,
    CookieTokenRefreshView,
    UserProfileView
)

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'workouts', WorkoutSessionViewSet)
router.register(r'workout-sets', WorkoutSetViewSet)
router.register(r'routines', RoutineViewSet, basename='routine')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/users/me/', UserProfileView.as_view(), name='user_profile'),

    path('api/', include(router.urls)),
    
    path('api/auth/login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', CookieTokenLogoutView.as_view(), name='token_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)