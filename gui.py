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
    def __init__(self, text):
        super(Runner, self).__init__()
        self.text = text

    def run(self):
        try:
            code = compile(self.text, "code", "exec")
            exec(code, shared.userspace, shared.userspace)
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
  ("FileMenu", None, "_File"),     # name, stock id, label
  ("EditMenu", None, "_Edit"),       # name, stock id, label
  ("RunMenu", None, "_Run"),       # name, stock id, label
  ("HelpMenu", None, "_Help"),     # name, stock id, label

#  ("New", gtk.STOCK_NEW,            # name, stock id
#    "_New", "<control>N",           # label, accelerator
#    "Create a new file",            # tooltip
#    do_new),      
#  ("Open", gtk.STOCK_OPEN,          # name, stock id
#    "_Open","<control>O",           # label, accelerator
#    "Open a file",                  # tooltip
#    do_open), 
#  ("Save", gtk.STOCK_SAVE,          # name, stock id
#    "_Save","<control>S",           # label, accelerator
#    "Save current file",            # tooltip
#    do_save),
#  ("SaveAs", gtk.STOCK_SAVE,        # name, stock id
#    "Save _As...", None,            # label, accelerator
#    "Save to a file",               # tooltip
#    do_save_as),
  ("Quit", gtk.STOCK_QUIT,          # name, stock id
    "_Quit", "Escape",              # label, accelerator
    "Quit",                         # tooltip
    do_quit), 

  ("Run", gtk.STOCK_MEDIA_PLAY,        # name, stock id
    "_Run", "<control>R",           # label, accelerator
    "Run",                          # tooltip
    lambda *args: shared.gui.run()), 

  ("Cancel", gtk.STOCK_MEDIA_STOP,        # name, stock id
    "_Cancel", "<control>E",           # label, accelerator
    "Cancel",                          # tooltip
    lambda *args: shared.gui.cancel()), 

  ("Undo", gtk.STOCK_UNDO,        # name, stock id
    "_Undo", "<control>Z",           # label, accelerator
    "Undo",                          # tooltip
    lambda *args: shared.gui.undo()), 

  ("About", None,                   # name, stock id
    "_About", "<control>A",         # label, accelerator
    "About",                        # tooltip
    do_about),
]

ui_info ="""
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
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

class Gui:
    def init(self):
        self.runner = None
        self.window = shared.gtkwin

        # table
        self.table = gtk.Table(4, 1, False)
        self.window.add(self.table)

        # menus
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

        # text edit box
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.set_shadow_type(gtk.SHADOW_IN)
        self.table.attach(self.sw,
                # X                    # Y
                0, 1,                  1, 2,
                gtk.EXPAND | gtk.FILL, gtk.EXPAND | gtk.FILL,
                0,                     0)

        self.buf = gtksourceview.Buffer()
        self.text = gtksourceview.View(self.buf)
        self.sw.add(self.text)

        # editor stuff
        langmgr = gtksourceview.language_manager_get_default()
        lang = langmgr.guess_language("test.py")
        self.buf.set_language(lang)

        self.text.set_show_line_numbers(True)
        self.text.set_auto_indent(True)
        self.text.set_insert_spaces_instead_of_tabs(True)
        self.text.set_tab_width(4)
        self.text.set_smart_home_end(True)

        font_desc = pango.FontDescription('monospace')
        if font_desc:
            self.text.modify_font(font_desc)

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
                0, 1,                  3, 4,
                gtk.EXPAND | gtk.FILL, 0,
                0,                     0)

        # action!
        self.window.show_all()
        self.text.grab_focus()
        self.set_status("Ready!")

    def step(self, elapsed):
        pass

    def run(self, *args):
        if not self.runner:
            start, end = self.buf.get_bounds()
            self.runner = Runner(self.buf.get_text(start, end, False))
            self.runner.start()
            self.set_status("Running...")
        else:
            self.set_status("Currently running... Press Ctrl+E to Cancel.")

    def undo(self, *args):
        if self.buf.can_undo():
            self.buf.undo()

    def set_status(self, msg):
        self.status.pop(0)
        self.status.push(0, msg)

    def cancel(self, *args):
        if self.runner and self.runner.isAlive():
            self.runner.kill()
            self.runner = None

    def quit(self):
        self.cancel()

