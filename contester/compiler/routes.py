from flask import Blueprint, request, current_app
from contester.compiler.compiler import Compiler
import json


app = Blueprint('compiler_bp', __name__)


@app.route('/check_code', methods=['POST'])
def check_code():
    data = json.loads(request.data.decode('utf-8'))

    problem_id = int(data['problem_id'])
    code = data['code']

    samples_db = current_app.config['samples.db']
    samples = samples_db.get_samples(problem_id)

    compiler = Compiler(code)
    result = compiler.create()
    if result['status'] is False:
        return result

    for i, sample in enumerate(samples):
        result = compiler.compile([sample.input])
        if result['status'] is False:
            return result

        output_cases = sample.output.split('%::%')

        accepted = False
        for output_case in output_cases:
            if result['answer'].strip() == output_case:
                accepted = True

        if accepted is False:
            return {
                'status': True,
                'accepted': False,
                'sample_index': i + 1
            }

    return {
        'status': True,
        'accepted': True
    }
