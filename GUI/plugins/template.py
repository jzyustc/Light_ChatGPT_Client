from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GUI.utils.local_hot_key import LocalHotkey

class TemplateWindow(QWidget):

	def __init__(self, parent, title):
		super().__init__(parent)
		self.parent = parent
		self.title = title

        # hot key
		self.hot_keys = LocalHotkey(self)
		self.set_hot_keys()

		# GUI : set you UI here
        ## e.g., set the main window
        ## self.window_layout = QGridLayout()
        ## self.setLayout(self.window_layout)

        # add to parent
		self.parent.plugins_layout.addWidget(self)
    
		# set focus
		self.set_focus()

	def set_info(self):
		# set the needed infomation here
        ## e.g., get url from the client class
        ## self.url = self.parent.parent.url 
		return

	def set_hot_keys(self):
		# set the hot key here
        ## e.g., Ctrl + n => trigger function self.ctrl_n
        ## self.hot_keys.add_hot_key(Qt.ControlModifier, Qt.Key_N, self.ctrl_n)
		return

	def set_focus(self):
		# set the focusing widget
		## e.g., set focus on self.text
		## self.text_input.setFocus()
		return


plugin = {
	"title" : "template plugin",    # it will be shown in the title of the main_window 
	"window" : TemplateWindow,      # the window class
}

__all__ = [plugin]