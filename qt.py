import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.main_window import MainWindow
from GUI.floating_window import FloatingWindow

if __name__ == '__main__':
    my_app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    floating_window = FloatingWindow("data/images/floating_window_icon.png")

    def switch_main():
        x = floating_window.pos().x() - main_window.w
        y = floating_window.pos().y() - (main_window.h - floating_window.h) / 2
        main_window.set_pos(x, y)
        main_window.show()
        floating_window.hide()

    def switch_floating():
        x = main_window.pos().x() + main_window.w
        y = main_window.pos().y() + (main_window.h - floating_window.h) / 2
        floating_window.set_pos(x, y)
        floating_window.show()
        main_window.hide()

    main_window.switch_floating_window_signal.connect(switch_floating)
    floating_window.switch_main_window_signal.connect(switch_main)

    # init pos
    device = QtWidgets.QApplication.desktop()
    device_h = device.height()
    device_w = device.width()

    init_x = device_w - floating_window.w
    init_y = device_h // 4
    floating_window.set_pos(init_x, init_y)

    floating_window.show()
    switch_main()
    sys.exit(my_app.exec_())