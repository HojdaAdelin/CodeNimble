from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton,QFrame, QStackedWidget
from PySide6.QtGui import QIcon, QColor, QPainter, QPen, QPixmap
from PySide6.QtCore import Qt
import sys

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QPixmap(1000, 500)
        self.image.fill(Qt.white)
        self.last_pos = None
        self.current_tool = "pencil"
        self.pencil_color = QColor("black")
        self.pen_width = 3
        self.eraser_width = 20
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_pos:
            painter = QPainter(self.image)
            if self.current_tool == "pencil":
                painter.setPen(QPen(self.pencil_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            elif self.current_tool == "eraser":
                painter.setCompositionMode(QPainter.CompositionMode_Source)
                painter.setPen(QPen(Qt.white, self.eraser_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            self.last_pos = event.pos()

    def mouseReleaseEvent(self, event):
        self.last_pos = None

    def set_tool(self, tool):
        self.current_tool = tool

    def set_pen_color(self, color):
        self.pencil_color = color

    def clear_canvas(self):
        self.image.fill(Qt.white)
        self.update()

class PaintApp(QMainWindow):
    def __init__(self, theme,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Paint Mode")
        self.setGeometry(100, 100, 1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowIcon(QIcon("images/logo.ico"))

        self.theme = theme
        self.pencil_color = QColor("black")
        self.current_tool = "pencil"
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        # Tool bar
        self.tool_bar = QFrame(self)
        self.tool_bar.setFixedHeight(50)
        self.setCentralWidget(self.tool_bar)

        tool_bar_layout = QHBoxLayout(self.tool_bar)

        # Buttons
        self.btn_pencil = QPushButton("Pencil", self.tool_bar)
        self.btn_pencil.clicked.connect(self.use_pencil)
        tool_bar_layout.addWidget(self.btn_pencil)

        self.btn_eraser = QPushButton("Eraser", self.tool_bar)
        self.btn_eraser.clicked.connect(self.use_eraser)
        tool_bar_layout.addWidget(self.btn_eraser)

        self.btn_clear = QPushButton("Clear", self.tool_bar)
        self.btn_clear.clicked.connect(self.clear_canvas)
        tool_bar_layout.addWidget(self.btn_clear)

        # Color buttons
        colors = ["black", "red", "yellow", "green", "blue"]
        for color in colors:
            color_btn = QPushButton("", self.tool_bar)
            color_btn.setStyleSheet(f"background-color: {color}; width: 20px; height: 20px;")
            color_btn.clicked.connect(lambda checked, c=color: self.change_pencil_color(c))
            tool_bar_layout.addWidget(color_btn)

        # Tab buttons
        self.tab_buttons = []
        for i in range(5):
            tab_button = QPushButton(f"#{i+1}", self.tool_bar)
            tab_button.setFixedSize(65, 25)
            tab_button.clicked.connect(lambda checked, idx=i: self.switch_tab(idx))
            tool_bar_layout.addWidget(tab_button)
            self.tab_buttons.append(tab_button)

        # Canvas stack (to switch between tabs)
        self.canvas_stack = QStackedWidget(self)
        self.canvas_stack.setGeometry(0, 50, 1000, 550)

        # Create canvases for each tab
        self.canvases = []
        for i in range(5):
            canvas_widget = CanvasWidget()
            self.canvas_stack.addWidget(canvas_widget)
            self.canvases.append(canvas_widget)

        self.switch_tab(0)  # Show the first tab by default

    def apply_theme(self):
        # Apply theme colors to UI elements
        self.setStyleSheet(f"background-color: {self.theme['background_color']}; color: {self.theme['text_color']};")
        self.tool_bar.setStyleSheet(f"background-color: {self.theme['background_color']};")
        for button in [self.btn_pencil, self.btn_eraser, self.btn_clear]:
            button.setStyleSheet(f"""
                background-color: {self.theme['button_color']};
                color: {self.theme['text_color']};
                border: 1px solid {self.theme['border_color']};
            """)
        for button in self.tab_buttons:
            button.setStyleSheet(f"""
                background-color: {self.theme['button_color']};
                color: {self.theme['text_color']};
                border: 1px solid {self.theme['border_color']};
            """)

    def use_pencil(self):
        self.current_tool = "pencil"
        for canvas in self.canvases:
            canvas.set_tool(self.current_tool)
        self.canvases[self.canvas_stack.currentIndex()].setCursor(Qt.ArrowCursor)

    def use_eraser(self):
        self.current_tool = "eraser"
        for canvas in self.canvases:
            canvas.set_tool(self.current_tool)
        self.canvases[self.canvas_stack.currentIndex()].setCursor(Qt.CrossCursor)

    def clear_canvas(self):
        self.canvases[self.canvas_stack.currentIndex()].clear_canvas()

    def change_pencil_color(self, color):
        self.pencil_color = QColor(color)
        for canvas in self.canvases:
            canvas.set_pen_color(self.pencil_color)
        self.use_pencil()

    def switch_tab(self, index):
        self.canvas_stack.setCurrentIndex(index)
        self.update_tab_buttons()

    def update_tab_buttons(self):
        for i, button in enumerate(self.tab_buttons):
            if i == self.canvas_stack.currentIndex():
                button.setStyleSheet(f"background-color: {self.theme['button_hover_color']}; color: {self.theme['text_color']};")
            else:
                button.setStyleSheet(f"background-color: {self.theme['button_color']}; color: {self.theme['text_color']};")
