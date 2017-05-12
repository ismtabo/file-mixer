import os

from .models import Problem
from .errors import UnsavedModifiedProblem

class MainViewModel:

    def __init__(self):

        self._path = None
        self._is_modified = False
        self._problem = None
        self._input_extensions = []
        self._answer_extensions = []

    @property
    def current_path(self):

        return self._path

    @current_path.setter
    def current_path(self, new_path):
        print("Change path {} to {}".format(self._path, new_path))
        self._path = new_path

    def get_file_path(self, basepath):
        print("Real path for {}, in {}".format(basepath, self._path))
        return os.path.join(self._path, basepath)

    @property
    def current_problem(self):

        return self._problem

    @current_problem.setter
    def current_problem(self, new_problem_id, choosenfiles):

        if self._is_modified and self._problem:
            raise UnsavedModifiedProblem('Current problem should be saved before open new one.')

        self._problem = Problem(new_problem_id, choosenfiles)

    @property
    def input_extensions(self):

        return self._input_extensions

    def add_input_extensions(self, *new_input_extensions):

        self._input_extensions += new_input_extensions

    @property
    def answer_extensions(self):

        return self._answer_extensions

    def add_answer_extensions(self, *new_answer_extensions):

        self._answer_extensions += new_answer_extensions

    def add_choosen_file(self, file_name):
        print('Choosen file: ', file_name)
        pass
