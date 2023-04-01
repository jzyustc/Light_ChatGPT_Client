import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GUI.utils.position import judge_in_region

class PlusinsMenuWindow(QMainWindow):
	switch_plugin_signal = pyqtSignal(int)		# signal to switch the plugin
	
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.plugins_info = parent.plugins_info

		# info
		self.w = self.parent.title_text.width()
		self.h = self.parent.title_h
		self.font_type = "Consolas"

		self.is_in_region = False

		# style
		self.font = self.parent.font		        # font

		# GUI
		self.main_UI()
		for k in self.plugins_info:
			self.add_plugin(k)

	'''
	GUI
	'''
	def main_UI(self):
		# set window type
		self.setWindowFlag(Qt.FramelessWindowHint)	# without framework
		self.setWindowFlag(Qt.WindowStaysOnTopHint)	# pin to the top
		self.setWindowFlag(Qt.SubWindow)			# sub_window
		self.setAutoFillBackground(False)

		# set window size
		self.setObjectName("user")
		self.setFixedWidth(self.w)

		# set main window
		self.main_widget = QWidget()
		self.main_layout = QGridLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_widget.setStyleSheet(f"border-top:none;background-color:#f8f8f8")
		self.main_widget.setLayout(self.main_layout)

		self.setCentralWidget(self.main_widget)


	def add_plugin(self, k):
		plugin_info = self.plugins_info[k]

		plugin_button = QLabel()
		plugin_button.setText(plugin_info["title"])
		plugin_button.setFont(self.font)
		plugin_button.mousePressEvent = lambda event: self.switch_plugin_signal.emit(k)

		self.main_layout.addWidget(plugin_button)

	'''
	event
	'''
	def enterEvent(self, event):
		self.show()

	def leaveEvent(self, event):
		main_pos = self.parent.pos()
		main_x, main_y = main_pos.x(), main_pos.y()
		if not judge_in_region(self.parent.title_text, main_x, main_y):
			self.hide()

	def on_window_close(self):
		self.close()
		self.deleteLater()

	'''
	control
	'''
	def set_pos(self, x, y):
		self.move(x, y)