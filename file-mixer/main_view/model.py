import os
import stat

from .models import Problem, FolderTreeElement
from .errors import UnsavedModifiedProblem, NoneCurrentProblem


class MainViewModel:

    def __init__(self):

        self._path = None
        self._pathtree = None
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
        self.current_pathtree = new_path

    def get_file_path(self, basepath):
        print("Real path for {}, in {}".format(basepath, self._path))
        return os.path.join(self._path, basepath)

    @property
    def current_pathtree(self):

        return self._pathtree

    @current_pathtree.setter
    def current_pathtree(self, new_path: str):

        def dirwalk(path):
            pathtree = []

            # Iterate over the contents of the specified path
            for f in os.listdir(path):
                # Get the absolute path of the item
                fullname = os.path.join(path, f)
                # Extract metadata from the item
                fdata = os.stat(fullname)
                # Determine if the item is a folder
                is_folder = stat.S_ISDIR(fdata.st_mode)
                # If the item is a folder, descend into it
                children = dirwalk(fullname) if is_folder else []
                # Append the item to the TreeStore
                li = FolderTreeElement(f, fdata.st_size, is_folder, fullname, children)
                pathtree.append(li)

            return pathtree

        self._pathtree = dirwalk(new_path)

    @property
    def current_problem(self):

        if not self._problem:
            raise NoneCurrentProblem('There is not current problem.')

        return self._problem

    def set_new_problem(self, problem):

        if self._is_modified:
            raise UnsavedModifiedProblem('Current problem should be saved before open new one.')

        del self._problem
        self._problem = problem
        self._is_modified = False

    def set_problem_number(self, new_problem_number):

        if not self._problem:
            raise NoneCurrentProblem('There is not current problem.')

        self._problem.number = new_problem_number
        self._is_modified = True

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

    def add_choosen_file(self, input_file_name, answer_file_name):
        print('Choosen file: ', input_file_name)
        if not self._problem:
            raise NoneCurrentProblem("There is not current problem.\nPlease entry problem number.")

        self._problem.add_used_files(input_file_name, answer_file_name)
        self._is_modified = True

    def remove_choosen_file(self, file_name=None, file_index=None):
        if file_name is None and file_index is None:
            raise Exception('Either file name or file index has to be given')

        print('Remove choosen file: ', file_name)
        if not self._problem:
            raise NoneCurrentProblem("There is not current problem.\nPlease entry problem number.")

        self._problem.remove_used_files(file_index)
        self._is_modified = True
        self._problem.generate()

    def sort_choosen_files(self):
        if not self._problem:
            raise NoneCurrentProblem("There is not current problem.\nPlease entry problem number.")
        self._problem.sort()
        self._problem.generate()

    def shuffle_choosen_files(self):
        if not self._problem:
            raise NoneCurrentProblem("There is not current problem.\nPlease entry problem number.")
        self._problem.shuffle()
        self._problem.generate()

    @property
    def current_problem_files_content(self):

        return self._problem.files_content

    @property
    def current_problem_choosenfiles(self):

        return self._problem.used_files

    @property
    def current_problem_path(self):

        return self._problem.path

    @current_problem_path.setter
    def current_problem_path(self, new_problem_save_path):
        self._problem.path = new_problem_save_path
        self._is_modified = True

    def set_problem_saved(self):
        self._is_modified = False
