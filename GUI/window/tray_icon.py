import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
 
 
class TrayIcon(QSystemTrayIcon):
	def __init__(self, icon_path, parent=None):
		super().__init__()
		self.parent = parent
		
		# create menu
		self.menu = QMenu()
		self.showAction = QAction("hide", self, triggered=self.show_or_hide)
		self.hotkeyAction = QAction("disable hot key", self, triggered=self.global_hot_key_enable_or_disable)
		self.quitAction = QAction("close", self, triggered=self.close)
 
		self.menu.addAction(self.showAction)
		self.menu.addAction(self.hotkeyAction)
		self.menu.addAction(self.quitAction)
		self.setContextMenu(self.menu)
 
		self.setIcon(QIcon(icon_path))
		self.icon = self.MessageIcon()
 
	def show_or_hide(self):
		if self.parent.is_hidden:
			self.parent.show()
			self.showAction.setText("hide")
		else:
			self.parent.hide()
			self.showAction.setText("show")
 
	def global_hot_key_enable_or_disable(self):
		if self.parent.is_global_host_key_enabled:
			self.parent.is_global_host_key_enabled = False
			self.hotkeyAction.setText("enable hot key")
		else:
			self.parent.is_global_host_key_enabled = True
			self.hotkeyAction.setText("disable hot key")
 
	def close(self):
		self.parent.close()
 

 
if __name__ == '__main__':
   app = QApplication(sys.argv)
   tray = TrayIcon()
   tray.show()
   sys.exit(app.exec_())