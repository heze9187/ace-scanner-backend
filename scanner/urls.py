# scanner/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    SignupView,
    CourtViewSet,
    UserPreferenceViewSet,
    CourtAvailabilityViewSet,
    ScrapeAvailabilityViewSet,
    whoami,
    api_login,
    api_logout,
    get_csrf_token,
)

router = DefaultRouter()
router.register(r'courts', CourtViewSet, basename='court')
router.register(r'preferences', UserPreferenceViewSet, basename='preference')
router.register(r'availabilities', CourtAvailabilityViewSet, basename='availability')
router.register(r'scrape', ScrapeAvailabilityViewSet, basename='scrape')

urlpatterns = router.urls + [
    path('signup/', SignupView.as_view(), name='signup'),   # <-- ✅ now it's a direct path!
    path('auth/login/', api_login, name='api-login'),        # <-- ✅ login
    path('auth/logout/', api_logout, name='api-logout'),     # <-- ✅ logout
    path('csrf/', get_csrf_token, name='get-csrf-token'),    # <-- ✅ csrf
    path('whoami/', whoami, name='whoami'),                  # <-- ✅ whoami
]