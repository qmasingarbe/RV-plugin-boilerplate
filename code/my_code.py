# rv python libs (located here on my system => /usr/local/rv-7.3.1/plugins/Python/rv)
from rv import rvtypes as rvt
from rv import commands as rvc
from rv import extra_commands as rve
from rv import qtutils as rvqt

import sys
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


class WriteStream(object):
    def __init__(self, old_stream, callback):
        self.old_stream = old_stream
        self.callback = callback

    def write(self, text):
        self.callback("> {}".format(text))
        self.old_stream.write(text)


# main class for our plugin
class MyPlugin(rvt.MinorMode):
    ALTERNATE_VIEW_NAME = "previousVersionAuto"
    def __init__(self):
        super(MyPlugin, self).__init__()

        self.ui_is_opened = False
        self.main_view = None
        self.current_frame = 1


        rvc.showConsole()

        # mandatory : define the plugin for RV
        self.init(
            "pluginName",
            [
                ("key-down--p", self.p_pressed, "Do something on p pressed")
            ],  # our event listeners
            None,  # overrideBindings : no idea what this does... globalBindings (on the line above) work fine
            [("pluginMenu", [("Open UI dev", self.menu_open_ui, None, self.menu_ui_is_opened)])]  # integration in menu bar
        )

        # load a custom settings saved in RV
        if bool(rvc.readSettings("myPlugin", "uiIsOpened", False)):
            self.menu_open_ui()

        self.write_stream = None

    # region UI
    def build_ui(self):
        print("Opening UI")

        # create a dock widget
        self.dock_widget = QDockWidget("My plugin window")
        self.dock_widget.closeEvent = self.dock_close_event
        main_layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.dock_widget.setWidget(main_widget)
        self.log_widget = QPlainTextEdit()
        self.log_widget.setStyleSheet("color: white")
        self.log_widget.setReadOnly(True)
        main_layout.addWidget(self.log_widget)
        self.code_widget = QTextEdit()
        main_layout.addWidget(self.code_widget)
        self.exec_widget = QPushButton("Execute")
        self.exec_widget.clicked.connect(self.exec_code)
        main_layout.addWidget(self.exec_widget)

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
    def write_in_console(self, text):
        self.log_widget.appendPlainText(text)
        self.log_widget.verticalScrollBar().setValue(self.log_widget.verticalScrollBar().maximum())

    def exec_code(self, *args):
        if self.write_stream is None:
            self.write_stream = WriteStream(sys.stdout, self.write_in_console)
            sys.stdout = self.write_stream
        code = self.code_widget.toPlainText()
        self.write_in_console(code)
        exec(compile(code, '<string>', 'exec'))

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

    # for node_name in rvc.nodes():
    #     print(node_name, rvc.nodeType(node_name))

    def p_pressed(self, *args):
        self.current_frame = rvc.frame()
        if self.main_view is None:
            # store current view
            self.main_view = rvc.viewNode()
            # create alternate view if not already present
            if self.ALTERNATE_VIEW_NAME not in rvc.viewNodes():
                previous_default_sources, _ = rvc.nodeConnections("defaultSequence")  # store default sequence content
                new_source = rvc.addSourceVerbose([r"C:\Users\Quentin\Downloads\Waterman.mp4"])  # add media
                if new_source.endswith("_source"):
                    # prevent warning because previous command return a source type node and not the parent source group
                    new_source = new_source[:-7]
                # create a sequence and add the new media in
                rvc.newNode("RVSequenceGroup", self.ALTERNATE_VIEW_NAME)
                rvc.setNodeInputs(self.ALTERNATE_VIEW_NAME, [new_source])
                # restore default sequence content before as before import because it auto adds new media in
                if self.main_view == "defaultSequence":
                    rvc.setNodeInputs("defaultSequence", previous_default_sources)
            # swap to alternate view and set cursor
            rvc.setViewNode(self.ALTERNATE_VIEW_NAME)
        else:
            # resume to main view and set cursor
            rvc.setViewNode(self.main_view)
            self.main_view = None
        rvc.setFrame(self.current_frame)


def createMode():
    # this is mandatory for rv to properly load the plugin
    return MyPlugin()
