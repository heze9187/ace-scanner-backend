# scanner/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SignupViewSet, CourtViewSet, UserPreferenceViewSet, CourtAvailabilityViewSet, ScrapeAvailabilityViewSet, whoami

router = DefaultRouter()
router.register(r'signup', SignupViewSet, basename='signup')
router.register(r'courts', CourtViewSet, basename='court')
router.register(r'preferences', UserPreferenceViewSet, basename='preference')
router.register(r'availabilities', CourtAvailabilityViewSet, basename='availability')
router.register(r'scrape', ScrapeAvailabilityViewSet, basename='scrape')

urlpatterns = router.urls

urlpatterns += [
    path('whoami/', whoami, name='whoami'),
]