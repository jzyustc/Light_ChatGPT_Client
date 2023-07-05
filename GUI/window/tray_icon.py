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
		self.quitAction = QAction("close", self, triggered=self.close)
 
		self.menu.addAction(self.showAction)
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

	def close(self):
		self.parent.close()
 