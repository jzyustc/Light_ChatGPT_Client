import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SettingsWindow(QMainWindow):
	save_settings_signal = pyqtSignal(QMainWindow)	    # signal to save the settings
	
	def __init__(self, parent=None):
		super().__init__()
		self.parent = parent

		# info
		self.w = 400
		self.h = 300
		self.title_h = 40

		# style
		self.font = self.parent.parent.main_window.font
		self.signal_move = False	# title move

		# GUI
		self.main_UI()
		self.title_UI()
		self.settings_UI()

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
		self.setObjectName("settings")
		self.setFixedSize(self.w, self.h)

		# set main window
		self.main_widget = QWidget()
		self.main_layout = QGridLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_widget.setStyleSheet(f"border-top:none;background-color:#ffffff")
		self.main_widget.setLayout(self.main_layout)

		self.setCentralWidget(self.main_widget)

	def title_UI(self):
		# set title
		self.title_widget = QWidget()
		self.title_widget.setFixedSize(self.w, self.title_h)
		self.title_layout = QHBoxLayout()
		self.title_layout.setContentsMargins(20, 0, 10, 0)
		self.title_layout.setSpacing(0)
		self.title_widget.mousePressEvent = self.press_on_title_event
		self.title_widget.mouseMoveEvent = self.move_on_title_event
		self.title_widget.mouseReleaseEvent = self.release_on_title_event

		# label : settings
		self.title_text = QLabel()
		self.title_text.setText("settings")
		self.title_text.setFixedHeight(self.title_h)
		self.title_text.setFont(self.font)

		# button : close
		self.button_switch_floating_window = QLabel()
		self.button_switch_floating_window.mousePressEvent = lambda event : self.on_window_close()
		self.button_switch_floating_window.setFixedSize(self.title_h - 10, self.title_h - 10)
		self.button_switch_floating_window.setPixmap(QPixmap("data/images/close.png"))
		self.button_switch_floating_window.setScaledContents(True)

		# add to title
		self.title_layout.addWidget(self.title_text)
		self.title_layout.addStretch(1)
		self.title_layout.addWidget(self.button_switch_floating_window)

		self.title_widget.setLayout(self.title_layout)
		self.title_widget.setFont(self.font)

		# add to main window
		self.main_layout.addWidget(self.title_widget)

	def settings_UI(self):
		# settings
		self.settings_block = QWidget()
		self.settings_block.setFixedSize(self.w, self.h - self.title_h)
		self.settings_block_layout = QVBoxLayout()
		self.settings_block.setLayout(self.settings_block_layout)
		self.settings_block_layout.setContentsMargins(0, 0, 0, 0)
		self.settings_block_layout.setSpacing(0)

		self.item_h = 50

		# settings items
		self.settings_list = []

		# save
		self.save_UI()

		# add to main window
		self.main_layout.addWidget(self.settings_block)

	def item_UI(self, title, text):
        # item
		item = QWidget()
		item.setFixedSize(self.w, self.item_h)
		item_layout = QHBoxLayout()
		item.setLayout(item_layout)
		item_layout.setAlignment(Qt.AlignLeft)
		item_layout.setContentsMargins(0, 0, 0, 0)
		item_layout.setSpacing(0)

        ## title
		item_title = QLabel()
		item_title.setFixedSize(self.w // 2 - self.item_h, self.item_h)
		item_title.setText(title)
		item_title.setFont(self.font)
		item_title.setAlignment(Qt.AlignCenter)

        ## password text input
		item_text_input = QTextEdit()
		item_text_input.setObjectName("text_input")
		item_text_input.setFixedSize(self.w // 2 - self.item_h, self.item_h)
		item_text_input.setText(text)
		item_text_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		item_text_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		item_text_input.setStyleSheet(f"border:1px solid #ccc;border-radius:5px;")
		item_text_input.setFont(self.font)
		
        ## add to password block
		item_layout.addStretch(1)
		item_layout.addWidget(item_title)
		item_layout.addStretch(1)
		item_layout.addWidget(item_text_input)
		item_layout.addStretch(1)

		return item

	def save_UI(self):
		# button
		self.save_button_block = QWidget()
		self.save_button_block.setFixedSize(self.w, self.item_h)
		self.save_button_block_layout = QHBoxLayout()
		self.save_button_block.setLayout(self.save_button_block_layout)
		self.save_button_block_layout.setContentsMargins(0, 0, 0, 0)
		self.save_button_block_layout.setSpacing(0)

		self.save_button = QPushButton("save")
		self.save_button.setFont(self.font)
		self.save_button.setFixedSize(self.w // 4, self.item_h)
		self.save_button.setStyleSheet(f"border:1px solid #ccc;border-radius:5px;background-color:#f8f8f8;")
		self.save_button.clicked.connect(self.on_save)
		self.save_button_block_layout.addStretch(1)
		self.save_button_block_layout.addWidget(self.save_button)
		self.save_button_block_layout.addStretch(1)


	'''
	event
	'''
	def press_on_title_event(self, event):
		if event.buttons() == Qt.LeftButton:
			# left button => moving event
			self.mouse_drag_pos = event.globalPos() - self.pos()
			self.signal_move = False

	def move_on_title_event(self, event):
		if event.buttons() == Qt.LeftButton:
			self.move(event.globalPos() - self.mouse_drag_pos)
			self.signal_move = True

	def release_on_title_event(self, event):
		# listen event : mouse release
		if event.button() == Qt.LeftButton:
			if self.signal_move:
				# move event : canceling the moving
				self.signal_move = False
				
	def on_save(self, event):
		self.save_settings_signal.emit(self)

	def on_window_close(self):
		self.close()
		self.deleteLater()

	'''
	control
	'''
	def set_pos(self, x, y):
		self.move(x, y)