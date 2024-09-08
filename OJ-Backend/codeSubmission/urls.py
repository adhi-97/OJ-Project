from django.urls import path
from .views import submit_code,test_code

urlpatterns = [
    path('problem/submit-code/', submit_code, name='submit_code'),
    path('problem/submit-code-test/', test_code, name='test_code'),
]
