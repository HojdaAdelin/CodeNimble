from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap, QMouseEvent, QFont, QEnterEvent
from PySide6.QtCore import Qt, QTimer
from Tools import scrap
from datetime import datetime, timedelta
from datetime import datetime

class StatusBar(QFrame):
    def __init__(self, text_widget, theme, main):
        super().__init__()
        self.theme = theme
        self.main = main
        self.text_widget = text_widget
        self.current_version = "2.0"
        self.latest_version = scrap.get_latest_version_from_github("HojdaAdelin", "CodeNimble")
        self.text = ""
        self.hv_color = theme.get("status_bar_hover")
        self.based_color = theme.get("status_bar_background")
        self.ctn_words_color = theme.get("ctn_words")
        self.num_lines = 0
        self.num_words = 0
        self.start_time = None
        self.running = False
        self.timer_paused = False
        self.elapsed_time = timedelta(0)
        self.msg_log = []
        self.msg_colors = []
        self.setStyleSheet(f"background-color: {self.based_color};")
        self.setup_ui()
        self.apply_theme(theme)
        self.server_icon.mousePressEvent = self.on_inbox_icon_click

    def setup_ui(self):
        font_size = 12
        self.font = QFont("Arial", font_size)

        self.separator1 = QFrame(self)
        self.separator1.setFrameShape(QFrame.VLine)
        self.separator2 = QFrame(self)
        self.separator2.setFrameShape(QFrame.VLine)
        self.separator3 = QFrame(self)
        self.separator3.setFrameShape(QFrame.VLine)
        
        self.new_version_label = QLabel("New version available", self)
        self.new_version_label.setFont(self.font)
        self.new_version_label.setStyleSheet("background-color: green; color: black;")

        self.num_stats_label = QLabel("Lines: 0, Words: 0 ", self)
        self.num_stats_label.setFont(self.font)
        self.num_stats_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.num_stats_label.setStyleSheet(f"color: {self.theme['text_color']};")

        self.status_label = QLabel(self.text, self)
        self.status_label.setFont(self.font)
        self.status_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.status_label.setStyleSheet(f"color: {self.theme['text_color']};")

        # Setup server status label
        self.server_status = QLabel("Server: none", self)
        self.server_status.setFont(self.font)
        self.server_status.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.server_status.setStyleSheet(f"color: {self.theme['text_color']};")

        # Create server icon label and set the default icon (bell-default.png)
        self.server_icon = QLabel(self)
        default_icon_path = "images/bell-default.png"  # Path to bell-default image
        pixmap = QPixmap(default_icon_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.server_icon.setPixmap(pixmap)
        self.server_icon.setStyleSheet(f"background-color: {self.based_color};")

        image_path = "images/run.png"  # Actualizează calea dacă este necesar
        pixmap = QPixmap(image_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.run_img = QLabel(self)
        self.run_img.setPixmap(pixmap)
        self.run_img.setStyleSheet(f"background-color: {self.based_color};")
        self.run_img.setCursor(Qt.PointingHandCursor)

        # Timer setup (move to the left)
        self.timer = QLabel("00:00:00", self)
        self.timer.setFont(self.font)
        self.timer.setStyleSheet(f"color: {self.theme['text_color']};")
        self.timer.setCursor(Qt.PointingHandCursor)

        # Layout setup
        layout = QHBoxLayout(self)
        layout.addWidget(self.new_version_label)
        layout.addWidget(self.timer)
        layout.addStretch() 
        layout.addWidget(self.server_icon)
        layout.addWidget(self.separator3)
        layout.addWidget(self.server_status)
        layout.addWidget(self.separator2)
        layout.addWidget(self.run_img)
        layout.addWidget(self.separator1)
        layout.addWidget(self.num_stats_label)
        layout.addWidget(self.status_label)
        layout.setContentsMargins(5, 2, 5, 2)  # Adaugă margini pentru a evita lipirea elementelor de marginea barei
        self.setLayout(layout)

        # Connections
        self.run_img.mousePressEvent = self.on_run_click  # Handle click event for run image
        self.run_img.enterEvent = self.on_run_hover_enter  # Handle hover enter for run image
        self.run_img.leaveEvent = self.on_run_hover_leave  # Handle hover leave for run image
        
        self.timer.mousePressEvent = self.on_timer_click  # Handle click event for timer
        self.timer.enterEvent = self.on_timer_hover_enter  # Handle hover enter for timer
        self.timer.leaveEvent = self.on_timer_hover_leave  # Handle hover leave for timer

        # Version check
        if self.latest_version > self.current_version and isinstance(self.latest_version, int):
            self.new_version_label.setVisible(True)
        else:
            self.new_version_label.setVisible(False)

    def apply_theme(self, theme):
        self.setStyleSheet(f"background-color: {theme['status_bar_background']};")
        self.separator1.setStyleSheet(f"color: {theme['text_color']}; width: 2px;")
        self.separator2.setStyleSheet(f"color: {theme['text_color']}; width: 2px;")
        self.separator3.setStyleSheet(f"color: {theme['text_color']}; width: 2px;")
        self.status_label.setStyleSheet(f"color: {theme['text_color']};")
        self.num_stats_label.setStyleSheet(f"color: {theme['text_color']};")
        self.server_status.setStyleSheet(f"color: {theme['text_color']};")
        self.hv_color = theme.get("button_hover_color", "#4d4d4d")
        self.based_color = theme["status_bar_background"]
        self.run_img.setStyleSheet(f"background-color: {self.based_color};")
        self.timer.setStyleSheet(f"background-color: {self.based_color};")
        self.server_icon.setStyleSheet(f"background-color: {self.based_color};")

    def on_inbox_icon_click(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:  # Verifică dacă s-a dat click stânga
            default_icon_path = "images/bell-default.png"
            new_pixmap = QPixmap(default_icon_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.server_icon.setPixmap(new_pixmap)
            self.show_inbox_popup()

    def time_sec_h(self):
        acum = datetime.now()
        ora = acum.hour
        minut = acum.minute
        secunda = acum.second
        return ora, minut, secunda

    def show_inbox_popup(self):
        # Creează un QWidget care va afișa lista de mesaje
        if hasattr(self, 'inbox_popup') and self.inbox_popup.isVisible():
            return
        self.inbox_popup = QWidget(self.main)
        self.inbox_popup.setStyleSheet(
            "background-color: rgba(0, 0, 0, 80); color: white; border-radius: 5px; padding: 5px;"
        )

        # Creează un layout vertical pentru a afișa toate mesajele
        layout = QVBoxLayout(self.inbox_popup)

        # Adaugă fiecare mesaj din msg_log într-un QLabel
        for i, message in enumerate(reversed(self.msg_log)):  # Afișează mesajele în ordinea inversă
            msg_label = QLabel(message)
            msg_label.setFont(self.font)
            msg_label.setStyleSheet(f"color: {self.msg_colors[-(i+1)]};")  # Aplica culoarea corespunzătoare
            layout.addWidget(msg_label)

        # Ajustează dimensiunea popup-ului în funcție de conținut
        self.inbox_popup.adjustSize()

        # Calculează coordonatele pentru a-l poziționa deasupra iconiței
        global_pos = self.server_icon.mapToGlobal(self.server_icon.rect().center())
        main_pos = self.main.mapFromGlobal(global_pos)
        popup_x = main_pos.x() - self.inbox_popup.width() // 2
        popup_y = main_pos.y() - self.inbox_popup.height() - 10

        self.inbox_popup.move(popup_x, popup_y)

        # Afișează și ridică popup-ul deasupra altor elemente
        self.inbox_popup.raise_()
        self.inbox_popup.show()

        # Focus pe popup, îl ascunde când utilizatorul dă click pe altceva
        self.inbox_popup.setFocus()
        self.inbox_popup.focusOutEvent = self.hide_inbox_popup

    def hide_inbox_popup(self, event):
        # Ascunde popup-ul când acesta pierde focusul
        self.inbox_popup.hide()

    def toggle_inbox_icon(self, text, color="#FFFFFF"):
        update_icon_path = "images/bell-update.png"
        new_pixmap = QPixmap(update_icon_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.server_icon.setPixmap(new_pixmap)
        self.popup_inbox(text, color)

    def popup_inbox(self, text, color):
        hour,minute, sec = self.time_sec_h()
        msg = f"[{hour}:{minute:02}:{sec:02}] {text}"
        # Creează un QLabel care va funcționa ca popup pe fereastra principală (self.main)
        self.popup_label = QLabel(msg, self.main)  
        self.popup_label.setFont(self.font)
        self.popup_label.setStyleSheet(
            f"background-color: rgba(0, 0, 0, 80); color: {color}; border-radius: 5px; padding: 5px;"
        )

        # Ajustează dimensiunea în funcție de text
        self.popup_label.adjustSize()

        # Calculează coordonatele pentru a-l poziționa deasupra iconiței, raportat la fereastra principală
        global_pos = self.server_icon.mapToGlobal(self.server_icon.rect().center())
        main_pos = self.main.mapFromGlobal(global_pos)
        popup_x = main_pos.x() - self.popup_label.width() // 2
        popup_y = main_pos.y() - self.popup_label.height() - 10  # 5 pixeli deasupra iconiței

        self.popup_label.move(popup_x, popup_y)

        # Afișează și ridică popup-ul deasupra altor elemente
        self.popup_label.raise_()
        self.popup_label.show()
        self.msg_log.append(msg)
        self.msg_colors.append(color)

        # Folosește un timer pentru a ascunde popup-ul după 3 secunde
        QTimer.singleShot(2000, self.popup_label.hide)

    def start_timer(self, event):
        if not self.running:
            self.start_time = datetime.now() - self.elapsed_time
            self.running = True
            self.update_timer()
        else:
            self.timer_paused = not self.timer_paused
            if self.timer_paused:
                self.elapsed_time = datetime.now() - self.start_time
            else:
                self.start_time = datetime.now() - self.elapsed_time
                self.update_timer()

    def update_timer(self):
        if self.running and not self.timer_paused:
            elapsed_time = datetime.now() - self.start_time
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.timer.setText(time_str)
            QTimer.singleShot(1000, self.update_timer)

    def on_run_hover_enter(self, event: QEnterEvent):
        self.run_img.setStyleSheet(f"background-color: {self.hv_color};")

    def on_run_hover_leave(self, event: QMouseEvent):
        self.run_img.setStyleSheet(f"background-color: {self.based_color};")

    def on_timer_hover_enter(self, event: QEnterEvent):
        self.timer.setStyleSheet(f"background-color: {self.hv_color};")

    def on_timer_hover_leave(self, event: QMouseEvent):
        self.timer.setStyleSheet(f"background-color: {self.based_color};")

    def on_run_click(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.main.run_core()

    def on_timer_click(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.start_timer(event)
        elif event.button() == Qt.MiddleButton:  
            self.reset_timer()

    def reset_timer(self):
        self.elapsed_time = timedelta(0)
        self.running = False
        self.timer_paused = False
        self.timer.setText("00:00:00")

    def update_text(self, new_text):
        self.status_label.setText(new_text)

    def update_stats(self):
        content = self.text_widget.toPlainText()
        lines = content.count('\n')
        words = len(content.split())
        self.num_lines = lines
        self.num_words = words
        stats_text = f"Lines: {lines+1}, Words: {words}"
        self.num_stats_label.setText(stats_text)

    def update_server(self, status):
        status_text = "Server: " + status
        self.server_status.setText(status_text)
