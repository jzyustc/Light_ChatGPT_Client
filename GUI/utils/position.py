from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget

def judge_in_region(widget:QWidget, add_x=0, add_y=0):
    # get cursor position
    cursor_pos = QCursor.pos()
    cursor_x, cursor_y = cursor_pos.x(), cursor_pos.y()

    # get widget region
    widget_pos = widget.pos()
    widget_x, widget_y = widget_pos.x() + add_x, widget_pos.y() + add_y
    widget_h, widget_w = widget.height(), widget.width()

    # judge
    if (widget_x <= cursor_x <= widget_x + widget_w) and (widget_y <= cursor_y <= widget_y + widget_h):
        return True
    else:
        return False