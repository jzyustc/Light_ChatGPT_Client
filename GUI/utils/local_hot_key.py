from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class LocalHotkey:
    def __init__(self, window:QWidget):
        self.window = window
        self.main_window = window.parent

        self.window.keyPressEvent = self.hot_key_event
        self.hot_key_list = [{
            'modifier': Qt.ControlModifier,
            'key': Qt.Key_Q,
            'func': self.main_window.close_app_signal.emit
        }]

    def hot_key_event(self, event):
        for hot_key in self.hot_key_list:
            if event.modifiers() == hot_key['modifier'] and event.key() == hot_key['key']:
                args = hot_key['args'] if 'args' in hot_key.keys() else ()
                kwargs = hot_key['kwargs'] if 'kwargs' in hot_key.keys() else {}
                hot_key['func'](*args, **kwargs)

    def add_hot_key(self, modifier, key, func, *args, **kwargs):

        hot_key = {
                'modifier': modifier,
                'key': key,
                'func': func,
            }
        if len(args) != 0:
            hot_key['args'] = args
        if len(kwargs) != 0:
            hot_key['kwargs'] = kwargs

        self.hot_key_list.append(hot_key)
