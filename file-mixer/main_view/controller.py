import os

from .model import MainViewModel
from .errors import NoneAnswerForInputFile


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

        print(new_problem_number)

    def open_folder(self):

        new_path = self.view.open_folder_dialog()

        if new_path:
            self.model.current_path = new_path
            self.view.update_folder_treeview(self.model.current_path)

    def add_choosen_file(self, file_name):

        file_basename, _ = os.path.splitext(os.path.basename(file_name))

        for extension in self.model.answer_extensions:
            file_path = "{}.{}".format(file_basename, extension)
            if os.path.exists(self.model.get_file_path(file_path)):
                _file_name = file_path
                break
        else:
            _file_name = self.view.open_file_dialog()
            if not _file_name:
                raise NoneAnswerForInputFile("Selected input file has not paired answer file.")
            if self.view.open_confirmation_dialog("¿Desea añadir la extensión a la lista?"):
                _, extension = os.path.splitext(os.path.basename(_file_name))
                if extension:
                    self.model.add_answer_extensions(extension[1:])
                    self.view.update_extension_treeviews(self.model.input_extensions, self.model.answer_extensions)

        self.model.add_choosen_file(file_name)
