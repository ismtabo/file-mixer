from .models import Problem


class UnsavedModifiedProblem(Exception):
    def __init__(self, message):
        super(UnsavedModifiedProblem, self).__init__(message)


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
        self._path = new_path

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

    @property
    def answer_extensions(self):
        return self._answer_extensions

    def add_choosen_file(self, file_name):
        pass
