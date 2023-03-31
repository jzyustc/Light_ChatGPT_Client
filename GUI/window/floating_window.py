import sys
import hashlib

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
		self.actionA = QAction(QIcon('data/images/user.png'), u'user', self)
		self.groupBox_menu.addAction(self.actionA)
		self.actionA.triggered.connect(self.on_user_window_open)

		# second item : close the whole app
		self.actionB = QAction(QIcon('data/images/close.png'), u'close', self)
		self.groupBox_menu.addAction(self.actionB)
		self.actionB.triggered.connect(lambda : self.close_app_signal.emit())

		# menus position
		self.groupBox_menu.popup(QCursor.pos())

	def on_user_window_open(self):
		# create user_window, and get user information to fill in the textform
		user_window = UserWindow()

		# position
		x = self.pos().x() - user_window.w
		y = self.pos().y() - (user_window.h - self.h) / 2
		user_window.set_pos(x, y)

		# signal
		self.get_user_signal.emit(user_window)

		# show
		user_window.show()

		# set the close signal event
		user_window.save_user_info_signal.connect(self.on_user_window_save)

	def on_user_window_save(self, user_window):
		# when user_window closes, get the uid and password, then set them into user information
		uid = user_window.uid_text_input.toPlainText()
		password = user_window.password_text_input.toPlainText()

		def judge_uid_legal(uid):
			# length
			len_judge = len(uid) == 4
			if not len_judge:
				return False, "uid must be a number wiuth a length of 4"
			
			# is number
			digit_judge = True
			for s in uid:
				digit_judge = digit_judge & s.isdigit()
			if not digit_judge:
				return False, "uid must be a number wiuth a length of 4"
			
			# legal
			return True, "legal"
		
		def hash_password_str(password):
			return hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
		
		# judge if uid is legal
		uid_legal, error_msg = judge_uid_legal(uid) 
		if not uid_legal:
			QMessageBox.warning(self, "error", error_msg, QMessageBox.Cancel)
			return
		
		# save info
		print(password, hash_password_str(password))
		self.set_user_signal.emit(uid, hash_password_str(password))

		# close
		QMessageBox.information(self, 'save', 'Succeed to set user!', QMessageBox.Yes, QMessageBox.Yes)
		user_window.on_window_close()

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
				self.out_of_screen_set_pos()
			else:
				# click event
				self.switch_main_window_signal.emit()

	def out_of_screen_set_pos(self):
		# when the window is out of the screen
		device_h, device_w, x, y = self.get_device_shape_and_pos()
		x = max(0, min(x, device_w - self.w))
		y = max(0, min(y, device_h - self.h))
		self.set_pos(x, y)


	def get_device_shape_and_pos(self):
		device = QApplication.desktop()
		device_h = device.height()
		device_w = device.width()
		x, y = self.pos().x(), self.pos().y()
		return device_h, device_w, x, y
	
	'''
	control
	'''
	def set_pos(self, x, y):
		self.move(x, y)