# scanner/admin.py
from django.contrib import admin
from .models import Court, UserPreference, CourtAvailability

admin.site.register(Court)
admin.site.register(CourtAvailability)
admin.site.register(UserPreference)
