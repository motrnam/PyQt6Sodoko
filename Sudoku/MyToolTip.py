from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QToolTip


class TooltipManager:
    def __init__(self, widget):
        self.widget = widget
        self.tooltip_text = None
        self.tooltip_widget = None
        self.show_tooltip_delay = 500  # Delay in milliseconds before showing the tooltip

    def showTooltip(self):
        if self.tooltip_text is None:
            return

        # Create tooltip widget if not already created
        if self.tooltip_widget is None:
            self.tooltip_widget = QToolTip()
            self.tooltip_widget.setStyleSheet("background-color: #fafafa;")
            self.tooltip_widget.setWindowOpacity(0.9)
            self.tooltip_widget.setWordWrap(True)
            self.tooltip_widget.setFont(self.widget.font())

        # Position tooltip widget over the cursor
        position = self.widget.mapToGlobal(QCursor.pos())
        self.tooltip_widget.move(position + QPoint(5, 5))
        self.tooltip_widget.show()

    def hideTooltip(self):
        if self.tooltip_widget:
            self.tooltip_widget.hide()
