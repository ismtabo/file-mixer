import os

from collections import namedtuple
from .errors import NoneCurrentProblemSavePath
from .patterns import Serializable

FolderTreeElement = namedtuple('FolderTreeElement',
                               ['f', 'size', 'is_folder', 'fullname', 'children'])
ProblemFile = namedtuple('ProblemFile', ['input', 'answer'])


class Problem(Serializable):
    def __init__(self, problemid, used_files=None):
        self._problemid = problemid
        self._path = None
        self._used_files = used_files or []
        self._input = ""
        self._answer = ""

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

    def add_used_files(self, input_file_name, answer_file_name):
        self._used_files += [ProblemFile(input_file_name, answer_file_name)]

    def remove_used_files(self, file_name):
        self._used_files = [ProblemFile(input_file_name, answer_file_name) for input_file_name, answer_file_name in self._used_files if not file_name in input_file_name]

    def generate(self):
        self._input = ""
        self._answer = ""

        for input_file, answer_file in self._used_files:
            with open(input_file, 'r') as file:
                self._input += file.read()

            with open(answer_file, 'r') as file:
                self._answer += file.read()

    def clear(self):

        self._input = ""
        self._answer = ""
        self._used_files.clear()

    @property
    def files_content(self):
        self.generate()
        return self._input, self._answer

    def __str__(self):
        return "p{0}".format(self.number)

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

        return Problem(marshall['number'], problem_used_files)
