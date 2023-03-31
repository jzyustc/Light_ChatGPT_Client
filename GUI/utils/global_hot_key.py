import sys
import time
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from system_hotkey import SystemHotkey

from GUI.api.chatgpt_server_api import ChatGPT_API

class GlobalHotkeys(QWidget):
	hot_key_signal = pyqtSignal(str)		    	# signal to process hot key

	def __init__(self):
		super().__init__()

	def send_key(self, hot_key):
		self.hot_key_signal.emit(hot_key)