import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class UserWindow(QMainWindow):
	save_user_info_signal = pyqtSignal(QMainWindow)	    # signal to save the user information
	
	def __init__(self, parent=None):
		super().__init__()
		self.parent = parent

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

	def user_UI(self):
		# user
		self.user_block = QWidget()
		self.user_block.setFixedSize(self.w, self.h - self.title_h)
		self.user_block_layout = QVBoxLayout()
		self.user_block.setLayout(self.user_block_layout)
		self.user_block_layout.setContentsMargins(0, 0, 0, 0)
		self.user_block_layout.setSpacing(0)

		item_h = 50
		self.uid_UI(item_h)
		self.password_UI(item_h)
		self.save_UI(item_h)
		
        # add to user_block
		self.user_block_layout.addStretch(2)
		self.user_block_layout.addWidget(self.uid_block)
		self.user_block_layout.addStretch(1)
		self.user_block_layout.addWidget(self.password_block)
		self.user_block_layout.addStretch(2)
		self.user_block_layout.addWidget(self.save_button_block)
		self.user_block_layout.addStretch(2)

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
		self.uid_title.setFixedSize(int(item_h * 1.5), item_h)
		self.uid_title.setText("uid")
		self.uid_title.setFont(self.font)
		self.uid_title.setAlignment(Qt.AlignCenter)

        ## uid text input
		self.uid_text_input = QTextEdit()
		self.uid_text_input.setFixedSize(self.w - 3 * item_h, item_h)
		self.uid_text_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.uid_text_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.uid_text_input.setStyleSheet(f"border:1px solid #ccc;border-radius:5px;")
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
		self.password_title.setFixedSize(int(item_h * 1.5), item_h)
		self.password_title.setText("password")
		self.password_title.setFont(self.font)
		self.password_title.setAlignment(Qt.AlignCenter)

        ## password text input
		self.password_text_input = QTextEdit()
		self.password_text_input.setFixedSize(self.w - 3 * item_h, item_h)
		self.password_text_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.password_text_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.password_text_input.setStyleSheet(f"border:1px solid #ccc;border-radius:5px;")
		self.password_text_input.setFont(self.font)
		
        ## add to password block
		self.password_block_layout.addStretch(1)
		self.password_block_layout.addWidget(self.password_title)
		self.password_block_layout.addStretch(1)
		self.password_block_layout.addWidget(self.password_text_input)
		self.password_block_layout.addStretch(1)

	def save_UI(self, item_h):
		# button
		self.save_button_block = QWidget()
		self.save_button_block.setFixedSize(self.w, item_h)
		self.save_button_block_layout = QHBoxLayout()
		self.save_button_block.setLayout(self.save_button_block_layout)
		self.save_button_block_layout.setContentsMargins(0, 0, 0, 0)
		self.save_button_block_layout.setSpacing(0)

		self.save_button = QPushButton("save")
		self.save_button.setFont(self.font)
		self.save_button.setFixedSize(self.w // 4, item_h)
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
		self.save_user_info_signal.emit(self)

	def on_window_close(self):
		self.close()
		self.deleteLater()

	'''
	control
	'''
	def set_pos(self, x, y):
		self.move(x, y)