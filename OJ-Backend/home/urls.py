from django.urls import path
from home.views import all_problems,problem_detail

urlpatterns = [
    path("problems/", all_problems, name="all-problems"),
    path("problems/<int:problem_id>/", problem_detail, name="problem-detail"),

]
