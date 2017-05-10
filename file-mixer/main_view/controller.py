import os

from .model import MainViewModel


class MainViewController(object):
    """docstring for MainViewController."""

    def __init__(self, view):
        super(MainViewController, self).__init__()
        self.view = view
        self.model = MainViewModel()

    def problem_number_changed(self, new_problem_number):
        print(new_problem_number)

    @property
    def current_dir(self):
        return self._current_dir

    @current_dir.setter
    def current_dir(self, new_dir):
        self._current_dir = new_dir

    def open_folder(self):
        new_path = self.view.open_folder_dialog()

        if new_path:
            self.current_dir = new_path
            self.view.update_folder_treeview(self.current_dir)

    def add_choosen_file(self, file_name):
        file_basename, _ = os.path.splitext(os.path.basename(file_name))


        for extension in self.model.answer_extensions:
            pass

        self.model.add_choosen_file(file_name)
