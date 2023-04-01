import sys
import time
import json
import importlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GUI.utils.position import judge_in_region
from GUI.window.plugins_menu_window import PlusinsMenuWindow

class MainWindow(QMainWindow):
	switch_floating_window_signal = pyqtSignal(bool)	# signal to switch to the floating window
	close_app_signal = pyqtSignal()						# signal to close the app

	def __init__(self, plugins=["chatgpt"]):
		super().__init__()
		# info
		self.w = 600
		self.h = 400
		self.title_h = 40
		self.font_type = "Consolas"
		self.plugins_info = {}

		# style
		self.set_font()		# font
		self.op = 1.		# opacity of the window

		# flag
		self.signal_move = False		# title move

		# GUI
		self.main_UI()
		self.title_UI()
		self.plugins_UI()

		# plugins
		self.load_plugins(plugins)


	def set_font(self):
		self.font = QFont()
		self.font.setPointSize(11)
		self.font.setFamily(self.font_type)

	def load_plugins(self, plugins):
		# load plugins window
		for i in range(len(plugins)):
			plugin_name = plugins[i]
			plugin_pkg = importlib.import_module(f'GUI.plugins.{plugin_name}')

			plugin = plugin_pkg.plugin
			self.__setattr__(f"{plugin_name}_window", plugin["window"](self, plugin["title"]))

			self.plugins_info[i] = {
				"name" : plugin_name,
				"title" : plugin["title"]
			}
			print(f"Plugin : {plugin_name} loaded")

		# load plugin menu
		self.plugins_menu_window = PlusinsMenuWindow(self)
		self.plugins_menu_window.switch_plugin_signal.connect(self.switch_plugin)

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
		self.setObjectName("main")
		self.setFixedSize(self.w, self.h)

		# set main window
		self.main_widget = QWidget()
		self.main_layout = QGridLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_widget.setStyleSheet(f"border-top:none;background-color:#ffffff")
		self.main_widget.setLayout(self.main_layout)

		self.main_widget.wheelEvent = self.wheel_on_window_event

		self.setCentralWidget(self.main_widget)

	def title_UI(self):
		# title UI includes the title

		# set title
		self.title_widget = QWidget()
		self.title_widget.setFixedSize(self.w, self.title_h)
		self.title_layout = QHBoxLayout()
		self.title_layout.setContentsMargins(20, 0, 10, 0)
		self.title_layout.setSpacing(0)
		self.title_widget.wheelEvent = self.wheel_on_title_event
		self.title_widget.mousePressEvent = self.press_on_title_event
		self.title_widget.mouseMoveEvent = self.move_on_title_event
		self.title_widget.mouseReleaseEvent = self.release_on_title_event

		# button : new chat
		self.title_text = QLabel()
		self.title_text.setText("light chat")
		self.title_text.setFixedSize(self.title_h * 4, self.title_h)
		self.title_text.setFont(self.font)
		self.title_text.enterEvent = self.enter_title_text_event
		self.title_text.leaveEvent = self.leave_title_text_event

		# button : switch
		self.button_switch_floating_window = QLabel()
		self.button_switch_floating_window.mousePressEvent = lambda event : self.switch_floating_window_signal.emit(False)
		self.button_switch_floating_window.setFixedSize(self.title_h - 10, self.title_h - 10)
		self.button_switch_floating_window.setPixmap(QPixmap("data/images/shrink.png"))
		self.button_switch_floating_window.setScaledContents(True)

		# add to title
		self.title_layout.addWidget(self.title_text)
		self.title_layout.addStretch(1)
		self.title_layout.addWidget(self.button_switch_floating_window)

		self.title_widget.setLayout(self.title_layout)
		self.title_widget.setFont(self.font)

		# add to main window
		self.main_layout.addWidget(self.title_widget)

	def plugins_UI(self):
		# set plugins displaying
		self.plugins_widget = QWidget()
		self.plugins_widget.setFixedSize(self.w, self.h - self.title_h)
		self.plugins_layout = QStackedLayout()
		self.plugins_layout.setContentsMargins(0, 0, 0, 0)
		self.plugins_layout.setSpacing(0)
		self.plugins_widget.setLayout(self.plugins_layout)

		# add to main window
		self.main_layout.addWidget(self.plugins_widget)

	'''
	event
	'''
	def set_window_opacity_half_tmp(self):
		self.setWindowOpacity(self.op * 0.5)

	def set_window_opacity(self, op):
		self.setWindowOpacity(op)

	def change_window_opacity(self, angleY):
		if angleY > 0:
			self.op = min(1., self.op + 0.1)
		else:
			self.op = max(0.01, self.op - 0.1)
		self.setWindowOpacity(self.op)

	def wheel_on_window_event(self, event):
		if self.op <= 0.3:
			angle = event.angleDelta() / 8
			angleY = angle.y()
			self.change_window_opacity(angleY)

	def wheel_on_title_event(self, event):
		if self.op > 0.3:
			angle = event.angleDelta() / 8
			angleY = angle.y()
			self.change_window_opacity(angleY)

	def press_on_title_event(self, event):
		if event.buttons() == Qt.LeftButton:
			# left button => moving event
			self.mouse_drag_pos = event.globalPos() - self.pos()
			self.signal_move = False

	def move_on_title_event(self, event):
		if event.buttons() == Qt.LeftButton:
			self.move(event.globalPos() - self.mouse_drag_pos)
			self.signal_move = True

			# out of screen : change opacity
			device_h, device_w, x, y = self.get_device_shape_and_pos()
			if x < 0 or x > device_w - self.w or y < 0 or y > device_h - self.h:
				self.set_window_opacity_half_tmp()
			else:
				self.set_window_opacity(self.op)

	def release_on_title_event(self, event):
		# listen event : mouse release
		if event.button() == Qt.LeftButton:
			if self.signal_move:
				# move event : canceling the moving
				self.signal_move = False
		
				# out of screen : switch
				device_h, device_w, x, y = self.get_device_shape_and_pos()
				if x < 0 or x > device_w - self.w or y < 0 or y > device_h - self.h:
					self.switch_floating_window_signal.emit(True)

	def enter_title_text_event(self, event):
		x, y = self.pos().x(), self.pos().y()
		self.plugins_menu_window.set_pos(x + self.title_text.pos().x(), y + self.title_h) 
		self.plugins_menu_window.show()

	def leave_title_text_event(self, event):
		if not judge_in_region(self.plugins_menu_window):
			self.plugins_menu_window.hide()

	def switch_plugin(self, k):
		self.plugins_layout.setCurrentIndex(k)
		self.title_text.setText(self.plugins_info[k]["title"])
		self.plugins_menu_window.hide()

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