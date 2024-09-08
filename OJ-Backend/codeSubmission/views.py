from django.shortcuts import get_object_or_404
from codeSubmission.models import CodeSubmission
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pathlib import Path
import uuid
import subprocess
import json
import os


@login_required
@require_http_methods(["POST"])
def submit_code(request):
    try:
        # Parse JSON data from the request
        data = json.loads(request.body)
        language = data.get('language')
        code = data.get('code')
        input_data = data.get('input_data', '')

        # Validate input
        if not language or not code:
            return JsonResponse({'error': 'Language and code are required fields.'}, status=400)

        # Run the code and get output
        output = run_code(language, code, input_data)

        # Save the submission to the database
        submission = CodeSubmission.objects.create(
            language=language,
            code=code,
            input_data=input_data,
            output_data=output
        )

        # Prepare the response data
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


@login_required
@require_http_methods(["POST"])
def test_code(request):
    try:
        # Parse JSON data from the request
        data = json.loads(request.body)
        language = data.get('language')
        code = data.get('code')
        input_data = data.get('input_data', '')
        problem_id = data.get('problem_id')

        # Validate input
        if not language or not code:
            return JsonResponse({'error': 'Language and code are required fields.'}, status=400)
        
        # Construct the path to the test cases file based on problem ID
        test_cases_file_path = os.path.join(settings.BASE_DIR, 'tests', f'problem_{problem_id}', 'test_cases.json')
        if not os.path.exists(test_cases_file_path):
            return JsonResponse({'error': f'Test cases file for problem {problem_id} not found.'}, status=404)

        # Load test cases from the file
        with open(test_cases_file_path, 'r') as file:
            test_cases = json.load(file)

        # Run the code against the test cases and get results
        results = run_code_test(language, code, test_cases)

        # Save the submission to the database
        submission = CodeSubmission.objects.create(
            language=language,
            code=code,
            input_data='',
            output_data=json.dumps(results)  # Save the detailed results
        )

        # Prepare the response data
        response_data = {
            'id': submission.id,
            'language': submission.language,
            'code': submission.code,
            'input_data': submission.input_data,
            'output_data': results,
            'success': all(result['success'] for result in results),  # Check if all test cases passed
        }
        return JsonResponse(response_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def run_code_test(language, code, test_cases):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    # Ensure necessary directories exist
    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    code_file_path = codes_dir / code_file_name

    # Write the submitted code to a file
    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    # Prepare to store results
    results = []

    for index, test_case in enumerate(test_cases):
        input_data = test_case['input']
        expected_output = test_case['expected_output']

        input_file_name = f"{unique}_{index}.txt"
        output_file_name = f"{unique}_{index}_output.txt"
        error_file_name = f"{unique}_{index}_error.txt"

        input_file_path = inputs_dir / input_file_name
        output_file_path = outputs_dir / output_file_name
        error_file_path = outputs_dir / error_file_name

        # Write the input data to a file
        with open(input_file_path, "w") as input_file:
            input_file.write(input_data)

        try:
            # Compile and run code based on language
            if language == "cpp":
                executable_path = codes_dir / unique
                compile_result = subprocess.run(
                    ["g++", str(code_file_path), "-o", str(executable_path)],
                    stderr=subprocess.PIPE,
                )
                if compile_result.returncode != 0:
                    error_message = compile_result.stderr.decode()
                    results.append({
                        'test_case': index + 1,
                        'input': input_data,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'error': f"Compilation error: {error_message}",
                        'success': False
                    })
                    continue

                # Run the compiled executable
                with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                    run_result = subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                    )
                    if run_result.returncode != 0:
                        error_message = run_result.stderr.decode()
                        results.append({
                            'test_case': index + 1,
                            'input': input_data,
                            'expected_output': expected_output,
                            'actual_output': '',
                            'error': f"Runtime error: {error_message}",
                            'success': False
                        })
                        continue

            elif language == "python":
                # Run the Python code
                with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                    run_result = subprocess.run(
                        ["python3", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                    )
                    if run_result.returncode != 0:
                        error_message = run_result.stderr.decode()
                        results.append({
                            'test_case': index + 1,
                            'input': input_data,
                            'expected_output': expected_output,
                            'actual_output': '',
                            'error': f"Runtime error: {error_message}",
                            'success': False
                        })
                        continue

            # Read the actual output
            with open(output_file_path, "r") as output_file:
                actual_output = output_file.read()

            # Ensure the comparison is between strings
            success = actual_output.strip() == expected_output.strip()
            results.append({
                'test_case': index + 1,
                'input': input_data,
                'expected_output': expected_output,
                'actual_output': actual_output,
                'error': '',
                'success': success
            })

        except Exception as e:
            # Catch any unexpected errors
            results.append({
                'test_case': index + 1,
                'input': input_data,
                'expected_output': expected_output,
                'actual_output': '',
                'error': f"Execution error: {str(e)}",
                'success': False
            })

    return results

def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"
    error_file_name = f"{unique}_error.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name
    error_file_path = outputs_dir / error_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    try:
        if language == "cpp":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)],
                stderr=subprocess.PIPE,  # Capture stderr
            )
            if compile_result.returncode != 0:
                with open(error_file_path, "w") as error_file:
                    error_file.write(compile_result.stderr.decode())
                return f"Compilation error: {compile_result.stderr.decode()}"

            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    run_result = subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,  # Capture stderr
                    )
                    if run_result.returncode != 0:
                        with open(error_file_path, "w") as error_file:
                            error_file.write(run_result.stderr.decode())
                        return f"Runtime error: {run_result.stderr.decode()}"

        elif language == "python":
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    run_result = subprocess.run(
                        ["python3", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,  # Capture stderr
                    )
                    if run_result.returncode != 0:
                        with open(error_file_path, "w") as error_file:
                            error_file.write(run_result.stderr.decode())
                        return f"Runtime error: {run_result.stderr.decode()}"

    except Exception as e:
        return f"Execution error: {str(e)}"

    # Read the output from the output file
    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()

    # Read any error messages from the error file
    error_data = ""
    if error_file_path.exists():
        with open(error_file_path, "r") as error_file:
            error_data = error_file.read()

    if error_data:
        return f"Error: {error_data}"

    return output_data
