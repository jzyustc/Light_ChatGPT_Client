import sys
import time
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GUI.api.chatgpt_server_api import ChatGPT_API

class MainWindow(QMainWindow):
	switch_floating_window_signal = pyqtSignal()	# signal to switch to the floating window

	def __init__(self, url, uid, hash_password):
		super().__init__()
		# info
		self.url = url
		self.uid = uid
		self.hash_password = hash_password

		self.w = 600
		self.h = 400
		self.title_h = 40
		self.display_h = 280
		self.font_type = "Consolas"

		# style
		self.set_font()		# font
		self.op = 1.		# opacity of the window
		self.is_chat_empty = True	# no chat
		self.signal_move = False	# title move

		# GUI
		self.main_UI()
		self.title_UI()
		self.display_UI()
		self.control_UI()


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
		self.setObjectName("chat")
		self.setFixedSize(self.w, self.h)

		# set main window
		self.main_widget = QWidget()
		self.main_layout = QGridLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_widget.setStyleSheet(f"border-top:none;background-color:#ffffff")
		self.main_widget.setLayout(self.main_layout)

		self.main_widget.wheelEvent = self.wheel_on_window_event

		self.setCentralWidget(self.main_widget)

	def get_vertical_scroll_bar_style(self, s1, s2, s3, s4, s5):
		style_sheet = f"QScrollBar:vertical" + "{" \
					  f"width:{s5}px;background-color:#ffffff;" \
					  f"margin:0px,0px,0px,0px;" \
					  f"padding-top:0px;padding-bottom:0px;padding-right:{s1}px;" + "}" \
					  f"QScrollBar::handle:vertical" + "{" \
					  f"background: rgb(0, 0, 0, 20);min-height:{s4}px;" + "}" \
					  f"QScrollBar::handle:vertical:hover" + "{" \
					  f"border-radius: {s2}px;width:{s3}px;" \
					  f"margin:0px,0px,0px,0px;" \
					  f"margin:0px,0px,0px,0px;" \
					  f"border-radius: {s2}px;width:{s3}px;"\
					  f"background:rgb(0, 0, 0, 30);min-height:{s4}px;" + "}"\
					  f"QScrollBar::add-line:vertical" + "{"\
					  f"width: 0px;height: 0px; background:#ffffff" + "}" \
					  f"QScrollBar::sub-line:vertical" + "{"\
					  f"width: 0px;height: 0px; background:#ffffff" + "}"
		return style_sheet

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
		self.title_text.setFixedHeight(self.title_h)
		self.title_text.setFont(self.font)

		# button : switch
		self.button_switch_floating_window = QLabel()
		self.button_switch_floating_window.mousePressEvent = lambda event : self.switch_floating_window_signal.emit()
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

	def display_UI(self):
		# display UI includes content in the middle (question / answer items, or no_chat display)

		# display table
		self.display_table = QWidget()
		self.display_table_layout = QVBoxLayout()
		self.display_table_layout.setContentsMargins(0, 0, 0, 0)
		self.display_table_layout.setSpacing(0)
		self.display_table.setLayout(self.display_table_layout)

		self.display_table_layout.addStretch(1)
		self.display_items = []

		# scroll
		self.display_scroll = QScrollArea()
		self.display_scroll.setWidgetResizable(True)			# enable dynamic
		self.display_scroll.setBackgroundRole(QPalette.Light)
		self.display_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.display_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.display_scroll.setFixedSize(self.w, self.display_h)

		s = 1.5
		s1, s2, s3, s4, s5 = int(0 * s), int(4* s), int(10 * s), int(20 * s), int(10 * s)
		self.display_scroll_bar_style = [s1, s2, s3, s4, s5]
		self.display_scroll.verticalScrollBar().setStyleSheet(self.get_vertical_scroll_bar_style(s1, s2, s3, s4, s5))

		self.display_scroll.verticalScrollBar().rangeChanged.connect(
			lambda: self.display_scroll.verticalScrollBar().setValue(
				self.display_scroll.verticalScrollBar().maximum()
			)
		)	# listen for dynamic change

		self.display_scroll.setWidget(self.display_table)

		# used when no chat:
		self.no_chat_image_block = QWidget()
		self.no_chat_image_block.setFixedSize(self.w, self.display_h)
		self.no_chat_image_block_layout = QGridLayout()
		self.no_chat_image_block.setLayout(self.no_chat_image_block_layout)
		self.no_chat_image_block_layout.setAlignment(Qt.AlignCenter)

		self.no_chat_image = QLabel()
		self.no_chat_image.setText("Light Chat ^_^ ~")

		font = QFont()
		font.setPointSize(20)
		font.setFamily(self.font_type)
		self.no_chat_image.setFont(font)

		self.no_chat_image_block_layout.addWidget(self.no_chat_image, 0, 0)
		self.display_table_layout.addWidget(self.no_chat_image_block)

		# add to main window
		self.main_layout.addWidget(self.display_scroll)

	def control_UI(self):
		# control UI includes content in the bottom ("send" button, question input box, "new chat" button)

		h =  self.h - self.display_h - self.title_h - 20

		# set control
		self.control_widget = QWidget()
		self.control_widget.setFixedSize(self.w, h + 20)
		self.control_layout = QHBoxLayout()
		self.control_layout.setContentsMargins(10, 10, 10, 10)
		self.control_layout.setSpacing(10)

		# button : send
		self.button_send = QLabel()
		self.button_send.mousePressEvent = lambda event : self.ask_question()
		self.button_send.setFixedSize(h // 2 , h // 2)
		self.button_send.setPixmap(QPixmap("data/images/send.png"))
		self.button_send.setScaledContents(True)

		# button : new chat
		self.button_new_chat = QLabel()
		self.button_new_chat.mousePressEvent = lambda event : self.new_chat()
		self.button_new_chat.setFixedSize(h // 2 , h // 2)
		self.button_new_chat.setPixmap(QPixmap("data/images/new.png"))
		self.button_new_chat.setScaledContents(True)

		# text : input
		self.text_input = QTextEdit()
		self.text_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.text_input.setStyleSheet(f"border:1px solid #ccc;border-radius:5px;box-shadow:#ccc 0px 0px 10px;")
		self.text_input.setFont(self.font)


		s = 1
		s1, s2, s3, s4, s5 = int(0 * s), int(4* s), int(10 * s), int(20 * s), int(10 * s)
		self.text_input.verticalScrollBar().setStyleSheet(self.get_vertical_scroll_bar_style(s1, s2, s3, s4, s5))

		# add to control
		self.control_layout.addWidget(self.button_send)
		self.control_layout.addWidget(self.text_input)
		self.control_layout.addWidget(self.button_new_chat)

		self.control_widget.setLayout(self.control_layout)
		self.control_widget.setFont(self.font)

		# add to main window
		self.main_layout.addWidget(self.control_widget)

	'''
	API
	'''
	def add_display_item(self, text, color):
		# add an item of question / answer for displaying
		# text : text of question / answer
		# color : background color of the item

		s = int(self.display_scroll_bar_style[-1] * 1.5)

		# display text
		display_text = QTextBrowser()
		display_text.setText(text)
		display_text.setFont(self.font)
		display_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		display_text.document().adjustSize()
		display_text_h = display_text.document().size().height() + 20
		display_text.setFixedSize(self.w - 4 * s, display_text_h)

		# left widget
		left_widget = QWidget()
		left_widget.setFixedSize(s, s)

		# left widget
		right_widget = QWidget()
		right_widget.setFixedSize(s, s)

		# display item
		display_item = QWidget()
		display_item.setFixedSize(self.w, display_text_h)
		display_item.setStyleSheet(f"border:none;background-color:{color}")
		
		display_item_layout = QHBoxLayout()
		display_item_layout.addWidget(left_widget)
		display_item_layout.addWidget(display_text)
		display_item_layout.addWidget(right_widget)
		display_item_layout.setContentsMargins(0, 10, 0, 0)
		display_item_layout.setSpacing(0)

		display_item.setLayout(display_item_layout)

		self.display_items.append(display_item)
		self.display_table_layout.addWidget(display_item)

	def ask_question(self):
		# get text of the question
		text = self.text_input.toPlainText()
		if len(text) == 0:
			return
		self.text_input.setText("")

		# add question display
		self.add_display_item(text, "#ffffff")

		# if there is no previous chat, start a new chat
		new_chat = "0"
		if self.is_chat_empty:
			self.no_chat_image_block.close()
			self.is_chat_empty = False
			new_chat = "1"

		# chatgpt API
		chatgpt_api = ChatGPT_API(url=self.url, uid=self.uid, hash_password=self.hash_password, new_chat=new_chat, question=text)
		chatgpt_api.get_answer_signal.connect(lambda : self.add_display_item(chatgpt_api.answer, "#f7f7f8"))	# add answer
		chatgpt_api.start()

	def new_chat(self):
		# create a new chat

		# delete all previous chats
		for display_item in self.display_items:
			display_item.deleteLater()
		self.display_items = []

		# show the no_chat display
		if not self.is_chat_empty:
			self.no_chat_image_block.show()
			self.is_chat_empty = True


	'''
	event
	'''
	def enter_press_event(self, event):
		enter_key = [Qt.Key_Enter, Qt.Key_Return]
			self.text_input.textCursor().insertText('\n')
		elif event.key() in enter_key:
			self.ask_question()
		else:
			self.text_input.keyPressEventRaw(event)

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

	def release_on_title_event(self, event):
		# listen event : mouse release
		if event.button() == Qt.LeftButton:
			if self.signal_move:
				# move event : canceling the moving
				self.signal_move = False
		

	'''
	control
	'''
	def set_pos(self, x, y):
		self.move(x, y)