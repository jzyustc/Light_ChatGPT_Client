import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GUI.window.user_window import UserWindow


class FloatingWindow(QMainWindow):
	switch_main_window_signal = pyqtSignal()	# signal to switch to the main window
	close_app_signal = pyqtSignal()				# signal to close the app
	get_user_signal = pyqtSignal(QMainWindow)	# signal to get user information in user window
	set_user_signal = pyqtSignal(str, str)		# signal to set user information

	def __init__(self, icon_path):
		super().__init__()
		# info
		self.w = 100
		self.h = 100
		self.icon_path = icon_path

		# GUI
		self.main_UI()
		self.switch_main_window_icon_UI()
		self.mouse_right_click_menu_UI()
		self.user_window = None

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

	def switch_main_window_icon_UI(self):
		# set icon
		self.icon_switch_main_window = QLabel()
		self.icon_switch_main_window.setPixmap(QPixmap(self.icon_path))
		self.icon_switch_main_window.setScaledContents(True)

		# add to main window
		self.main_layout.addWidget(self.icon_switch_main_window)

	def mouse_right_click_menu_UI(self):
		# set menu policy
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		# event trigger
		self.customContextMenuRequested.connect(self.create_rightmenu) 
		
	'''
	event
	'''
	def create_rightmenu(self):
		# set menu
		self.groupBox_menu = QMenu(self)

		# first item : user id
		self.actionA = QAction(QIcon('data/images/new.png'),u'user',self)
		self.groupBox_menu.addAction(self.actionA)
		self.actionA.triggered.connect(self.on_user_window_open)

		# second item : close the whole app
		self.actionB = QAction(QIcon('data/images/new.png'),u'close',self)
		self.groupBox_menu.addAction(self.actionB)
		self.actionB.triggered.connect(lambda : self.close_app_signal.emit())

		# menus position
		self.groupBox_menu.popup(QCursor.pos())

	def on_user_window_open(self):
		# create user_window, and get user information to fill in the textform
		user_window = UserWindow()
		self.get_user_signal.emit(user_window)
		user_window.show()

		# set the close signal event
		user_window.user_window_close_signal.connect(self.on_user_window_close)

	def on_user_window_close(self, user_window):
		# when user_window closes, get the uid and password, then set them into user information
		uid = user_window.uid_text_input.toPlainText()
		password = user_window.password_text_input.toPlainText()
		self.set_user_signal.emit(uid, password)
		user_window.close()
		user_window.deleteLater()

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
		if event.button() == Qt.LeftButton:
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