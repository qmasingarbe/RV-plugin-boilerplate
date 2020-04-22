# rv python libs (located here on my systeme => /usr/local/rv-7.3.1/plugins/Python/rv)
from rv import rvtypes as rvt
from rv import commands as rvc
from rv import extra_commands as rve
from rv import qtutils as rvqt

# for UI, seems that PySide is shipped with RV
try:
    from PySide import QtGui, QtCore, QtOpenGL
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


# main class for our plugin
class MyPlugin(rvt.MinorMode):
    def __init__(self):
        super(MyPlugin, self).__init__()

        self.ui_is_opened = False

        # mandatory : define the plugin for RV
        self.init(
            "pluginName",
            [("new-source", self.new_source_event, "This is an event listener")],  # our event listeners
            None,  # overrideBindings : no idea what this does... globalBindings (on the line above) work fine
            [("pluginMenu", [("Open UI", self.menu_open_ui, None, self.menu_ui_is_opened)])]  # integration in menu bar
        )

        # load a custom settings saved in RV
        if bool(rvc.readSettings("myPlugin", "uiIsOpened", False)):
            self.menu_open_ui()

    # region UI
    def build_ui(self):
        print("Opening UI")

        # create a dock widget
        self.dock_widget = QDockWidget("My plugin window")
        self.dock_widget.closeEvent = self.dock_close_event
        self.test_widget = QLabel("Hello world")
        self.dock_widget.setWidget(self.test_widget)  # add content

        # Gets the current RV session windows as a PySide QMainWindow and add our QDockWidget
        rv_window = rvqt.sessionWindow()
        rv_window.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)

        # save UI state to settings
        self.ui_is_opened = True
        rvc.writeSettings("myPlugin", "uiIsOpened", self.ui_is_opened)

    def dock_close_event(self, *args):
        self.ui_is_opened = False
        rvc.writeSettings("myPlugin", "uiIsOpened", self.ui_is_opened)
    # endregion

    # region EVENT HANDLING
    def new_source_event(self, *args):
        """ This will trigger when a user add a new media in RV """
        print("Event 'new-source' triggered, args : {}".format(args))
        print("Sources are : {}".format(rvc.sources()))
        self.test_widget.setText("\n".join([s[0] for s in rvc.sources()]))
    # endregion

    # region MENU
    def menu_ui_is_opened(self):
        """
        This is called by the menu item when shown to know if it should be checked, muted, etc...
        In our case we add a checkmark if the UI is already opened and remove it when closed
        """
        if self.ui_is_opened:
            return rvc.CheckedMenuState
        return rvc.UncheckedMenuState

    def menu_open_ui(self, *args):
        """ Either build and show the UI or kill it """
        if not self.ui_is_opened:
            self.build_ui()
        else:
            rv_window = rvqt.sessionWindow()
            rv_window.removeDockWidget(self.dock_widget)
            self.dock_close_event()
    # endregion


def createMode():
    # this is mandatory for rv to properly load the plugin
    return MyPlugin()
