from django.shortcuts import get_object_or_404
from home.models import problem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_problems(request):
    all_problems = problem.objects.all().values('id', 'statement', 'name', 'code', 'difficulty')
    problems_list = list(all_problems)
    return JsonResponse({'all_problems': problems_list})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def problem_detail(request, problem_id):
    req_problem = get_object_or_404(problem, id=problem_id)
    problem_data = {
            'id': req_problem.id,
            'statement': req_problem.statement,
            'name': req_problem.name,
            'code': req_problem.code,
            'difficulty': req_problem.difficulty
        }
    return JsonResponse(problem_data)