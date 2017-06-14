import os
import json

from .models import Problem
from .model import MainViewModel
from .errors import NoneAnswerForInputFile, NoneCurrentProblem, ChoosenFileHasNotInputExtension, \
    NoneCurrentProblemSavePath


class MainViewController(object):
    """docstring for MainViewController."""

    def __init__(self, view):

        super(MainViewController, self).__init__()
        self.view = view
        self.model = MainViewModel()
        self.model.add_input_extensions('in')
        self.model.add_answer_extensions('ans')
        self.view.update_extension_treeviews(self.model.input_extensions,
                                             self.model.answer_extensions)

    def problem_number_changed(self, new_problem_number):

        try:
            self.model.set_problem_number(int(new_problem_number))
            self.view.update_problem_number(self.model.current_problem.number)
        except NoneCurrentProblem as err:
            self.model.set_new_problem(Problem(int(new_problem_number)))

    def problem_number_focus_out(self, new_problem_number):

        if not new_problem_number:
            try:
                problem_number = self.model.current_problem.number
            except NoneCurrentProblem as err:
                problem_number = 0
            self.view.update_problem_number(problem_number)

    def new_problem_file(self):

        problem_number = int(self.view.open_entry_dialog())

        if problem_number:
            self.model.set_new_problem(Problem(problem_number))
            self.view.update_problem_number(problem_number)
            self.view.update_choosen_files_tree_view(self.model.current_problem_choosenfiles)
            self.view.update_problem_content(*self.model.current_problem_files_content)

    def open_problem_file(self):

        problem_file_path = self.view.open_file_dialog()

        if problem_file_path:
            content = self._open_file(problem_file_path)
            marshall_problem = json.loads(content)

            self.model.set_new_problem(Problem.unserialize(marshall_problem))
            self.view.update_problem_number(str(self.model.current_problem.number))
            self.view.update_choosen_files_tree_view(self.model.current_problem_choosenfiles)
            self.view.update_problem_content(*self.model.current_problem_files_content)


    def open_folder(self):

        new_path = self.view.open_folder_dialog(os.path.expanduser('~'))

        if new_path:
            self.model.current_path = new_path
            self.view.update_folder_treeview(self.model.current_pathtree)

    def add_choosen_file(self, file_path):

        base_path, file_basename = os.path.split(file_path)
        file_name, extension = os.path.splitext(file_basename)

        if extension[1:] not in self.model.input_extensions:
            raise ChoosenFileHasNotInputExtension("Please choose another file or add input extension")

        for extension in self.model.answer_extensions:
            answer_file_path = os.path.join(base_path, "{}.{}".format(file_name, extension))
            if os.path.exists(self.model.get_file_path(answer_file_path)):
                _file_name = answer_file_path
                break
        else:
            _file_name = self.view.open_file_dialog(os.path.expanduser(base_path))
            if not _file_name:
                raise NoneAnswerForInputFile("Selected input file has not paired answer file.")
            if self.view.open_confirmation_dialog("¿Desea añadir la extensión a la lista?"):
                _, extension = os.path.splitext(os.path.basename(_file_name))
                if extension:
                    self.model.add_answer_extensions(extension[1:])
                    self.view.update_extension_treeviews(self.model.input_extensions, self.model.answer_extensions)

        if not self.model.current_problem:
            raise NoneCurrentProblem("Please input problem number")

        self.model.add_choosen_file(file_path, _file_name)

        self.view.update_choosen_files_tree_view(self.model.current_problem_choosenfiles)
        self.view.update_problem_content(*self.model.current_problem_files_content)

    def remove_choosen_file(self, file_path):

        file_name, _ = os.path.splitext(file_path)
        self.model.remove_choosen_file(file_path)

        self.view.update_choosen_files_tree_view(self.model.current_problem_choosenfiles)
        self.view.update_problem_content(*self.model.current_problem_files_content)

    def add_input_extension(self, new_input_extension):

        if not new_input_extension in self.model.input_extensions:
            self.model.add_input_extensions(new_input_extension)
            self.view.update_extension_treeviews(self.model.input_extensions,
                                                 self.model.answer_extensions)

    def add_answer_extension(self, new_answer_extension):

        if not new_answer_extension in self.model.answer_extensions:
            self.model.add_answer_extensions(new_answer_extension)
            self.view.update_extension_treeviews(self.model.input_extensions,
                                                 self.model.answer_extensions)

    def save_problem(self, force_ask_path=False):

        if force_ask_path:
            problem_path = self._ask_current_problem_path()
            self.model.current_problem_path = problem_path

        try:
            problem_path = self.model.current_problem_path
        except NoneCurrentProblemSavePath as err:
            problem_path = self._ask_current_problem_path()
            self.model.current_problem_path = problem_path

        problem_serial_filename = "p{0}.prob".format(self.model.current_problem.number)
        problem_serial_content = json.dumps(self.model.current_problem.serialize())

        problem_input_filename = "p{0}.in".format(self.model.current_problem.number)
        problem_answer_filename = "p{0}.ans".format(self.model.current_problem.number)
        problem_input_content, problem_answer_content = self.model.current_problem_files_content

        self._save_file(self.model.current_path, problem_serial_filename, problem_serial_content)
        self._save_file(self.model.current_path, problem_input_filename, problem_input_content)
        self._save_file(self.model.current_path, problem_answer_filename, problem_answer_content)
        self.model.set_problem_saved()

    def _ask_current_problem_path(self):

        problem_path = self.view.open_folder_dialog(self.model.current_path, save=True)
        return problem_path

    def _open_file(self, path):

        with open(path, 'r') as file:
            content = file.read()

        return content

    def _save_file(self, path, filename, content):

        with open(os.path.join(path, filename), 'w') as file:
            file.write(content)
