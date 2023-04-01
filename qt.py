import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.client import LightChatGPTClient

if __name__ == '__main__':
    client = LightChatGPTClient()
    client.run()
    