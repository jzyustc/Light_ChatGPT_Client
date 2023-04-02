import sys
import hashlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from GUI.window.user_window import UserWindow
from GUI.window.settings_window import SettingsWindow


class FloatingWindow(QMainWindow):
	switch_main_window_signal = pyqtSignal()	# signal to switch to the main window
	to_tray_signal = pyqtSignal()				# signal to shrink to the tray icon
	close_app_signal = pyqtSignal()				# signal to close the app
	set_user_signal = pyqtSignal(str, str)		# signal to set user information
	set_settings_signal = pyqtSignal(list, dict)		# signal to set settings

	def __init__(self, icon_path, parent=None):
		super().__init__()
		self.parent = parent

		# info
		self.w = 100
		self.h = 100
		self.icon_path = icon_path

		# GUI
		self.main_UI()
		self.switch_main_window_icon_UI()
		self.mouse_right_click_menu_UI()
		self.user_window = None

		self.op_leave = 0.5		# opacity of window when mouse leave the icon
		self.op_leave_time = 0	# time to set the opacity
		self.setWindowOpacity(self.op_leave)

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
		self.action_user = QAction(QIcon('data/images/user.png'), u'user', self)
		self.groupBox_menu.addAction(self.action_user)
		self.action_user.triggered.connect(self.on_user_window_open)

		# second item : settings
		self.action_settings = QAction(QIcon('data/images/settings.png'), u'settings', self)
		self.groupBox_menu.addAction(self.action_settings)
		self.action_settings.triggered.connect(self.on_settings_window_open)

		# third item : tray
		self.action_tray = QAction(QIcon('data/images/tray.png'), u'to tray', self)
		self.groupBox_menu.addAction(self.action_tray)
		self.action_tray.triggered.connect(lambda : self.to_tray_signal.emit())

		# forth item : close the whole app
		self.action_close = QAction(QIcon('data/images/close.png'), u'close', self)
		self.groupBox_menu.addAction(self.action_close)
		self.action_close.triggered.connect(lambda : self.close_app_signal.emit())

		# menus position
		self.groupBox_menu.popup(QCursor.pos())

	def on_user_window_open(self):
		# create user_window, and get user information to fill in the textform
		user_window = UserWindow(self)

		# position
		x = self.pos().x() - user_window.w
		y = self.pos().y() - (user_window.h - self.h) / 2
		user_window.set_pos(x, y)

		# set contents
		user_window.uid_text_input.setText(self.parent.uid)

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
		self.set_user_signal.emit(uid, hash_password_str(password))

		# close
		QMessageBox.information(self, 'save', 'Succeed to set user!', QMessageBox.Yes, QMessageBox.Yes)
		user_window.on_window_close()

	def on_settings_window_open(self):
		# create settings_window, and get settings information to fill in the textform
		settings_window = SettingsWindow(self)

		# position
		x = self.pos().x() - settings_window.w
		y = self.pos().y() - (settings_window.h - self.h) / 2
		settings_window.set_pos(x, y)

		# set contents
		settings_window.settings_block_layout.addStretch(2)

		## for global_hot_keys
		for content in self.parent.settings["global_hot_keys"]:
			key = self.parent.settings["global_hot_keys"][content]["key"]
			text = self.parent.settings["global_hot_keys"][content]["text"]

			# create item
			item = settings_window.item_UI(text, key)

			# logging
			settings_window.settings_list.append({
					"keys" : ["global_hot_keys", content],
					"item" : item
				})
			
			# add to layout
			settings_window.settings_block_layout.addWidget(item)
			settings_window.settings_block_layout.addStretch(1)

		settings_window.settings_block_layout.addStretch(1)
		settings_window.settings_block_layout.addWidget(settings_window.save_button_block)
		settings_window.settings_block_layout.addStretch(2)

		# show
		settings_window.show()

		# set the close signal event
		settings_window.save_settings_signal.connect(self.on_settings_window_save)

	def on_settings_window_save(self, settings_window):
		# when settings_window closes, get the uid and password, then set them into settings information
		settings_global_hot_keys = {}

		for setting in settings_window.settings_list:

			# for global_hot_keys : get keys
			if setting["keys"][0] == "global_hot_keys":
				content = setting["keys"][1]
				item = setting["item"]
				key = item.findChild(QTextEdit, "text_input").toPlainText()
				
				settings_global_hot_keys[content] = {}
				settings_global_hot_keys[content]["key"] = key

		# for global_hot_keys : save info
		self.set_settings_signal.emit(["global_hot_keys"], settings_global_hot_keys)

		# close
		QMessageBox.information(self, 'save', 'Succeed to set settings!', QMessageBox.Yes, QMessageBox.Yes)
		settings_window.on_window_close()

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
	
	def leaveEvent(self, event):
		timer = QTimer()

		def on_timer():
			self.setWindowOpacity(self.op_leave)
			timer.stop()

		timer.timeout.connect(on_timer)
		timer.start(self.op_leave_time * 1000)
		

	def enterEvent(self, event):
		self.setWindowOpacity(1.)
	
	'''
	control
	'''
	def set_pos(self, x, y):
		self.move(x, y)