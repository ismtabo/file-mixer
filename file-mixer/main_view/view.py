from gi.repository import Gtk

from .controller import MainViewController

class MainView(object):
    """docstring for MainView."""
    def __init__(self, builder, window_label):
        super(MainView, self).__init__()
        self._builder = builder
        self._window = self._builder.get_object(window_label)
        self.controller = MainViewController(self)

        self._load_elements()
        self._bind_events()

    def _load_elements(self):
        self._problemnumberentry = self._builder.get_object('problemnumberentry')
        self._inputsizelabel = self._builder.get_object('inputsizelabel')
        self._answersizelabel = self._builder.get_object('answersizelabel')
        pass

    def _bind_events(self):
        self._window.connect("delete-event", Gtk.main_quit)
        self._problemnumberentry.connect("changed", self._problem_number_changed)

    def show_all(self):
        self._window.show_all()

    def _problem_number_changed(self, entry):
        self.controller.problem_number_changed(entry.get_text())
