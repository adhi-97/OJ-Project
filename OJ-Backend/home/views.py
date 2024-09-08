from django.shortcuts import get_object_or_404
from home.models import problem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

@login_required
def all_problems(request):
    all_problems = problem.objects.all().values('id', 'statement', 'name', 'code', 'difficulty')
    problems_list = list(all_problems)
    return JsonResponse({'all_problems': problems_list})

@login_required
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