from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User with this username already exists'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return JsonResponse({'message': 'User created successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
        
        login(request, user)
        return JsonResponse({'message': 'Login successful'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def logout_user(request):
    try:
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
