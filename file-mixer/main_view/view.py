import os
import stat
from gi.repository import Gtk

from .controller import MainViewController


class MainView(object):
    """docstring for MainView."""

    def __init__(self, builder, window_label):

        super(MainView, self).__init__()
        self._builder = builder
        self._window = self._builder.get_object(window_label)

        self._load_elements()
        self._bind_events()

        self.controller = MainViewController(self)


    def _load_elements(self):

        # Menu buttons
        self._newmenuitem = self._builder.get_object('newimagemenuitem')
        self._openmenuitem = self._builder.get_object('openimagemenuitem')
        self._savemenuitem = self._builder.get_object('saveimagemenuitem')
        self._saveasmenuitem = self._builder.get_object('saveasimagemenuitem')
        self._exitmenuitem = self._builder.get_object('exitimagemenuitem')
        self._aboutmenuitem = self._builder.get_object('aboutimagemenuitem')

        # Number of problem input
        self._problemnumberentry = self._builder.get_object('problemnumberentry')

        # Output files information labels
        self._inputsizelabel = self._builder.get_object('inputsizelabel')
        self._answersizelabel = self._builder.get_object('answersizelabel')

        # File management buttons
        self._newproblembutton = self._builder.get_object('newproblembutton')
        self._saveproblembutton = self._builder.get_object('saveproblembutton')
        self._openproblembutton = self._builder.get_object('openproblembutton')

        # File treeview
        self._foldertreestore = self._builder.get_object('foldertreestore')
        self._foldertreeview = self._builder.get_object('foldertreeview')
        self._foldertreeviewselection = self._builder.get_object('foldertreeview-selection')

        # Used file treeview
        self._choosenfilestreestore = self._builder.get_object('choosenfilesliststore')
        self._choosenfilestreeview = self._builder.get_object('choosenfilestreeview')
        self._inputfiletreeviewcolumn = self._builder.get_object('inputfiletreeviewcolumn')
        self._answerfiletreeviewcolumn = self._builder.get_object('answerfiletreeviewcolumn')
        self._choosenfilestreeviewselection = self._builder.get_object('choosenfilestreeview-selection')

        # Input/answer extensions treeviews
        self._inputextensiontreestore = self._builder.get_object('inputextensionliststore')
        self._inputextensiontreeview = self._builder.get_object('inputextensiontreeview')
        self._answerextensiontreestore = self._builder.get_object('answerextensionliststore')
        self._answerextensiontreeview = self._builder.get_object('answerextensiontreeview')

        # Input/answer extension management
        self._inputextensionentry = self._builder.get_object('inputextensionentry')
        self._addinputextensionbutton = self._builder.get_object('addinputextensionbutton')
        self._inputextensiontreeviewcolumn = self._builder.get_object('inputextensiontreeviewcolumn')
        self._answerextensionentry = self._builder.get_object('answerextensionentry')
        self._addanswerextensionbutton = self._builder.get_object('addanswerextensionbutton')
        self._answerextensiontreeviewcolumn = self._builder.get_object('_answerextensiontreeviewcolumn')

        # Input/answer result content
        self._inputfiletextview = self._builder.get_object('inputfiletextview')
        self._answerfiletextview = self._builder.get_object('answerfiletextview')

    def _bind_events(self):

        # Window close event
        self._window.connect("delete-event", Gtk.main_quit)

        # Menu buttons events
        self._newmenuitem.connect('select', self.noop)
        self._openmenuitem.connect('activate', self._open_folder_clicked)
        self._savemenuitem.connect('select', self.noop)
        self._saveasmenuitem.connect('select', self.noop)
        self._exitmenuitem.connect('select', self.noop)
        self._aboutmenuitem.connect('select', self.noop)

        # Folder treeview events
        self._foldertreeviewselection.connect('changed', self._folder_selection_changed)

        # Number of problem input event
        self._problemnumberentry.connect('changed', self._problem_number_changed)

        # File management buttons events
        self._newproblembutton.connect('clicked', self.noop)
        self._saveproblembutton.connect('clicked', self.noop)
        self._openproblembutton.connect('clicked', self._open_folder_clicked)

        # Choosen files treeview events
        self._choosenfilestreeviewselection.connect('changed', self.noop)

        # Input/answer extension management events
        self._addinputextensionbutton = self._builder.get_object('addinputextensionbutton')
        self._addanswerextensionbutton = self._builder.get_object('addanswerextensionbutton')

    def load_default_settings(self):

        self._inputextensiontreestore.append('in')
        self._answerextensiontreestore.append('data')

    def show_all(self):

        self._window.show_all()

    def open_error_dialog(self, error):

        dialog = Gtk.MessageDialog(self._window, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, error)
        dialog.format_secondary_text(
            "")
        dialog.run()
        dialog.destroy()

    def open_confirmation_dialog(self, confirmation_question, confirmation_title=None):

        dialog = ConfirmationDialog(self._window, confirmation_question, confirmation_title)
        response = dialog.run()
        dialog.destroy()

        return response == Gtk.ResponseType.OK

    def open_file_dialog(self):

        path = ""
        dialog = Gtk.FileChooserDialog("Please choose a file", self._window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            path = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

        return path

    def _open_folder_clicked(self, element):

        self.controller.open_folder()


    def open_folder_dialog(self):

        path = ""
        dialog = Gtk.FileChooserDialog("Please choose a folder", self._window,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("Folder selected: " + dialog.get_filename())
            path = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

        return path

    def _problem_number_changed(self, entry):

        self.controller.problem_number_changed(entry.get_text())

    def update_folder_treeview(self, dirname):

        self._reset_treeview()

        def dirwalk(path, parent=None):
            # Iterate over the contents of the specified path
            for f in os.listdir(path):
                # Get the absolute path of the item
                fullname = os.path.join(path, f)
                # Extract metadata from the item
                fdata = os.stat(fullname)
                # Determine if the item is a folder
                is_folder = stat.S_ISDIR(fdata.st_mode)
                # Generate an icon from the default icon theme
                img = Gtk.IconTheme.get_default().load_icon(
                    "folder" if is_folder else "document",
                    12, 0)
                # Append the item to the TreeStore
                li = self._foldertreestore.append(parent, [f, img, fdata.st_size, is_folder])
                # If the item is a folder, descend into it
                if is_folder:
                    dirwalk(fullname, li)

        dirwalk(dirname)

    def _reset_treeview(self):

        self._foldertreestore.clear()

    def _folder_selection_changed(self, element):
        _, iter = element.get_selected()
        file_name, is_folder = self._foldertreestore.get(iter, 0, 3)
        if not is_folder:
            self.controller.add_choosen_file(file_name)

    def update_extension_treeviews(self, input_extensions, answer_extensions):

        self._update_input_extension_treeviews(input_extensions)
        self._update_answer_extension_treeviews(answer_extensions)

    def _update_input_extension_treeviews(self, new_input_extensions):

        self._inputextensiontreestore.clear()
        for extension in new_input_extensions:
            self._inputextensiontreestore.append([extension])

    def _update_answer_extension_treeviews(self, new_answer_extensions):

        self._answerextensiontreestore.clear()
        for extension in new_answer_extensions:
            self._answerextensiontreestore.append([extension])

    def noop(self, param):

        print('New event not bind from ', param)


class ConfirmationDialog(Gtk.Dialog):

    def __init__(self, parent, label_text, title=None):

        if not title:
            title = "Confirmation dialog"

        Gtk.Dialog.__init__(self, title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label(label_text)

        box = self.get_content_area()
        box.add(label)

        self.show_all()
