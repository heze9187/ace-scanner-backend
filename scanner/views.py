# scanner/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.core.management import call_command
from django.http import JsonResponse
from django.middleware.csrf import get_token
from .models import User, Court, UserPreference, CourtAvailability
from .serializer import CourtSerializer, UserPreferenceSerializer, CourtAvailabilitySerializer
from django.conf import settings

# --- Authentication Helpers ---

@api_view(['GET'])
def whoami(request):
    if request.user.is_authenticated:
        return Response({'is_authenticated': True, 'username': request.user.username})
    else:
        return Response({'is_authenticated': False})

class SignupView(APIView):
    permission_classes = [AllowAny]

    @csrf_protect
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'message': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully.'})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def api_login(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({'message': 'Login success'})
    else:
        return JsonResponse({'message': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def api_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout success'})


def get_csrf_token(request):
    csrf_token = get_token(request)
    response = JsonResponse({'message': 'CSRF cookie set'})

    cookie_settings = {
        'key': 'csrftoken',
        'value': csrf_token,
        'secure': True,
        'httponly': False,
        'samesite': 'None',
        'path': '/',
    }

    # If production, set domain
    if settings.ENVIRONMENT == 'production':
        cookie_settings['domain'] = 'ace-scanner-frontend.onrender.com'  # 🔥 Only add domain in production

    response.set_cookie(**cookie_settings)
    return response

def csrf_failure(request, reason=""):
    return JsonResponse({'detail': 'CSRF Failed: ' + str(reason)}, status=403)

# --- Main Application APIs ---

class CourtViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
    permission_classes = [permissions.AllowAny]  # Publicly viewable courts

class UserPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CourtAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourtAvailability.objects.all().order_by('date', 'time')
    serializer_class = CourtAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

class ScrapeAvailabilityViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        call_command('scrape_availability')
        return Response({'message': 'Scraping started successfully'})