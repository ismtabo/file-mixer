
class UnsaveModifiedProblem(Exception):

    def __init__(self, message, errors):
        super(UnsavedModifiedProblem, self).__init__(message)
        self.errors = errors


class MainViewModel:

    def __init__(self):

        self._path = None
        self._is_modified = False
        self._problem = None


    @property
    def current_path():
        return self._path


    @current_path.setter
    def current_path(new_path):
        self._path = new_path


    @property
    def current_problem():
        return self._problem

    @current_problem.setter
    def current_problem(new_problem_id, choosenfiles):
        if self._is_modified and self._problem:
            raise
