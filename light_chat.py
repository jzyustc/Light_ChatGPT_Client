import sys
from multiprocessing import Process
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.client import LightChatGPTClient

import GUI.api
import GUI.api.chatgpt_server_api
import GUI.api.google_translation_api

import GUI.plugins
import GUI.plugins.chatgpt
import GUI.plugins.google_translate

import GUI.utils
import GUI.utils.global_hot_key
import GUI.utils.language
import GUI.utils.local_hot_key
import GUI.utils.position

import GUI.window
import GUI.window.floating_window
import GUI.window.main_window
import GUI.window.plugins_menu_window
import GUI.window.user_window

def run_GUI():
    client = LightChatGPTClient()
    client.run()


from HTTPServer.http_server_api import create_http_server

def run_HTTPServer(ip, port, share_data_path):
    create_http_server(ip, port, share_data_path)

if __name__ == '__main__':
    
    p1 = Process(target=run_GUI)
    p1.start()

    p2 = Process(target=run_HTTPServer, args=("0.0.0.0", 8000, "data/file_transfer_server_data.json"))
    p2.start()

    process_list = [p1, p2]
    for p in process_list:
        p.join()
