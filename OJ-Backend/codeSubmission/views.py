from django.shortcuts import get_object_or_404
from codeSubmission.models import CodeSubmission
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from pathlib import Path
import uuid
import subprocess
import json
import os

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_code(request):
    try:
        data = json.loads(request.body)
        language = data.get('language')
        code = data.get('code')
        input_data = data.get('input_data', '')

        if not language or not code:
            return JsonResponse({'error': 'Language and code are required fields.'}, status=400)

        output = run_code(language, code, input_data)

        submission = CodeSubmission.objects.create(
            language=language,
            code=code,
            input_data=input_data,
            output_data=output
        )

        response_data = {
            'id': submission.id,
            'language': submission.language,
            'code': submission.code,
            'input_data': submission.input_data,
            'output_data': submission.output_data
        }
        return JsonResponse(response_data, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_code(request):
    try:
        data = json.loads(request.body)
        language = data.get('language')
        code = data.get('code')
        problem_id = data.get('problem_id')

        if not language or not code:
            return JsonResponse({'error': 'Language and code are required fields.'}, status=400)
        
        test_cases_file_path = os.path.join(settings.BASE_DIR, 'tests', f'problem_{problem_id}', 'test_cases.json')
        if not os.path.exists(test_cases_file_path):
            return JsonResponse({'error': f'Test cases file for problem {problem_id} not found.'}, status=404)

        with open(test_cases_file_path, 'r') as file:
            test_cases = json.load(file)

        results = run_code_test(language, code, test_cases)

        submission = CodeSubmission.objects.create(
            language=language,
            code=code,
            input_data='',
            output_data=json.dumps(results)
        )

        response_data = {
            'id': submission.id,
            'language': submission.language,
            'code': submission.code,
            'input_data': submission.input_data,
            'output_data': results,
            'success': all(result['success'] for result in results),
        }
        return JsonResponse(response_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    unique = str(uuid.uuid4())
    code_file_path = (project_path / "codes" / f"{unique}.{language}").resolve()
    input_file_path = (project_path / "inputs" / f"{unique}.txt").resolve()
    output_file_path = (project_path / "outputs" / f"{unique}.txt").resolve()
    error_file_path = (project_path / "outputs" / f"{unique}_error.txt").resolve()

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    try:
        if language == "cpp":
            executable_path = (project_path / "codes" / unique).resolve()
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)],
                stderr=subprocess.PIPE,
                timeout=3
            )
            if compile_result.returncode != 0:
                with open(error_file_path, "w") as error_file:
                    error_file.write(compile_result.stderr.decode())
                return f"Compilation error: {compile_result.stderr.decode()}"

            run_result = subprocess.run(
                [str(executable_path)],
                stdin=open(input_file_path),
                stdout=open(output_file_path, "w"),
                stderr=subprocess.PIPE,
                timeout=3
            )
            if run_result.returncode != 0:
                with open(error_file_path, "w") as error_file:
                    error_file.write(run_result.stderr.decode())
                return f"Runtime error: {run_result.stderr.decode()}"

        elif language == "python":
            run_result = subprocess.run(
                ["python3", str(code_file_path)],
                stdin=open(input_file_path),
                stdout=open(output_file_path, "w"),
                stderr=subprocess.PIPE,
                timeout=3
            )
            if run_result.returncode != 0:
                with open(error_file_path, "w") as error_file:
                    error_file.write(run_result.stderr.decode())
                return f"Runtime error: {run_result.stderr.decode()}"

    except subprocess.TimeoutExpired:
        return "Error: Time Limit Exceeded (TLE)."
    except Exception as e:
        return f"Execution error: {str(e)}"

    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()

    if error_file_path.exists():
        with open(error_file_path, "r") as error_file:
            error_data = error_file.read()
            if error_data:
                return f"Error: {error_data}"

    return output_data

def run_code_test(language, code, test_cases):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    unique = str(uuid.uuid4())
    code_file_path = (project_path / "codes" / f"{unique}.{language}").resolve()

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    results = []

    for index, test_case in enumerate(test_cases):
        input_data = test_case['input']
        expected_output = test_case['expected_output']

        input_file_path = (project_path / "inputs" / f"{unique}_{index}.txt").resolve()
        output_file_path = (project_path / "outputs" / f"{unique}_{index}_output.txt").resolve()
        error_file_path = (project_path / "outputs" / f"{unique}_{index}_error.txt").resolve()

        with open(input_file_path, "w") as input_file:
            input_file.write(input_data)

        try:
            if language == "cpp":
                executable_path = (project_path / "codes" / unique).resolve()
                compile_result = subprocess.run(
                    ["g++", str(code_file_path), "-o", str(executable_path)],
                    stderr=subprocess.PIPE,
                    timeout=3
                )
                if compile_result.returncode != 0:
                    results.append({
                        'test_case': index + 1,
                        'input': input_data,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'error': f"Compilation error: {compile_result.stderr.decode()}",
                        'success': False
                    })
                    continue

                run_result = subprocess.run(
                    [str(executable_path)],
                    stdin=open(input_file_path),
                    stdout=open(output_file_path, "w"),
                    stderr=subprocess.PIPE,
                    timeout=3
                )
                if run_result.returncode != 0:
                    results.append({
                        'test_case': index + 1,
                        'input': input_data,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'error': f"Runtime error: {run_result.stderr.decode()}",
                        'success': False
                    })
                    continue

            elif language == "python":
                run_result = subprocess.run(
                    ["python3", str(code_file_path)],
                    stdin=open(input_file_path),
                    stdout=open(output_file_path, "w"),
                    stderr=subprocess.PIPE,
                    timeout=3
                )
                if run_result.returncode != 0:
                    results.append({
                        'test_case': index + 1,
                        'input': input_data,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'error': f"Runtime error: {run_result.stderr.decode()}",
                        'success': False
                    })
                    continue

            with open(output_file_path, "r") as output_file:
                actual_output = output_file.read()

            success = actual_output.strip() == expected_output.strip()
            results.append({
                'test_case': index + 1,
                'input': input_data,
                'expected_output': expected_output,
                'actual_output': actual_output,
                'error': '',
                'success': success
            })

        except subprocess.TimeoutExpired:
            results.append({
                'test_case': index + 1,
                'input': input_data,
                'expected_output': expected_output,
                'actual_output': '',
                'error': 'Time Limit Exceeded (TLE)',
                'success': False
            })
        except Exception as e:
            results.append({
                'test_case': index + 1,
                'input': input_data,
                'expected_output': expected_output,
                'actual_output': '',
                'error': f"Execution error: {str(e)}",
                'success': False
            })

    return results
