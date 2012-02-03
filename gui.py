# ------------------------------------------------------------------
# gui.py
# 
# The code editor gui
# ------------------------------------------------------------------

import pygtk
import threading
import gtk
import gobject
import pango
import inspect
import ctypes
import sys
import trace
import os
import gtksourceview2 as gtksourceview

import shared
import userspace

class KThread(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
                return self.localtrace

    def kill(self):
        self.killed = True

class Runner(KThread):
    def __init__(self, filename, text):
        super(Runner, self).__init__()
        self.text = text
        self.filename = filename

    def run(self):
        try:
            code = compile(self.text, self.filename, "exec")
            userspace.run(code)
        except Exception as e:
            userspace.output("Error: " + e.__str__())
            gtk.threads_enter()
            shared.gui.set_status("Error! Check output console.")
            gtk.threads_leave()
        except SystemExit:
            gtk.threads_enter()
            shared.gui.set_status("Cancelled.")
            gtk.threads_leave()
        else:
            gtk.threads_enter()
            shared.gui.set_status("Finished running!")
            gtk.threads_leave()
        shared.gui.runner = None

def do_quit(*args):
    shared.stop_game = True

entries = [
  ("FileMenu", None, "_File"),
  ("EditMenu", None, "_Edit"),
  ("RunMenu", None, "_Run"),

  ("Open", gtk.STOCK_OPEN,
    "_Open","<control>O",
    "Open a file",
    lambda *args: shared.gui.do_open()), 
  ("Save", gtk.STOCK_SAVE,
    "_Save","<control>S",
    "Save current file",
    lambda *args: shared.gui.do_save()),
  ("SaveAs", gtk.STOCK_SAVE,
    "Save _As...", None,
    "Save to a file",
    lambda *args: shared.gui.do_save_as()),
  ("NewTab", gtk.STOCK_ADD,
    "_New Tab", "<Control>N",
    "Make a new tab",
    lambda *args: shared.gui.new_page()), 
  ("CloseTab", gtk.STOCK_CLOSE,
    "_Close Tab", "<Control>W",
    "Close currently visible tab",
    lambda *args: shared.gui.close_page()), 
  ("NextTab", gtk.STOCK_GO_FORWARD,
    "_Next Tab", "<Control>Right",
    "Switch to next tab",
    lambda *args: shared.gui.next_page()), 
  ("PrevTab", gtk.STOCK_GO_BACK,
    "_Previous Tab", "<Control>Left",
    "Switch to previous tab",
    lambda *args: shared.gui.prev_page()), 
  ("DetachHelp", None,
    "_Detach Help Window", "<Control>D",
    "Detach the help tab",
    lambda *args: shared.gui.detach_help_page()), 
  ("AttachHelp", None,
    "_Attach Help Window", "<Control>G",
    "Attach the help tab",
    lambda *args: shared.gui.attach_help_page()), 
  ("Quit", gtk.STOCK_QUIT,
    "_Quit", "<Control>Q",
    "Exit the program",
    do_quit), 

  ("Undo", gtk.STOCK_UNDO,
    "_Undo", "<control>Z",
    "Undo",
    lambda *args: shared.gui.undo()),

  ("Run", gtk.STOCK_MEDIA_PLAY,
    "_Run", "<control>R",
    "Run code in current tab",
    lambda *args: shared.gui.run()), 
  ("Cancel", gtk.STOCK_MEDIA_STOP,
    "_Cancel", "<control>E",
    "Cancel",
    lambda *args: shared.gui.cancel()), 
]

ui_info ="""
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='NewTab'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <menuitem action='Open'/>
      <menuitem action='CloseTab'/>
      <separator/>
      <menuitem action='NextTab'/>
      <menuitem action='PrevTab'/>
      <separator/>
      <menuitem action='DetachHelp'/>
      <menuitem action='AttachHelp'/>
      <separator/>
      <menuitem action='Quit'/>
    </menu>

    <menu action='EditMenu'>
      <menuitem action='Undo'/>
    </menu>

    <menu action='RunMenu'>
      <menuitem action='Run'/>
      <menuitem action='Cancel'/>
    </menu>
    
  </menubar>
</ui>
"""

codelang = gtksourceview.language_manager_get_default().guess_language("test.py")
codefont = pango.FontDescription('monospace')

class Page:
    def __init__(self, gui, filename, path = None):
        self.gui = gui
        self.path = path
        self.is_help = False

        # text edit box inside a scrolled window
        self.buf = gtksourceview.Buffer()
        self.text = gtksourceview.View(self.buf)
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.set_shadow_type(gtk.SHADOW_IN)
        self.sw.add(self.text)

        self.buf.set_language(codelang)
        self.text.set_show_line_numbers(True)
        self.text.set_auto_indent(True)
        self.text.set_insert_spaces_instead_of_tabs(True)
        self.text.set_tab_width(4)
        self.text.set_smart_home_end(True)
        if codefont:
            self.text.modify_font(codefont)

        # add self to notebook
        gui.nb.append_page(self.sw, None)
        self.set_filename(filename)
        gui.window.show_all()

    def close(self):
        ind = self.gui.nb.page_num(self.sw)
        self.gui.nb.remove_page(ind)
        self.gui.pages.remove(self)

    def set_filename(self, filename):
        self.filename = filename
        self.gui.nb.set_tab_label_text(self.sw, filename)

divider_text = '\n# ----------------------------------------------------------------------------\n'
class HelpPage:
    def __init__(self, gui):
        self.gui = gui
        self.is_help = True
        self.window = None

        # text box inside a scrolled window
        self.buf = gtksourceview.Buffer()
        self.text = gtksourceview.View(self.buf)
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.set_shadow_type(gtk.SHADOW_IN)
        self.sw.add(self.text)

        self.buf.set_language(codelang)
        #self.text.set_show_line_numbers(True)
        self.text.set_smart_home_end(True)
        if codefont:
            self.text.modify_font(codefont)

        # can't edit help text
        self.text.set_editable(False)

        # initially detached
        self.detach()

    def attach(self):
        if hasattr(self, 'attached') and self.attached:
            return

        # remove detached window if exists
        if self.window is not None:
            self.remove_window()

        # add self to notebook at 0
        self.gui.nb.insert_page(self.sw, None, 0)
        self.gui.nb.set_tab_label_text(self.sw, "Help")
        self.gui.window.show_all()

        # add self to pages list at 0
        self.gui.pages.insert(0, self)

        self.attached = True

    def detach(self):
        # remove from notebook
        if hasattr(self, 'attached'):
            if self.attached:
                self.gui.nb.remove_page(0)
                self.gui.pages.remove(self)
            else:
                return

        # create separate window
        self.make_window()

        self.attached = False

    def make_window(self):
        # make window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # move slightly below-right of main window
        x, y = shared.gtkwin.get_position()
        w, h = shared.gtkwin.get_size()
        h -= 50
        self.window.resize(w, h)
        self.window.move(x, y - h - 70)
        self.window.set_title("thegame - help")

        # on close, attach
        self.window.connect("delete-event", lambda *args: self.attach())

        # attach self
        self.window.add(self.sw)
        self.window.show_all()
    def remove_window(self):
        self.window.remove(self.sw)
        self.window.destroy()

    def set_text(self, text):
        self.buf.set_text(text)
    def append_text(self, text):
        end = self.buf.get_end_iter()
        self.buf.insert(end, divider_text + text)

        new_end = self.buf.get_end_iter()
        self.buf.place_cursor(new_end)
        self.text.scroll_mark_onscreen(self.buf.get_insert())

    def clear_text(self):
        self.buf.delete(*(self.buf.get_bounds()))

    def close(self):
        pass #can't close help page!

class Gui:
    def __init__(self):
        self.runner = None
        self.window = shared.gtkwin
        self.new_page_num = 1
        self.pages = []

        # on close, quit
        self.window.connect("delete-event", do_quit)

        # table
        self.table = gtk.Table(3, 1, False)
        self.window.add(self.table)

        # menu bar
        actions = gtk.ActionGroup("Actions")
        actions.add_actions(entries)
      
        ui = gtk.UIManager()
        ui.insert_action_group(actions, 0)
        self.window.add_accel_group(ui.get_accel_group())
        self.window.set_border_width(0)
        ui.add_ui_from_string(ui_info)

        bar = ui.get_widget("/MenuBar")
        bar.show()
        self.table.attach(bar, 
                # X                    # Y
                0, 1,                  0, 1,
                gtk.EXPAND | gtk.FILL, 0,
                0,                     0)

        # notebook
        self.nb = gtk.Notebook()
        self.table.attach(self.nb,
                # X                    # Y
                0, 1,                  1, 2,
                gtk.EXPAND | gtk.FILL, gtk.EXPAND | gtk.FILL,
                0,                     0)
        self.nb.connect("focus-tab", self.focus_page)

        # run button
        #self.run_button = gtk.Button("Run!")
        #self.run_button.connect("clicked", self.run, None)
        #self.table.attach(self.run_button,
                # X                    # Y
                #0, 1,                  2, 3,
                #gtk.EXPAND | gtk.FILL, 0,
                #0,                     0)

        # status bar
        self.status = gtk.Statusbar()
        self.table.attach(self.status,
                # X                    # Y
                0, 1,                  2, 3,
                gtk.EXPAND | gtk.FILL, 0,
                0,                     0)

        # make help tab and a new code tab
        self.help_page = HelpPage(self)
        self.set_page(0) #focus help page

        # action!
        self.window.show_all()
        self.set_status("Ready!")
        self.focus_page()

    def new_page(self):
        self.add_page("new file %d" % (self.new_page_num))
        self.new_page_num += 1

    def add_page(self, name):
        page = Page(self, name)
        self.pages.append(page)
        self.set_page(-1) #last page
        self.focus_page()
        return page

    def set_page(self, ind):
        self.nb.set_current_page(ind)
    def get_page(self):
        return self.nb.get_current_page()

    def next_page(self):
        self.nb.next_page()
    def prev_page(self):
        self.nb.prev_page()
        
    def undo(self, *args):
        ind = self.get_page()

        if (ind >= 0):
            buf = self.pages[ind].buf
            if buf.can_undo():
                buf.undo()

    def focus_page(self):
        ind = self.get_page()
        if ind >= 0:
            self.pages[ind].text.grab_focus()

    def close_page(self):
        ind = self.get_page()
        if ind >= 0:
            self.pages[ind].close()

    def step(self, elapsed):
        pass

    def run(self, *args):
        if not self.runner:
            ind = self.get_page()

            if ind >= 0 and not self.pages[ind].is_help:
                filename = self.pages[ind].filename
                buf = self.pages[ind].buf
                start, end = buf.get_bounds()
                self.runner = Runner(filename, buf.get_text(start, end, False))
                self.runner.start()
                fmt = "Running '%s'..."
                self.set_status(fmt % (filename))
        else:
            fmt = "Already running '%s'... Press Ctrl+E to Cancel."
            self.set_status(fmt % (self.runner.filename))

    def set_status(self, msg):
        self.status.pop(0)
        self.status.push(0, msg)

    def cancel(self, *args):
        if self.runner and self.runner.isAlive():
            self.runner.kill()
            self.runner = None

    def quit(self):
        if self.runner and self.runner.isAlive():
            self.runner.kill()
            self.runner.join()

    def do_open(self):
        dialog = gtk.FileChooserDialog("Select file",
                                       self.window,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            path = dialog.get_filename()
            self.load_file(path)
        dialog.destroy()
    def load_file(self, path):
        error_dialog = None
        try:
            contents = file(path).read()
        except IOError, ex:
            error_dialog = gtk.MessageDialog(self.window,
                                             gtk.DIALOG_DESTROY_WITH_PARENT,
                                             gtk.MESSAGE_ERROR,
                                             gtk.BUTTONS_CLOSE,
                                             "Error loading file %s:\n%s" %
                                             (path,
                                              str(ex)))
        else:
            try:
                contents = contents.decode("utf-8")
            except UnicodeDecodeError:
                error_dialog = gtk.MessageDialog(self.window,
                                                 gtk.DIALOG_DESTROY_WITH_PARENT,
                                                 gtk.MESSAGE_ERROR,
                                                 gtk.BUTTONS_CLOSE,
                                                 "Error loading file %s:\n%s" %
                                                 (path,
                                                  "Not valid text"))
            else:
                page = self.add_page(os.path.basename(path))
                page.path = path
                page.buf.set_text(contents)
        if error_dialog is not None:
            error_dialog.connect("response", lambda w,resp: w.destroy())
            error_dialog.show()

    def do_save(self):
        ind = self.get_page()
        if ind < 0 or self.pages[ind].is_help:
            return
        page = self.pages[ind]
        if not page.path:
            self.do_save_as()
        else:
            self.save_file(page, page.path)
    def do_save_as(self):
        ind = self.get_page()
        if ind < 0 or self.pages[ind].is_help:
            return
        page = self.pages[ind]

        dialog = gtk.FileChooserDialog("Select file",
                                       self.window,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            path = dialog.get_filename()
            self.save_file(page, path)
        dialog.destroy()
    def save_file(self, page, path):
        start, end = page.buf.get_bounds()
        text = page.buf.get_text(start, end, False)

        error_dialog = None
        try:
            file(path, "w").write(text)
        except IOError, ex:
            error_dialog = gtk.MessageDialog(self.window,
                                             gtk.DIALOG_DESTROY_WITH_PARENT,
                                             gtk.MESSAGE_ERROR,
                                             gtk.BUTTONS_CLOSE,
                                             "Error saving to file %s:\n%s" %
                                             (open_filename,
                                              str(ex)))
            error_dialog.connect("response", lambda w,resp: w.destroy())
            error_dialog.show()
        else:
            page.set_filename(os.path.basename(path))
            page.path = path

    def detach_help_page(self):
        self.help_page.detach()
    def attach_help_page(self):
        self.help_page.attach()
