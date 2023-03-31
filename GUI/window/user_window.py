import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class UserWindow(QMainWindow):
	user_window_close_signal = pyqtSignal(QMainWindow)	    # signal sent when the window closes
	
	def __init__(self):
		super().__init__()
		# info
		self.w = 400
		self.h = 300
		self.title_h = 40
		self.font_type = "Consolas"

		# style
		self.set_font()		        # font
		self.signal_move = False	# title move

		# GUI
		self.main_UI()
		self.title_UI()
		self.user_UI()

	def set_font(self):
		self.font = QFont()
		self.font.setPointSize(11)
		self.font.setFamily(self.font_type)

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

		# label : user
		self.title_text = QLabel()
		self.title_text.setText("user")
		self.title_text.setFixedHeight(self.title_h)
		self.title_text.setFont(self.font)

		# button : close
		self.button_switch_floating_window = QLabel()
		self.button_switch_floating_window.mousePressEvent = self.on_window_close
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

	def user_UI(self):
		# user
		self.user_block = QWidget()
		self.user_block.setFixedSize(self.w, self.h - self.title_h)
		self.user_block_layout = QVBoxLayout()
		self.user_block.setLayout(self.user_block_layout)
		# self.user_block.setStyleSheet(f"border:1px solid #ccc;background-color:#888;")
		self.user_block_layout.setContentsMargins(0, 0, 0, 0)
		self.user_block_layout.setSpacing(0)

		item_h = 50
		self.uid_UI(item_h)
		self.password_UI(item_h)
		
        # add to user_block
		self.user_block_layout.addStretch(2)
		self.user_block_layout.addWidget(self.uid_block)
		self.user_block_layout.addStretch(1)
		self.user_block_layout.addWidget(self.password_block)
		self.user_block_layout.addStretch(3)

		# add to main window
		self.main_layout.addWidget(self.user_block)

	def uid_UI(self, item_h):
        # uid
		self.uid_block = QWidget()
		self.uid_block.setFixedSize(self.w, item_h)
		self.uid_block_layout = QHBoxLayout()
		self.uid_block.setLayout(self.uid_block_layout)
		self.uid_block_layout.setAlignment(Qt.AlignLeft)
		self.uid_block_layout.setContentsMargins(0, 0, 0, 0)
		self.uid_block_layout.setSpacing(0)

        ## uid title
		self.uid_title = QLabel()
		self.uid_title.setFixedSize(item_h, item_h)
		self.uid_title.setText("uid : ")
		self.uid_title.setFont(self.font)

        ## uid text input
		self.uid_text_input = QTextEdit()
		self.uid_text_input.setFixedSize(self.w - 3 * item_h, item_h)
		self.uid_text_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.uid_text_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.uid_text_input.setStyleSheet(f"border:1px solid #ccc;border-radius:5px;box-shadow:#ccc 0px 0px 10px;")
		self.uid_text_input.setFont(self.font)
		
        ## add to uid block
		self.uid_block_layout.addStretch(1)
		self.uid_block_layout.addWidget(self.uid_title)
		self.uid_block_layout.addStretch(1)
		self.uid_block_layout.addWidget(self.uid_text_input)
		self.uid_block_layout.addStretch(1)

	def password_UI(self, item_h):
        # password
		self.password_block = QWidget()
		self.password_block.setFixedSize(self.w, item_h)
		self.password_block_layout = QHBoxLayout()
		self.password_block.setLayout(self.password_block_layout)
		self.password_block_layout.setAlignment(Qt.AlignLeft)
		self.password_block_layout.setContentsMargins(0, 0, 0, 0)
		self.password_block_layout.setSpacing(0)

        ## password title
		self.password_title = QLabel()
		self.password_title.setFixedSize(item_h, item_h)
		self.password_title.setText("password : ")
		self.password_title.setFont(self.font)

        ## password text input
		self.password_text_input = QTextEdit()
		self.password_text_input.setFixedSize(self.w - 3 * item_h, item_h)
		self.password_text_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.password_text_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.password_text_input.setStyleSheet(f"border:1px solid #ccc;border-radius:5px;box-shadow:#ccc 0px 0px 10px;")
		self.password_text_input.setFont(self.font)
		
        ## add to password block
		self.password_block_layout.addStretch(1)
		self.password_block_layout.addWidget(self.password_title)
		self.password_block_layout.addStretch(1)
		self.password_block_layout.addWidget(self.password_text_input)
		self.password_block_layout.addStretch(1)

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
				
	def on_window_close(self, event):
		self.user_window_close_signal.emit(self)
