import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.window.main_window import MainWindow
from GUI.window.floating_window import FloatingWindow
from GUI.utils.global_hot_key import GlobalHotkeys

from system_hotkey import SystemHotkey

class LightChatGPTClient:

    
    def __init__(self):

        self.app = QtWidgets.QApplication(sys.argv)

        # a flag to show whether it is main windw now
        self.main_flag = False

        self.user_info_path = "data/info.json"
        self.init_user(info_path=self.user_info_path)

        self.main_window = MainWindow(self.url, self.uid, self.hash_password)
        self.floating_window = FloatingWindow("data/images/floating_window_icon.png")

        self.init_pos()
        self.init_hot_keys()
        self.init_signals()

    '''
    initialize
    '''
    def init_user(self, info_path):
        self.info = json.load(open(info_path))
        self.url = self.info["url"]
        self.uid = self.info["uid"]
        self.hash_password = self.info["hash_password"]

    def init_pos(self):
        # init pos
        device = QtWidgets.QApplication.desktop()
        device_h = device.height()
        device_w = device.width()

        init_x = device_w - self.floating_window.w
        init_y = device_h // 4
        self.floating_window.set_pos(init_x, init_y)

    def init_signals(self):
        # switch between main window and floating window
        self.main_window.switch_floating_window_signal.connect(self.switch_floating)
        self.floating_window.switch_main_window_signal.connect(self.switch_main)

        # global hot key signal
        self.global_hot_keys.hot_key_signal.connect(self.switch_window)

        # close the app 
        self.floating_window.close_app_signal.connect(self.close)

        # user information
        self.floating_window.get_user_signal.connect(self.get_user_info_into_user_window)
        self.floating_window.set_user_signal.connect(self.set_user_info)

    def init_hot_keys(self):
        self.hot_keys = SystemHotkey()
        self.register_hot_keys()
        self.global_hot_keys = GlobalHotkeys()

    def register_hot_keys(self):
        self.hot_keys.register(('control', 't'), callback=lambda x:self.global_hot_keys.send_key('ctrl+t'))

    def unregister_hot_keys(self):
        self.hot_keys.unregister(('control', 't'))

    '''
    signals
    '''
    def switch_main(self):
        x = self.floating_window.pos().x() - self.main_window.w
        y = self.floating_window.pos().y() - (self.main_window.h - self.floating_window.h) / 2
        self.main_window.set_pos(x, y)
        self.main_window.show()
        self.floating_window.hide()

    def switch_floating(self):
        x = self.main_window.pos().x() + self.main_window.w
        y = self.main_window.pos().y() + (self.main_window.h - self.floating_window.h) / 2
        self.floating_window.set_pos(x, y)
        self.floating_window.show()
        self.main_window.hide()

    def switch_window(self, hot_key):
        if self.main_flag:
            if hot_key == 'ctrl+t':
                self.switch_floating()
                self.main_flag = False
        else:
            if hot_key == 'ctrl+t':
                self.switch_main()
                self.main_flag = True

    def get_user_info_into_user_window(self, user_window):
        user_window.uid_text_input.setText(self.uid)
        # user_window.password_text_input.setText(self.password)

    def set_user_info(self, uid, hash_password):
        self.uid = self.main_window.uid = uid
        self.hash_password = self.main_window.hash_password = hash_password
        
        # write into info.json
        with open(self.user_info_path, "w") as f:
            user_info = {
                "url": self.url, 
                "uid": uid, 
                "hash_password": hash_password
            }
            json.dump(user_info,f)

    def hot_key_func(self, hot_key_value):
        # switch to main window
        if hot_key_value == 'ctrl+t':
            self.switch_window()
        else:
            pass

    '''
    run and close
    '''
    def run(self):
        self.floating_window.show()
        # self.switch_main()
        sys.exit(self.app.exec_())

    def close(self):
        self.main_window.close()
        self.floating_window.close()
        sys.exit(self.app.exec_())