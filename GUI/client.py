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

        # window
        self.main_window = MainWindow(["chatgpt", "google_translate"], self)
        self.floating_window = FloatingWindow("data/images/icon.png", self)

        # init
        self.init_pos()
        self.init_hot_keys()
        self.init_signals()
        self.init_user(info_path="data/info.json")


    '''
    initialize
    '''
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
        self.global_hot_keys.hot_key_signal.connect(self.hot_key_func)

        # close the app 
        self.floating_window.close_app_signal.connect(self.close)
        self.main_window.close_app_signal.connect(self.close)

        # user information
        self.floating_window.get_user_signal.connect(self.get_user_info_into_user_window)
        self.floating_window.set_user_signal.connect(self.set_user_info)

    def init_hot_keys(self):
        self.hot_keys = SystemHotkey()
        self.register_hot_keys()
        self.global_hot_keys = GlobalHotkeys()

    def register_hot_keys(self):
        self.hot_keys.register(('control', 't'), callback=lambda x:self.global_hot_keys.send_key('ctrl+t'))

    def init_user(self, info_path):
        self.user_info_path = info_path
        self.info = json.load(open(info_path))

        self.url = self.info["url"]
        self.uid = self.info["uid"]
        self.hash_password = self.info["hash_password"]

        self.main_window.chatgpt_window.set_info(self.url, self.uid, self.hash_password)
        self.main_window.init_plugins()
        
    '''
    signals
    '''
    def switch_main(self):
        device_h, device_w, nx, ny = self.floating_window.get_device_shape_and_pos()
        nh, nw = self.floating_window.h, self.floating_window.w

        if nx + nw // 2 < device_w // 2: # in left half screen
            x = nx
        else: # in right half screen
            x = nx + nw - self.main_window.w
        y = ny - (self.main_window.h - nh) / 2

        self.main_window.set_pos(x, y)
        self.main_window.set_window_opacity(self.main_window.op)
        self.main_window.show()
        self.floating_window.hide()

    def switch_floating(self, check_out_of_range):
        device_h, device_w, nx, ny = self.main_window.get_device_shape_and_pos()
        nh, nw = self.main_window.h, self.main_window.w

        if nx + nw // 2 < device_w // 2: # in left half screen
            x = nx
        else: # in right half screen
            x = nx + nw - self.floating_window.w
        y = ny - (self.floating_window.h - nh) / 2

        self.floating_window.set_pos(x, y)

        if check_out_of_range:
            self.floating_window.out_of_screen_set_pos()

        self.floating_window.show()
        self.main_window.hide()

    def switch_window(self):
        if self.main_flag:
            self.switch_floating(False)
            self.main_flag = False
        else:
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