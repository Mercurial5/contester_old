from typing import List
import subprocess
import uuid
import os


class Compiler:

    def __init__(self, code: str):
        self.directory_path = os.path.join(os.getcwd(), 'contester')
        self.directory_path = os.path.join(self.directory_path, 'compiler')
        self.directory_path = os.path.join(self.directory_path, 'temp')
        self.filename = uuid.uuid4().hex
        self.absolute_path_to_file = os.path.join(self.directory_path, self.filename + '.cpp')
        self.absolute_path_to_runner = os.path.join(self.directory_path, self.filename + '.out')
        self.code = code

    def create(self):
        with open(self.absolute_path_to_file, 'w', encoding='utf-8') as file:
            file.write(self.code)

        compile_commands = ['g++', self.absolute_path_to_file, '-o', self.absolute_path_to_runner]
        compilation_result = subprocess.run(compile_commands, stderr=subprocess.PIPE)
        if compilation_result.stderr.decode('utf-8') != '':
            return {
                'status': False,
                'error': 'Compilation Error',
                'log': compilation_result.stderr.decode('utf-8')
            }

        return {
            'status': True
        }

    def compile(self, input_values: List[str] = []):

        command = [self.absolute_path_to_runner]
        program = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        for value in input_values:
            program.stdin.write((value + '\n').encode('utf-8'))
        program.stdin.flush()

        stdout = program.stdout.read()
        stderr = program.stderr.read()

        if stderr.decode('utf-8') != '':
            return {
                'status': False,
                'error': 'Runtime Error',
                'log': stderr.decode('utf-8')
            }

        return {
            'status': True,
            'answer': stdout.decode('utf-8')
        }

    def __del__(self):
        if os.path.exists(self.absolute_path_to_file):
            os.remove(self.absolute_path_to_file)
        if os.path.exists(self.absolute_path_to_runner):
            os.remove(self.absolute_path_to_runner)
