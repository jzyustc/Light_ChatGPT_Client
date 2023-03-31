import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FloatingWindow(QMainWindow):
	switch_main_window_signal = pyqtSignal()	# signal to switch to the main window

	def __init__(self, icon_path):
		super().__init__()
		# info
		self.w = 100
		self.h = 100
		self.icon_path = icon_path

		# GUI
		self.main_UI()
		self.icon_UI_switch_main_window()

		# event info
		self.signal_move = False

	'''
	GUI
	'''
	def main_UI(self):
		# set window type
		self.setWindowFlag(Qt.FramelessWindowHint)	# without framework
		self.setWindowFlag(Qt.WindowStaysOnTopHint)	# pin to the top
		self.setWindowFlag(Qt.SubWindow)			# sub_window

		# set window shape
		self.setFixedSize(self.w, self.h)
		self.setAutoFillBackground(False)
		self.setAttribute(Qt.WA_TranslucentBackground, True)

		# set main window
		self.main_widget = QWidget()
		self.main_layout = QGridLayout()
		self.main_widget.setLayout(self.main_layout)
		self.setCentralWidget(self.main_widget)

	def icon_UI_switch_main_window(self):
		# set icon
		self.icon_switch_main_window = QLabel()
		self.icon_switch_main_window.setPixmap(QPixmap(self.icon_path))
		self.icon_switch_main_window.setScaledContents(True)

		# add to main window
		self.main_layout.addWidget(self.icon_switch_main_window)

	'''
	event
	'''
	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			# left button => moving event
			self.mouse_drag_pos = event.globalPos() - self.pos()
			# self.setCursor(QCursor(Qt.OpenHandCursor))

	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.move(event.globalPos() - self.mouse_drag_pos)
			self.signal_move = True

	def mouseReleaseEvent(self, event):
		# listen event : mouse release
		if self.signal_move:
			# move event : canceling the moving
			self.signal_move = False
			# self.setCursor(QCursor(Qt.ArrowCursor))
		else:
			# click event
			self.switch_main_window_signal.emit()

	'''
	control
	'''
	def set_pos(self, x, y):
		self.move(x, y)