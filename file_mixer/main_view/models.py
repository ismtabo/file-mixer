import os
import random
from mmap import mmap

from collections import namedtuple

import time

from .errors import NoneCurrentProblemSavePath
from .patterns import Serializable

FolderTreeElement = namedtuple('FolderTreeElement',
                               ['f', 'size', 'is_folder', 'fullname', 'children'])
ProblemFile = namedtuple('ProblemFile', ['input', 'answer'])


class Problem(Serializable):
    def __init__(self, problemid=0, used_files=None):
        super().__init__()
        self._problemid = problemid
        self._path = None
        self._input = ""
        self._answer = ""
        self._used_files = []
        self._used_files_mm = []
        self.used_files = used_files or []

    def __del__(self):
        self.clear()

    @property
    def number(self):
        return self._problemid

    @number.setter
    def number(self, new_number):
        self._problemid = new_number

    @property
    def path(self):

        if not self._path:
            raise NoneCurrentProblemSavePath("Please select save path to current problem")
        return self._path

    @path.setter
    def path(self, new_path):

        self._path = new_path

    @property
    def used_files(self):
        return self._used_files

    @used_files.setter
    def used_files(self, new_used_files):
        if self.used_files:
            del self.used_files
        for input_file_name, answer_file_name in new_used_files:
            self.add_used_files(input_file_name, answer_file_name)

    @used_files.deleter
    def used_files(self):
        self._used_files.clear()
        for input_mm, answer_mm in self._used_files_mm:
            input_mm.close()
            answer_mm.close()
        self._used_files_mm.clear()

    def add_used_files(self, input_file_name, answer_file_name):
        self._used_files += [ProblemFile(input_file_name, answer_file_name)]
        with open(input_file_name, 'r+') as file:
            input_file_mm = mmap(file.fileno(), 0)
            input_content = file.read()
        with open(answer_file_name, 'r+') as file:
            answer_file_mm = mmap(file.fileno(), 0)
            answer_content = file.read()
        self._input = ''.join([self._input, input_content])
        self._answer = ''.join([self._answer, answer_content])
        self._used_files_mm += [ProblemFile(input_file_mm, answer_file_mm)]

    def remove_used_files(self, file_iter):
        del self._used_files[file_iter]
        input_file_mm, answer_file_mm = self._used_files_mm[file_iter]
        input_file_mm.close()
        answer_file_mm.close()
        del self._used_files_mm[file_iter]

    def sort(self):
        _used_files = list(zip(self._used_files, self._used_files_mm))
        _used_files.sort()

        self._used_files.clear()
        self._used_files_mm.clear()

        for files, mm_files in _used_files:
            self._used_files.append(files)
            self._used_files_mm.append(mm_files)

    def shuffle(self):
        random.seed(time.time())
        _used_files = list(zip(self._used_files, self._used_files_mm))
        random.shuffle(_used_files)

        self._used_files.clear()
        self._used_files_mm.clear()

        for files, mm_files in _used_files:
            self._used_files.append(files)
            self._used_files_mm.append(mm_files)

    def generate(self):
        self._input = ""
        self._answer = ""

        for input_file_mm, answer_file_mm in self._used_files_mm:
            input_file_mm.seek(0)
            self._input += input_file_mm.read().decode('ascii')
            answer_file_mm.seek(0)
            self._answer += answer_file_mm.read().decode('ascii')

    def clear(self):
        self._input = ""
        self._answer = ""
        del self.used_files

    @property
    def files_content(self):
        return self._input, self._answer

    def serialize(self):
        return {
            'number': self.number,
            'used_files': [
                {
                    'input': inputfilename,
                    'output': outputfilename
                }
                for inputfilename, outputfilename
                in self.used_files
            ]
        }

    @staticmethod
    def unserialize(marshall):

        problem_used_files = [
            ProblemFile(problemfile['input'], problemfile['output'])
            for problemfile in marshall.get('used_files', [])
            if all(map(os.path.exists, problemfile.values()))
        ]

        ProblemClass = Problem if not 'case_numbered' in marshall else NumberedProblem

        return ProblemClass(marshall['number'], problem_used_files)


class NumberedProblem(Problem):

    def __init__(self, *args, **kwargs):
        self._test_cases = 0
        super().__init__(*args, **kwargs)

    # TODO: override first line of input contains number of test cases
    def add_used_files(self, input_file_name, answer_file_name):
        self._used_files += [ProblemFile(input_file_name, answer_file_name)]
        with open(input_file_name, 'r+') as file:
            input_file_mm = mmap(file.fileno(), 0)
            self._test_cases += int(file.readline().strip())
            input_content = file.read()
        with open(answer_file_name, 'r+') as file:
            answer_file_mm = mmap(file.fileno(), 0)
            answer_content = file.read()
        if len(self._input.split('\n', 1)) > 2:
            self._input = '{0}\n{1}{2}'.format(self._test_cases, self._input.split('\n', 1)[1], input_content)
        else:
            self._input = '{0}\n{1}'.format(self._test_cases, input_content)
        self._answer = ''.join([self._answer, answer_content])
        self._used_files_mm += [ProblemFile(input_file_mm, answer_file_mm)]

    # TODO: override first line of input contains number of test cases
    def generate(self):
        self._test_cases = 0
        self._input = ""
        self._answer = ""

        for input_file_mm, answer_file_mm in self._used_files_mm:
            input_file_mm.seek(0)
            self._test_cases += int(input_file_mm.readline().decode('ascii').strip())
            self._input += input_file_mm.read().decode('ascii')
            answer_file_mm.seek(0)
            self._answer += answer_file_mm.read().decode('ascii')

        self._input = "{0}\n".format(self._test_cases) + self._input

    def serialize(self):
        serialization = super().serialize()
        serialization.update({'case_numbered': True})
        return serialization
    
    def get_problem(self):
        return Problem(problemid=self.number, used_files=self.used_files)

    @classmethod
    def from_problem(self, problem):
        return NumberedProblem(problemid=problem.number, used_files=problem.used_files)