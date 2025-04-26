# scanner/serializers.py
from rest_framework import serializers
from .models import Court, UserPreference, CourtAvailability

class CourtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = '__all__'

class UserPreferenceSerializer(serializers.ModelSerializer):
    court = CourtSerializer(read_only=True)  # Used for GET
    court_id = serializers.PrimaryKeyRelatedField(
        queryset=Court.objects.all(), source='court', write_only=True
    )  # Used for POST

    class Meta:
        model = UserPreference
        fields = [
            'id',
            'court',
            'court_id',
            'weekday_start',
            'weekday_end',
            'weekend_start',
            'weekend_end',
            'receive_email',
            'user',
        ]
        extra_kwargs = {
            'user': {'read_only': True},
        }

class CourtAvailabilitySerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source='court.name', read_only=True)

    class Meta:
        model = CourtAvailability
        fields = ['id', 'court_name', 'date', 'time']