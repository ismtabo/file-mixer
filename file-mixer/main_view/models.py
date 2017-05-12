import ntpath
from collections import namedtuple
from typing import List

FilePaths = namedtuple('FilePaths', ['input', 'answer'])


class ProblemFile():

    def __init__(self, input_path, answer_path):

        self._input_path = input_path
        self._answer_path = answer_path

    @property
    def paths(self):

        return FilePaths(self._input_path, self._answer_path)

    @paths.setter
    def path(self, new_input_path, new_answer_path):

        self._input_path = new_input_path
        self._answer_path = new_answer_path

    @property
    def name(self):

        return ntpath.basename(self._input_path)


class Problem:

    def __init__(self, problemid: str, used_files: List[ProblemFile]):

        self._problemid = problemid
        self._used_files = used_files
        self._input = ""
        self._answer = ""

    @property
    def name(self):

        return 'p' + self._problemid

    def generate(self):

        for input_file, answer_file in self._used_files:
            with open(input_file, 'r') as file:
                self._input += file.read()

            with open(answer_file, 'r') as file:
                self._answer += file.read()

    def clear(self):

        self._input = ""
        self._answer = ""
        self._used_files.clear()

    def __str__(self):

        return """Problem Id: {}""".format(self.name)
