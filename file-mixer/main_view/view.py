import os
import sys
import traceback

from functools import partial
from math import log, floor

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
        self._right_click_menu = None

        self._load_elements()

        self.controller = MainViewController(self)

    def _load_elements(self):

        # Menu buttons
        self._load_menu_buttons()

        # Number of problem input
        self._load_problem_entry()

        # Output files information labels
        self._load_size_labels()

        # File management buttons
        self._load_problem_buttons()

        # File treeview
        self._load_folder_treeview()

        # Used files actions
        self._load_choosenfiles_actions()

        # Used files treeview
        self._load_choosenfiles_treeview()

        # Foldertv to Choosentv DragnDrop events
        self._load_foldertv2choosentv_dragndrop()

        # Input/answer extension management
        self._load_inputanswer_extensions_management()

        # Input/answer result content
        self._load_inputanswer_content_textviews()

        # Window close event
        self._window.connect('delete-event', Gtk.main_quit)

        # Default settings
        self._load_default_settings()

    def _load_menu_buttons(self):

        # Menu buttons
        self._newmenuitem = self._builder.get_object('newimagemenuitem')
        self._openfoldermenuitem = self._builder.get_object('openfolderimagemenuitem')
        self._savemenuitem = self._builder.get_object('saveimagemenuitem')
        self._saveasmenuitem = self._builder.get_object('saveasimagemenuitem')
        self._exitmenuitem = self._builder.get_object('exitimagemenuitem')
        self._aboutmenuitem = self._builder.get_object('aboutimagemenuitem')

        # Menu buttons events
        self._newmenuitem.connect('select', self._noop)
        self._openfoldermenuitem.connect('activate', self._open_folder_clicked)
        self._savemenuitem.connect('select', self._save_problem_clicked)
        self._saveasmenuitem.connect('select', self._noop)
        self._exitmenuitem.connect('select', self._noop)
        self._aboutmenuitem.connect('select', self._noop)

    def _load_problem_entry(self):

        # Number of problem input
        self._problemnumberentry = self._builder.get_object('problemnumberentry')
        self._updateproblemnumberbutton = self._builder.get_object('saveproblemnumberbutton')

        # Number of problem input event
        self._problemnumberentry.connect('changed', self._problem_number_changed)
        self._problemnumberentry.connect('focus-out-event', self._problem_number_focus_out)
        self._updateproblemnumberbutton.connect('clicked', self._update_problem_number)

    def _load_size_labels(self):

        # Output files information labels
        self._nfileslabel = self._builder.get_object('nfileslabel')
        self._inputsizelabel = self._builder.get_object('inputsizelabel')
        self._answersizelabel = self._builder.get_object('answersizelabel')

    def _load_problem_buttons(self):

        # File management buttons
        self._newproblembutton = self._builder.get_object('newproblembutton')
        self._saveproblembutton = self._builder.get_object('saveproblembutton')
        self._openproblembutton = self._builder.get_object('openproblembutton')
        self._openfolderbutton = self._builder.get_object('openfolderbutton')

        # File management buttons events
        self._newproblembutton.connect('clicked', self._new_file_clicked)
        self._saveproblembutton.connect('clicked', self._save_problem_clicked)
        self._openproblembutton.connect('clicked', self._open_file_clicked)
        self._openfolderbutton.connect('clicked', self._open_folder_clicked)

    def _load_folder_treeview(self):

        # File treeview
        self._foldertreestore = self._builder.get_object('foldertreestore')
        self._foldertreeview = self._builder.get_object('foldertreeview')
        self._foldertreeviewselection = self._builder.get_object('foldertreeview-selection')
        self._foldertreeviewnamecolumn = self._builder.get_object('foldernametreeviewcolumn')
        self._foldertreeviewnamecolumn.set_sort_column_id(0)
        self._foldertreeviewsizecolumn = self._builder.get_object('foldersizetreeviewcolumn')

    def _load_choosenfiles_actions(self):
        self._sortbynamebutton = self._builder.get_object('sortbynamebutton')
        self._sortbyrandombutton = self._builder.get_object('sortbyrandombutton')
        self._clearproblembutton = self._builder.get_object('clearproblembutton')
        self._sortbynamebutton.connect('clicked', self._sortbyname_clicked)
        self._sortbyrandombutton.connect('clicked', self._sortbyrandom_clicked)
        self._clearproblembutton.connect('clicked', self._clearproblem_clicked)

    def _load_choosenfiles_treeview(self):

        # Used file treeview
        self._choosenfilestreestore = self._builder.get_object('choosenfilesliststore')
        self._choosenfilestreeview = self._builder.get_object('choosenfilestreeview')
        self._inputfiletreeviewcolumn = self._builder.get_object('inputfiletreeviewcolumn')
        self._answerfiletreeviewcolumn = self._builder.get_object('answerfiletreeviewcolumn')
        self._choosenfilestreeviewselection = self._builder.get_object('choosenfilestreeview-selection')

        # Choosen files treeview events
        self._choosenfilestreeviewselection.connect('changed', self._noop)
        self._choosenfilestreeview.connect('button-release-event', self._choosenfiles_treeview_clicked)

    def _load_foldertv2choosentv_dragndrop(self):

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

    def _load_inputanswer_extensions_management(self):

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

        # Input/answer extension management events
        self._addinputextensionbutton.connect('clicked', self._add_input_extension_clicked)
        self._addanswerextensionbutton.connect('clicked', self._add_answer_extension_clicked)

    def _load_inputanswer_content_textviews(self):

        # Input/answer result content
        self._inputfiletextview = self._builder.get_object('inputfiletextview')
        self._inputfiletextbuffer = self._inputfiletextview.get_buffer()
        self._answerfiletextview = self._builder.get_object('answerfiletextview')
        self._answerfiletextbuffer = self._answerfiletextview.get_buffer()

    def _load_default_settings(self):

        # Default input/answer extension
        self._inputextensiontreestore.append(['in'])
        self._answerextensiontreestore.append(['data'])

        # Disable problem information update buttons
        self._updateproblemnumberbutton.set_sensitive(False)
        self._saveproblembutton.set_sensitive(False)

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

    def _open_file_clicked(self, element):

        try:
            self.controller.open_problem_file()
            self._saveproblembutton.set_sensitive(False)
        except Exception as err:
            self.open_error_dialog(err)

    def _new_file_clicked(self, element):

        try:
            self.controller.new_problem_file()
            self._saveproblembutton.set_sensitive(False)
        except Exception as err:
            self.open_error_dialog(err)

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

    def open_folder_dialog(self, root_path=None, save=False):

        path = ""
        dialog = Gtk.FileChooserDialog("Please choose a folder", self._window,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN if not save else Gtk.STOCK_SAVE,
                                        Gtk.ResponseType.OK))
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

    def open_entry_dialog(self, _label=None, _title=None):
        label = _label or "Please input problem number"
        title = _title

        entry = ""
        dialog = EntryDialog(self._window, label, title)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            entry = dialog.get_text()
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

        return entry

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
            self._enable_save_button()
        except Exception as err:
            self.open_error_dialog(err)

    def update_problem_number(self, new_problem_number: str):

        self._problemnumberentry.set_text(str(new_problem_number))

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
            li = self._foldertreestore.append(parent,
                                              [f, img, "{} {}B".format(*self._raw_size_to_unit(size)), is_folder,
                                               fullname])
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

        self._update_problem_files_number()
        self._update_problem_files_sizes(input_content, answer_content)

    def _update_problem_files_number(self):
        self._nfileslabel.set_text(str(len(self._choosenfilestreestore)))

    def _update_problem_files_sizes(self, input_content, answer_content):

        input_file_size, answer_file_size = map(sys.getsizeof, [input_content, answer_content])
        self._inputsizelabel.set_text("{} {}B".format(*self._raw_size_to_unit(input_file_size)))
        self._answersizelabel.set_text("{} {}B".format(*self._raw_size_to_unit(answer_file_size)))

    @staticmethod
    def _raw_size_to_unit(size):

        sizes = ['', 'K', 'M', 'G']
        try:
            size_log = log(size, 1024)
        except ValueError as err:
            print("Value error calculating log_1024 of {0}".format(size))
            size_log = 0
        measurement = floor(size_log)
        return size // (1024 ** measurement), sizes[measurement]

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

    def _delete_choosen_file_clicked(self, inputfilename, element):
        print("element clicked - delete {} file".format(inputfilename))

    def _save_problem_clicked(self, element):

        try:
            self.controller.save_problem()
            self._disable_save_button()
        except Exception as err:
            self.open_error_dialog(err)

    def _folder_treeview_drag_get_data(self, widget, drag_context, data, info, time):
        _, iterator = self._foldertreeviewselection.get_selected()
        is_folder, fullname = self._foldertreestore.get(iterator, 3, 4)

        if not is_folder:
            data.set_text(fullname, -1)

    def _sortbyname_clicked(self, button):
        try:
            self.controller.sort_choosen_files()
        except Exception as err:
            self.open_error_dialog(err)

    def _sortbyrandom_clicked(self, button):
        try:
            self.controller.shuffle_choosen_files()
        except Exception as err:
            self.open_error_dialog(err)

    def _clearproblem_clicked(self, button):
        try:
            self.controller.clear_choosen_files()
        except Exception as err:
            self.open_error_dialog(err)

    def _choosenfiles_treeview_drag_data_received(self, widget, drag_context, x, y, data, info, time):

        try:
            file_path = data.get_text()
            self.controller.add_choosen_file(file_path)
            self._enable_save_button()
        except Exception as err:
            self.open_error_dialog(err)

    def _choosenfiles_treeview_clicked(self, treeview, event):

        if event.button == 3:
            selected_path = self._choosenfilestreeview.get_path_at_pos(int(event.x), int(event.y))

            if selected_path:
                path, _, _, _ = selected_path

                if self._choosenfilestreeviewselection.path_is_selected(path):
                    _, iterator = self._choosenfilestreeviewselection.get_selected()
                    inputfilename = self._choosenfilestreestore.get(iterator, 0)[0]
                    inputfileindex = path.get_indices()[0]
                    print('Input file index: ', inputfileindex)
                    self._right_click_menu = Gtk.Menu()
                    delete_button = Gtk.MenuItem("Eliminar")
                    delete_button.connect('activate',
                                          partial(self._right_menu_delete_btn_clicked, inputfilename, inputfileindex))
                    self._right_click_menu.append(delete_button)
                    self._right_click_menu.show_all()
                    self._right_click_menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

    def _right_menu_delete_btn_clicked(self, inputfilename, inputfileindex, *args):

        try:
            self._right_click_menu.destroy()
            self.controller.remove_choosen_file(file_index=inputfileindex)
            self._enable_save_button()
        except Exception as err:
            self.open_error_dialog(err)

    def _noop(self, *param, **kwargs):

        print('Event with params:\n{0}\n{1}'.format(param, kwargs))

    def _enable_save_button(self):

        self._saveproblembutton.set_sensitive(True)

    def _disable_save_button(self):

        self._saveproblembutton.set_sensitive(False)


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


class EntryDialog(Gtk.Dialog):
    def __init__(self, parent, label_text, title=None):
        if not title:
            title = "Entry dialog"

        Gtk.Dialog.__init__(self, title, parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label(label_text)
        self._entry = Gtk.Entry()

        box = self.get_content_area()
        box.add(label)
        box.add(self._entry)

        self.show_all()

    def get_text(self):
        return self._entry.get_text()
