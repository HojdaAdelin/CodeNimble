from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QTextCursor, QFont
from PySide6.QtCore import Qt

class MiniMap(QWidget):
    def __init__(self, editor,theme, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setFixedWidth(100)  

        self.font = QFont("Consolas", 3)
        self.font.setPointSize(3) 
        self.line_spacing = 4  
        self.theme = theme['minimap']

    def setTheme(self, theme):
        for key in ["background", "text", "highlight"]:
            if key in theme:
                self.theme[key] = theme[key]
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.8)  
        painter.fillRect(self.rect(), QColor(self.theme["background"]))  

        painter.setFont(self.font)

        font_metrics = painter.fontMetrics()
        char_width = font_metrics.horizontalAdvance("a")  
        num_chars_fit = self.width() // char_width  

        block = self.editor.document().begin()
        y_offset = 0
        while block.isValid():
            text = block.text()
            truncated_text = text[:num_chars_fit]  
            painter.setOpacity(0.8)  
            painter.setPen(QColor(self.theme["text"])) 
            painter.drawText(2, y_offset + self.line_spacing, truncated_text)
            y_offset += self.line_spacing
            block = block.next()

        visible_rect = self.editor.viewport().rect()
        cursor = self.editor.cursorForPosition(visible_rect.topLeft())
        start_block = cursor.block().blockNumber()

        visible_lines = visible_rect.height() // self.editor.fontMetrics().height()

        highlighter_color = QColor(self.theme["highlight"])
        highlighter_color.setAlpha(80)
        painter.setBrush(highlighter_color)  
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, start_block * self.line_spacing, self.width(),
                         visible_lines * self.line_spacing)

    def mousePressEvent(self, event):
        y = event.pos().y()
        block_index = y // self.line_spacing  
        document = self.editor.document()
        block = document.findBlockByNumber(block_index)

        if block.isValid():
            cursor = QTextCursor(block)
            self.editor.setTextCursor(cursor)
            self.editor.centerCursor()
