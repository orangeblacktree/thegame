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
            exec(code, userspace.space, userspace.space)
        except Exception as e:
            gtk.threads_enter()
            shared.gui.set_status("Error: " + e.__str__())
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

def do_about(*args):
    pass

def do_quit(*args):
    shared.stop_game = True

entries = [
  ("FileMenu", None, "_File"),
  ("EditMenu", None, "_Edit"),
  ("RunMenu", None, "_Run"),
  ("HelpMenu", None, "_Help"),

#  ("Open", gtk.STOCK_OPEN,
#    "_Open","<control>O",
#    "Open a file",
#    do_open), 
#  ("Save", gtk.STOCK_SAVE,
#    "_Save","<control>S",
#    "Save current file",
#    do_save),
#  ("SaveAs", gtk.STOCK_SAVE,
#    "Save _As...", None,
#    "Save to a file",
#    do_save_as),
  ("NewTab", gtk.STOCK_ADD,
    "_New Tab", "<Control>N",
    "Make a new tab",
    lambda *args: shared.gui.add_page()), 
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
  ("Quit", gtk.STOCK_QUIT,
    "_Quit", "Escape",
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

  ("About", None,
    "_About", "<control>A",
    "About",
    do_about),
]

ui_info ="""
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='NewTab'/>
      <menuitem action='CloseTab'/>
      <separator/>
      <menuitem action='NextTab'/>
      <menuitem action='PrevTab'/>
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

    <menu action='HelpMenu'>
      <menuitem action='About'/>
    </menu>
  </menubar>
</ui>
"""

codelang = gtksourceview.language_manager_get_default().guess_language("test.py")
codefont = pango.FontDescription('monospace')

class Page:
    def __init__(self, gui, label):
        self.label = label
        self.gui = gui

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
        gui.nb.set_tab_label_text(self.sw, label)
        gui.window.show_all()

    def close(self):
        ind = self.gui.nb.page_num(self.sw)
        self.gui.nb.remove_page(ind)
        self.gui.pages.remove(self)

class Gui:
    def __init__(self):
        self.runner = None
        self.window = shared.gtkwin
        self.new_page_num = 1
        self.pages = []

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

        # action!
        self.add_page()
        self.window.show_all()
        self.set_status("Ready!")
        self.focus_page()

    def add_page(self):
        self.pages.append(Page(self, "Tab %d" % (self.new_page_num)))
        self.set_page(-1) #last page
        self.new_page_num += 1

    def set_page(self, ind):
        self.nb.set_current_page(ind)
    def get_page(self):
        return self.nb.get_current_page()

    def next_page(self):
        self.nb.next_page()
    def prev_page(self):
        self.nb.prev_page()

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

            if (ind >= 0):
                buf = self.pages[ind].buf
                start, end = buf.get_bounds()
                self.runner = Runner(self.pages[ind].label,
                        buf.get_text(start, end, False))
                self.runner.start()
                self.set_status("Running...")
        else:
            fmt = "Currently running code from '%s'... Press Ctrl+E to Cancel."
            self.set_status(fmt % (self.runner.filename))

    def undo(self, *args):
        ind = self.get_page()

        if (ind >= 0):
            buf = self.pages[ind].buf
            if buf.can_undo():
                buf.undo()

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

