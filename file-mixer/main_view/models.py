from collections import namedtuple
from .errors import NoneCurrentProblemSavePath

FolderTreeElement = namedtuple('FolderTreeElement',
                               ['f', 'size', 'is_folder', 'fullname', 'children'])
ProblemFile = namedtuple('ProblemFile', ['input', 'answer'])


class Problem:
    def __init__(self, problemid, used_files=None):
        self._problemid = problemid
        self._path = None
        self._used_files = used_files or []
        self._input = ""
        self._answer = ""

    @property
    def number(self):
        return "p{0}".format(self._problemid)

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
        return """Problem Id: {}""".format(self.number)
