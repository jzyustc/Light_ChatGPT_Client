import sys
import time
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GUI.api.google_translation_api import GoogleTranslation_API
from GUI.utils.local_hot_key import LocalHotkey


class GoogleTranslationWindow(QWidget):

	def __init__(self, parent, title):
		super().__init__(parent)
		self.parent = parent
		self.title = title

		# info
		self.display_h = 280
		self.w = self.parent.w
		self.h = self.parent.h - self.parent.title_h
		self.font = self.parent.font

        # hot key
		self.hot_keys = LocalHotkey(self)
		self.set_hot_keys()

        # style
		self.set_font_background()		            # font for the background 
		self.is_translation_empty = True		# no translation

		# flag
		self.new_translation_enabled = True	# is new_translation_button enabled

		# GUI
		self.window_UI()
		self.display_UI()
		self.control_UI()
		
        # add to parent
		self.parent.plugins_layout.addWidget(self)
        
	def set_info(self):
		self.url = self.parent.parent.url
		
	def set_font_background(self):
		self.font_background = QFont()
		self.font_background.setPointSize(20)
		self.font_background.setFamily(self.parent.font_type)
		
	def set_hot_keys(self):
		self.hot_keys.add_hot_key(Qt.ControlModifier, Qt.Key_N, self.new_translation)

	'''
	GUI
	'''
	def window_UI(self):
		# set window size
		self.setObjectName("translate")
		self.setFixedSize(self.w, self.h)

		# set window
		self.window_layout = QGridLayout()
		self.window_layout.setContentsMargins(0, 0, 0, 0)
		self.setStyleSheet(f"border-top:none;")
		self.setLayout(self.window_layout)

	def get_vertical_scroll_bar_style(self, s):
		s1, s2, s3, s4, s5 = int(0 * s), int(4* s), int(10 * s), int(20 * s), int(10 * s)
		style_sheet = f"QScrollBar:vertical" + "{" \
					  f"width:{s5}px;background-color:#ffffff;" \
					  f"margin:0px,0px,0px,0px;" \
					  f"padding-top:0px;padding-bottom:0px;padding-right:{s1}px;" + "}" \
					  f"QScrollBar::handle:vertical" + "{" \
					  f"background: rgba(0, 0, 0, 20);min-height:{s4}px;" + "}" \
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

	def display_UI(self):
		# display UI includes content in the middle (question / answer items, or no_translation display)

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
		self.display_scroll_bar_width = int(10 * s)
		self.display_scroll.verticalScrollBar().setStyleSheet(self.get_vertical_scroll_bar_style(s))

		self.display_scroll.verticalScrollBar().rangeChanged.connect(
			lambda: self.display_scroll.verticalScrollBar().setValue(
				self.display_scroll.verticalScrollBar().maximum()
			)
		)	# listen for dynamic change

		self.display_scroll.setWidget(self.display_table)

		# used when no translation:
		self.no_translation_image_block = QWidget()
		self.no_translation_image_block.setFixedSize(self.w, self.display_h - 20)
		self.no_translation_image_block_layout = QGridLayout()
		self.no_translation_image_block.setLayout(self.no_translation_image_block_layout)
		self.no_translation_image_block_layout.setAlignment(Qt.AlignCenter)

		self.no_translation_image = QLabel()
		self.no_translation_image.setText("Google Translation \(^_^)/ ")
		self.no_translation_image.setFont(self.font_background)

		self.no_translation_image_block_layout.addWidget(self.no_translation_image, 0, 0)
		self.display_table_layout.addWidget(self.no_translation_image_block)

		# add to main window
		self.window_layout.addWidget(self.display_scroll)

	def control_UI(self):
		# control UI includes content in the bottom ("send" button, question input box, "new translation" button)

		h =  self.h - self.display_h - 20

		# set control
		self.control_widget = QWidget()
		self.control_widget.setFixedSize(self.w, h + 20)
		self.control_layout = QHBoxLayout()
		self.control_layout.setContentsMargins(10, 10, 10, 10)
		self.control_layout.setSpacing(10)

		# button : send
		self.button_send = QLabel()
		self.button_send.mousePressEvent = lambda event : self.translate()
		self.button_send.setFixedSize(h // 2 , h // 2)
		self.button_send.setPixmap(QPixmap("data/images/send.png"))
		self.button_send.setScaledContents(True)

		# button : new translation
		self.button_new_translation = QLabel()
		self.button_new_translation.mousePressEvent = lambda event : self.new_translation()
		self.button_new_translation.setFixedSize(h // 2 , h // 2)
		self.button_new_translation.setPixmap(QPixmap("data/images/new.png"))
		self.button_new_translation.setScaledContents(True)

		# text : input
		self.text_input_style_sheet = f"border:1px solid #ccc;border-radius:5px;"
		self.text_input = QTextEdit()
		self.text_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.text_input.setStyleSheet(self.text_input_style_sheet)
		self.text_input.setFont(self.font)

		if not hasattr(self.text_input, "keyPressEventRaw"):
			self.text_input.keyPressEventRaw = self.text_input.keyPressEvent
		self.text_input.keyPressEvent = self.enter_press_event

		self.text_input.verticalScrollBar().setStyleSheet(self.get_vertical_scroll_bar_style(s=1))

		# add to control
		self.control_layout.addWidget(self.button_send)
		self.control_layout.addWidget(self.text_input)
		self.control_layout.addWidget(self.button_new_translation)

		self.control_widget.setLayout(self.control_layout)
		self.control_widget.setFont(self.font)

		# add to main window
		self.window_layout.addWidget(self.control_widget)

	'''
	API
	'''
	def add_display_item(self, text, color):
		# add an item of question / answer for displaying
		# text : text of question / answer
		# color : background color of the item

		s = int(self.display_scroll_bar_width * 1.5)

		# display text
		display_text = QTextBrowser()
		display_text.setText(text)
		display_text.setFont(self.font)
		display_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		display_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		
		display_text.document().setTextWidth(self.w - 4 * s)
		display_text_h = display_text.document().size().height() + 25
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
		display_item_layout.setContentsMargins(0, 10, 0, 10)

		display_item.setLayout(display_item_layout)

		self.display_items.append(display_item)
		self.display_table_layout.addWidget(display_item)

	def translate(self):
		# get text of the question
		text = self.text_input.toPlainText()
		if len(text) == 0:
			return
		self.text_input.setText("")
		self.unable_text_input()

		# add question display
		self.add_display_item(text, "#ffffff")

		# if there is no previous translation, start a new translation
		if self.is_translation_empty:
			self.no_translation_image_block.close()
			self.is_translation_empty = False

		# Google Translation API
		google_translate_api = GoogleTranslation_API(url=self.url, text=text.strip().strip("\n"))
		google_translate_api.get_translated_signal.connect(lambda : {
				self.add_display_item(google_translate_api.translated, "#f7f7f8"),
				self.enable_text_input()
			})	# add answer
		google_translate_api.start()

	def unable_text_input(self):
		self.text_input.setReadOnly(True)
		# self.text_input.setTextInteractionFlags(Qt.NoTextInteraction)
		self.text_input.viewport().setCursor(Qt.ArrowCursor)
		self.text_input.setStyleSheet(f"{self.text_input_style_sheet}background:#f7f7f8")

		# unable new_translation
		self.new_translation_enabled = False

		# loading...
		text = "loading"
		self.num = 0
		self.timer = QTimer()

		def set_loading_text():
			text_loading = text + self.num * "."
			self.text_input.setText(text_loading)
			self.num = (self.num + 1) % 6

		set_loading_text()
		self.timer.timeout.connect(set_loading_text)
		self.timer.start(500)
		
	def enable_text_input(self):
		self.text_input.setReadOnly(False)
		# self.text_input.setTextInteractionFlags(Qt.TextEditorInteraction)
		self.text_input.viewport().setCursor(Qt.IBeamCursor)
		self.text_input.setStyleSheet(f"{self.text_input_style_sheet}background:#ffffff")

		# enable new_translation
		self.new_translation_enabled = True

		# loading...
		self.timer.stop()
		self.text_input.setText("")

	def new_translation(self):
		# create a new translation
		if self.new_translation_enabled:
			# delete all previous translations
			for display_item in self.display_items:
				display_item.deleteLater()
			self.display_items = []

			# show the no_translation display
			if not self.is_translation_empty:
				self.no_translation_image_block.show()
				self.is_translation_empty = True

	'''
	event
	'''
	def enter_press_event(self, event):
		enter_key = [Qt.Key_Enter, Qt.Key_Return]
		if event.modifiers() == Qt.ControlModifier and event.key() in enter_key:
			self.text_input.textCursor().insertText('\n')
		elif event.key() in enter_key:
			self.translate()
		else:
			self.text_input.keyPressEventRaw(event)


plugin = {
	"title" : "translate",
	"window" : GoogleTranslationWindow,
}

__all__ = [plugin]