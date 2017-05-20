import os
import traceback

from gi.repository import Gtk
from gi.repository import Gdk

from .controller import MainViewController
from .errors import ChoosenFileHasNotInputExtension


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
        self._openfoldermenuitem = self._builder.get_object('openfolderimagemenuitem')
        self._savemenuitem = self._builder.get_object('saveimagemenuitem')
        self._saveasmenuitem = self._builder.get_object('saveasimagemenuitem')
        self._exitmenuitem = self._builder.get_object('exitimagemenuitem')
        self._aboutmenuitem = self._builder.get_object('aboutimagemenuitem')

        # Number of problem input
        self._problemnumberentry = self._builder.get_object('problemnumberentry')
        self._updateproblemnumberbutton = self._builder.get_object('saveproblemnumberbutton')

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
        self._foldertreeviewnamecolumn = self._builder.get_object('foldernametreeviewcolumn')
        self._foldertreeviewsizecolumn = self._builder.get_object('foldersizetreeviewcolumn')

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
        self._inputfiletextbuffer = self._inputfiletextview.get_buffer()
        self._answerfiletextview = self._builder.get_object('answerfiletextview')
        self._answerfiletextbuffer = self._answerfiletextview.get_buffer()

    def _bind_events(self):

        # Window close event
        self._window.connect('delete-event', Gtk.main_quit)

        # Menu buttons events
        self._newmenuitem.connect('select', self._noop)
        self._openfoldermenuitem.connect('activate', self._open_folder_clicked)
        self._savemenuitem.connect('select', self._save_problem_clicked)
        self._saveasmenuitem.connect('select', self._noop)
        self._exitmenuitem.connect('select', self._noop)
        self._aboutmenuitem.connect('select', self._noop)

        # Folder treeview events
        # self._foldertreeviewselection.connect('changed', self._folder_selection_changed)

        # Drag and drop events
        self._foldertreeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [
            ('MY_TREE_MODEL_ROW', Gtk.TargetFlags.SAME_WIDGET, 0),
            ('text/plain', 0, 1), ], Gdk.DragAction.COPY)
        self._choosenfilestreeview.enable_model_drag_dest([
            ('MY_TREE_MODEL_ROW', Gtk.TargetFlags.SAME_WIDGET, 0),
            ('text/plain', 0, 1), ], Gdk.DragAction.COPY)
        self._foldertreeview.connect('drag-begin', self._noop)
        self._foldertreeview.connect('drag-data-get', self._folder_treeview_drag_get_data)
        self._choosenfilestreeview.connect('drag-data-received', self._choosenfiles_treeview_drag_data_received)

        # self._choosenfilestreeview.drag_dest_set_target_list(None)
        # self._foldertreeview.drag_source_set_target_list(None)
        #
        # self._foldertreeview.drag_dest_add_text_targets()
        # self._foldertreeview.drag_source_add_text_targets()


        # Number of problem input event
        self._problemnumberentry.connect('changed', self._problem_number_changed)
        self._problemnumberentry.connect('focus-out-event', self._problem_number_focus_out)
        self._updateproblemnumberbutton.connect('clicked', self._update_problem_number)

        # File management buttons events
        self._newproblembutton.connect('clicked', self._noop)
        self._saveproblembutton.connect('clicked', self._save_problem_clicked)
        self._openproblembutton.connect('clicked', self._open_folder_clicked)

        # Choosen files treeview events
        self._choosenfilestreeviewselection.connect('changed', self._noop)

        # Input/answer extension management events
        self._addinputextensionbutton.connect('clicked', self._add_input_extension_clicked)
        self._addanswerextensionbutton.connect('clicked', self._add_answer_extension_clicked)

    def load_default_settings(self):

        self._inputextensiontreestore.append('in')
        self._answerextensiontreestore.append('data')
        self._updateproblemnumberbutton.disable(False)

    def show_all(self):

        self._window.show_all()
        self._problemnumberentry.grab_focus()

    def open_error_dialog(self, error: Exception):
        print("Error occurred{0}:\n {1}".format(str(error), traceback.format_exc()))

        dialog = Gtk.MessageDialog(self._window, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK, error.__class__.__name__)
        dialog.format_secondary_text("{0}\n{1}".format(str(error), traceback.format_exc()))
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

    def open_save_file_dialog(self, root_path, suggested_filename):

        path = ""
        dialog = Gtk.FileChooserDialog("Please choose a file", self._window,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_current_folder(os.path.abspath(root_path))
        dialog.set_current_name(suggested_filename)

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

        try:
            self.controller.open_folder()
        except Exception as err:
            self.open_error_dialog(err)

    def open_folder_dialog(self, root_path=None):

        path = ""
        dialog = Gtk.FileChooserDialog("Please choose a folder", self._window,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        if root_path:
            dialog.set_current_folder(os.path.abspath(root_path))

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

        self._updateproblemnumberbutton.set_sensitive(True)

    def _problem_number_focus_out(self, entry, focus):

        try:
            self.controller.problem_number_focus_out(self._problemnumberentry.get_text())
        except Exception as err:
            self.open_error_dialog(err)

        return False

    def _update_problem_number(self, button):

        try:
            self.controller.problem_number_changed(self._problemnumberentry.get_text())
            button.set_sensitive(False)
        except Exception as err:
            self.open_error_dialog(err)

    def update_problem_number(self, new_problem_number):

        self._problemnumberentry.set_text(new_problem_number)

    def update_folder_treeview(self, pathtree):

        self._reset_treeview()

        def dirwalk(element, parent=None):
            # Get the absolute path of the item
            f, size, is_folder, fullname, children = element
            # Generate an icon from the default icon theme
            img = Gtk.IconTheme.get_default().load_icon(
                "folder" if is_folder else "document",
                12, 0)
            # Append the item to the TreeStore
            li = self._foldertreestore.append(parent, [f, img, size, is_folder, fullname])
            # If the item is a folder, descend into it
            if is_folder:
                for child in element.children:
                    dirwalk(child, li)

        # Iterate over the contents of the specified path
        for element in pathtree:
            dirwalk(element)

    def _reset_treeview(self):

        try:
            self._foldertreestore.clear()
        except Exception as err:
            self.open_error_dialog(err)

    def _folder_selection_changed(self, element):

        _, iterator = element.get_selected()
        is_folder, fullname = self._foldertreestore.get(iterator, 3, 4)
        if not is_folder:
            try:
                self.controller.add_choosen_file(fullname)
            except Exception as err:
                self.open_error_dialog(err)

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

    def update_problem_content(self, input_content, answer_content):

        self._inputfiletextbuffer.set_text(input_content)
        self._answerfiletextbuffer.set_text(answer_content)

        self._update_problem_files_sizes(input_content, answer_content)

    def _update_problem_files_sizes(self, input_content, answer_content):

        input_file_size, answer_file_size = map(len, [input_content, answer_content])
        self._inputsizelabel.set_text("{} B".format(input_file_size * 8))
        self._answersizelabel.set_text("{} B".format(answer_file_size * 8))

    def _add_input_extension_clicked(self, element):

        try:
            self.controller.add_input_extension(self._inputextensionentry.get_text())
        except Exception as err:
            self.open_error_dialog(err)

    def _add_answer_extension_clicked(self, element):

        try:
            self.controller.add_answer_extension(self._answerextensionentry.get_text())
        except Exception as err:
            self.open_error_dialog(err)

    def update_choosen_files_tree_view(self, choosen_files):

        self._choosenfilestreestore.clear()

        for files in choosen_files:
            inputfilename, answerfilename = map(os.path.basename, files)
            self._choosenfilestreestore.append([inputfilename, answerfilename])

    def _save_problem_clicked(self, element):

        try:
            self.controller.save_problem()
        except Exception as err:
            self.open_error_dialog(err)

    def _folder_treeview_drag_get_data(self, widget, drag_context, data, info, time):
        _, iterator = self._foldertreeviewselection.get_selected()
        is_folder, fullname = self._foldertreestore.get(iterator, 3, 4)

        if not is_folder:
            data.set_text(fullname, -1)

    def _choosenfiles_treeview_drag_data_received(self, widget, drag_context, x, y, data, info, time):

        try:
            file_path = data.get_text()
            self.controller.add_choosen_file(file_path)
        except ChoosenFileHasNotInputExtension as err:
            self.open_error_dialog(err)

    def _noop(self, *param, **kwargs):

        print('Event with params:\n{0}\n{1}'.format(param, kwargs))


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
