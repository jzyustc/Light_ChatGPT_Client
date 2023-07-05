import sys
import time
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GUI.utils.local_hot_key import LocalHotkey



class SetNameWindow(QMainWindow):
	set_name_signal = pyqtSignal(QMainWindow)	    # signal to set name
	
	def __init__(self, parent=None):
		super().__init__()
		self.parent = parent

		# info
		self.w = 400
		self.h = 300
		self.title_h = 40

		# style
		self.font = self.parent.font
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
		self.main_widget.setStyleSheet(f"border-top:none;background-color:#fafafb")
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
		self.title_text.setText("set name")
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
		self.name_item = None

		# set
		self.set_UI()

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

	def set_UI(self):
		# button
		self.set_button_block = QWidget()
		self.set_button_block.setFixedSize(self.w, self.item_h)
		self.set_button_block_layout = QHBoxLayout()
		self.set_button_block.setLayout(self.set_button_block_layout)
		self.set_button_block_layout.setContentsMargins(0, 0, 0, 0)
		self.set_button_block_layout.setSpacing(0)

		self.set_button = QPushButton("set")
		self.set_button.setFont(self.font)
		self.set_button.setFixedSize(self.w // 4, self.item_h)
		self.set_button.setStyleSheet(f"border:1px solid #ccc;border-radius:5px;background-color:#f8f8f8;")
		self.set_button.clicked.connect(self.on_set)
		self.set_button_block_layout.addStretch(1)
		self.set_button_block_layout.addWidget(self.set_button)
		self.set_button_block_layout.addStretch(1)


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
				
	def on_set(self, event):
		self.set_name_signal.emit(self)

	def on_window_close(self):
		self.close()
		self.deleteLater()

	'''
	control
	'''
	def set_pos(self, x, y):
		self.move(x, y)


class FileTransferServerWindow(QWidget):

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

		# flag
		self.clear_folders_enabled = True	# is new_folder_button enabled

		# GUI
		self.window_UI()
		self.display_UI()
		self.control_UI()
		
        # add to parent
		self.parent.plugins_layout.addWidget(self)

		# set focus
		self.set_focus()

		# read data
		self.share_data_path = "data/file_transfer_server_data.json"
		self.shared_folders = self.get_data(new=True)

		self.is_folder_empty = (len(self.shared_folders) == 0)		# no folder

	def set_info(self):
		return 
		
	def set_font_background(self):
		self.font_background = QFont()
		self.font_background.setPointSize(20)
		self.font_background.setFamily(self.parent.font_type)
		
	def set_hot_keys(self):
		return 

	def set_focus(self):
		self.text_input.setFocus()

	'''
	data
	'''
	def get_data(self, new=False):
		if new :
			with open(self.share_data_path, 'w') as share_data:
				shared_folders = {}
				json.dump(shared_folders, share_data)
		else:
			with open(self.share_data_path, 'r') as share_data:
				shared_folders = json.loads(share_data.read())
		return shared_folders
	
	def set_data(self):
		with open(self.share_data_path, 'w') as share_data:
			json.dump(self.shared_folders, share_data)
		return

	'''
	GUI
	'''
	def window_UI(self):
		# set window size
		self.setObjectName("transfer-S")
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
		# display UI includes content in the middle (question / answer items, or no_shared display)

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

		# used when no shared:
		self.no_shared_image_block = QWidget()
		self.no_shared_image_block.setFixedSize(self.w, self.display_h - 20)
		self.no_shared_image_block_layout = QGridLayout()
		self.no_shared_image_block.setLayout(self.no_shared_image_block_layout)
		self.no_shared_image_block_layout.setAlignment(Qt.AlignCenter)

		self.no_shared_image = QLabel()
		self.no_shared_image.setText("File Transfer [Server]")
		self.no_shared_image.setFont(self.font_background)

		self.no_shared_image_block_layout.addWidget(self.no_shared_image, 0, 0)
		self.display_table_layout.addWidget(self.no_shared_image_block)

		# add to main window
		self.window_layout.addWidget(self.display_scroll)

	def control_UI(self):
		# control UI includes content in the bottom ("add" button, question input box, "clear" button)

		h =  self.h - self.display_h - 20

		# set control
		self.control_widget = QWidget()
		self.control_widget.setFixedSize(self.w, h + 20)
		self.control_layout = QHBoxLayout()
		self.control_layout.setContentsMargins(10, 10, 10, 10)
		self.control_layout.setSpacing(10)

		# button : add a folder
		self.button_add = QLabel()
		self.button_add.mousePressEvent = lambda event : self.on_set_name_window_open()
		self.button_add.setFixedSize(h // 2 , h // 2)
		self.button_add.setPixmap(QPixmap("data/images/add.png"))
		self.button_add.setScaledContents(True)

		# button : clear all folders
		self.button_clear_all = QLabel()
		self.button_clear_all.mousePressEvent = lambda event : self.on_clear_all()
		self.button_clear_all.setFixedSize(h // 2 , h // 2)
		self.button_clear_all.setPixmap(QPixmap("data/images/new.png"))
		self.button_clear_all.setScaledContents(True)

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
		self.control_layout.addWidget(self.button_add)
		self.control_layout.addWidget(self.text_input)
		self.control_layout.addWidget(self.button_clear_all)

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

	def unable_text_input(self):
		self.text_input.setReadOnly(True)
		# self.text_input.setTextInteractionFlags(Qt.NoTextInteraction)
		self.text_input.viewport().setCursor(Qt.ArrowCursor)
		self.text_input.setStyleSheet(f"{self.text_input_style_sheet}background:#f7f7f8")

		# unable new_folder
		self.clear_folders_enabled = False

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

		# enable new_folder
		self.clear_folders_enabled = True

		# loading...
		self.timer.stop()
		self.text_input.setText("")

	def add_new_folder(self, name, path):
		num = len(self.shared_folders)
		self.shared_folders[num] = {
			"name" : name,
			"path" : path
		}
		self.set_data()

	def clear_all_folders(self):
		self.shared_folders = {}
		self.set_data()

	'''
	event
	'''
	
	def on_set_name_window_open(self):
		# create set_name_window, and get set_name information to fill in the textform
		set_name_window = SetNameWindow(self)

		# position
		x = self.parent.pos().x() - (set_name_window.w - self.w) / 2
		y = self.parent.pos().y() - (set_name_window.h - self.h) / 2
		set_name_window.set_pos(x, y)

		# set contents
		set_name_window.settings_block_layout.addStretch(2)

		## for name item
		set_name_window.name_item = set_name_window.item_UI("name", "")
		set_name_window.settings_block_layout.addWidget(set_name_window.name_item)
		set_name_window.settings_block_layout.addStretch(1)
  
		set_name_window.settings_block_layout.addStretch(1)
		set_name_window.settings_block_layout.addWidget(set_name_window.set_button_block)
		set_name_window.settings_block_layout.addStretch(2)

		# show
		set_name_window.show()

		# set the close signal event
		set_name_window.set_name_signal.connect(self.on_set_name_window_save)

	def on_set_name_window_save(self, set_name_window):
		name = set_name_window.name_item.findChild(QTextEdit, "text_input").toPlainText()
		path = self.text_input.toPlainText()

		# clear input
		self.text_input.setText("")
		self.unable_text_input()
		set_name_window.on_window_close()

		# run it after succeed to submit to the server
		def on_add():
			# set the data
			self.add_new_folder(name, path)

			# add folder display
			idx = len(self.shared_folders) - 1
			self.add_display_item(f"[{idx}] {name} :", "#f7f7f8")
			self.add_display_item(f"{path}", "#ffffff")

			# if there is no previous folder, start a new folder
			if self.is_folder_empty:
				self.no_shared_image_block.close()
				self.is_folder_empty = False

			self.enable_text_input()
		
		# TODO : API
		on_add()
		# google_translate_api = GoogleTranslation_API(url=self.url, text=text.strip().strip("\n"))
		# google_translate_api.get_translated_signal.connect(on_add)
		# google_translate_api.start()

	def on_clear_all(self):
		# clear input
		self.unable_text_input()

		# run it after succeed to submit to the server
		def on_clear():
			# set the data
			self.clear_all_folders()
			self.enable_text_input()

			# create a new translation
			if self.clear_folders_enabled:
				# delete all previous translations
				for display_item in self.display_items:
					display_item.deleteLater()
				self.display_items = []

				# show the no_translation display
				if not self.is_folder_empty:
					self.no_shared_image_block.show()
					self.is_folder_empty = True
		

		# TODO : API
		on_clear()
		# google_translate_api = GoogleTranslation_API(url=self.url, text=text.strip().strip("\n"))
		# google_translate_api.get_translated_signal.connect(on_add)
		# google_translate_api.start()

	def enter_press_event(self, event):
		enter_key = [Qt.Key_Enter, Qt.Key_Return]
		if event.modifiers() == Qt.ControlModifier and event.key() in enter_key:
			self.text_input.textCursor().insertText('\n')
		elif event.key() in enter_key:
			self.on_set_name_window_open()
		else:
			self.text_input.keyPressEventRaw(event)


plugin = {
	"title" : "transfer-S",
	"window" : FileTransferServerWindow,
}

__all__ = [plugin]