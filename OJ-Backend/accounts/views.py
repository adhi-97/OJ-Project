from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import json

# Function to get JWT tokens for a user

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Register a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        cpassword = data.get('cpassword')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User with this username already exists'}, status=400)
        
        if password != cpassword:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Generate JWT token
        tokens = get_tokens_for_user(user)

        return JsonResponse({'message': 'User created successfully','tokens': tokens}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Login user and return JWT tokens
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username,password)
        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
        
        # Generate JWT token
        tokens = get_tokens_for_user(user)

        return JsonResponse({
            'message': 'Login successful',
            'tokens': tokens
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Logout user by blacklisting the refresh token (optional)
@api_view(['POST'])
def logout_user(request):
    try:
        # To logout a user in JWT, we typically blacklist the refresh token
        token = request.data.get('refresh_token')

        if token:
            try:
                refresh_token = RefreshToken(token)
                refresh_token.blacklist()  # Blacklist the token
                return JsonResponse({'message': 'Logout successful'}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No refresh token provided'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
