from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QTabWidget, QTabBar, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QEvent, Signal, QObject
from PySide6.QtGui import QFontMetrics, QFont, QMouseEvent, QIcon, QShortcut, QKeySequence
import os

class TabBar(QWidget):
    def __init__(self, theme, text_widget, file_manager):
        super().__init__()
        
        self.theme = theme
        self.text_widget = text_widget
        self.file_manager = file_manager

        self.tabs = {}  
        self.contents = {} 
        self.modified_tabs = set()  

        self.current_file_path = None

        self.init_ui()
        self.setup_shortcuts()
        self.connect_text_widget_signals()
    
    def init_ui(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(False)  # Dezactivăm mutarea taburilor
        self.tab_widget.setElideMode(Qt.ElideNone)
        self.tab_widget.tabBar().setExpanding(False)
        self.tab_widget.tabBar().setDocumentMode(True)

        self.layout.addWidget(self.tab_widget)

        self.apply_stylesheet()

        # Conectarea semnalelor
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.switch_tab)
        self.tab_widget.tabBar().tabBarDoubleClicked.connect(self.on_tab_double_click)
        self.tab_widget.tabBar().installEventFilter(self)
    
    def apply_stylesheet(self):
        # Stilizare personalizată pentru tab-uri
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 0;
            }}
            QTabBar::tab {{
                background: {self.theme['background_color']};
                color: {self.theme['text_color']};
                padding: 5px 10px;
                margin: 2px;
                border-radius: 4px;
                min-width: 100px;
                max-width: 200px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme['button_color']};
                color: {self.theme['text_color']};
            }}
            QTabBar::tab:!selected {{
                background: {self.theme['background_color']};
                color: {self.theme['text_color']};
            }}
            QTabBar::close-button {{
                image: url('images/close.png'); 
            }}
            QTabBar::close-button:hover {{
                image: url('images/close.png');
            }}
        """)
    
    def setup_shortcuts(self):
        # Scurtături pentru navigarea între tab-uri
        next_tab_shortcut = QShortcut(QKeySequence("Ctrl+Tab"), self)
        next_tab_shortcut.activated.connect(self.next_tab)

        previous_tab_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Tab"), self)
        previous_tab_shortcut.activated.connect(self.previous_tab)
    
    def connect_text_widget_signals(self):
        # Detectarea modificărilor în text_widget
        self.text_widget.textChanged.connect(self.on_text_changed)
    
    def add_tab(self, file_path=None):
        if file_path and file_path in self.tabs.values():
            index = list(self.tabs.keys())[list(self.tabs.values()).index(file_path)]
            self.tab_widget.setCurrentIndex(index)
            return 

        if file_path:
            file_name = os.path.basename(file_path)
            content = self.file_manager.get_file_content(file_path)
        else:
            file_name = "Untitled"
            content = ""

        new_tab = QWidget()
        index = self.tab_widget.addTab(new_tab, file_name)
        self.tabs[index] = file_path
        self.contents[file_path] = content
        self.tab_widget.setCurrentIndex(index)
        self.update_tab_title(index)
        self.text_widget.setPlainText(content)
        self.current_file_path = file_path
        self.file_manager.change_opened_filename(file_path)
        self.text_widget.document().setModified(False)
        self.setFixedHeight(30)
    
    def close_tab(self, index):
        if index < 0 or index >= self.tab_widget.count():
            return

        # Obține calea fișierului pentru tab-ul care se închide
        file_path = self.tabs.get(index)
        if file_path is None:
            return

        # Obține conținutul original și cel asociat tab-ului care se închide
        original_content = self.file_manager.get_file_content(file_path) if file_path else ""
        if index == self.tab_widget.currentIndex():
            tab_content = self.text_widget.toPlainText()
        else:
            tab_content = self.contents.get(file_path, "")
        # Verifică dacă există modificări nesalvate
        is_modified = original_content != tab_content

        if is_modified:
            # Asigură-te că tab-ul pe care vrei să-l închizi este activ
            current_index = self.tab_widget.currentIndex()
            self.tab_widget.setCurrentIndex(index)

            reply = QMessageBox.question(
                self, "Unsaved Changes",
                f"The file '{os.path.basename(file_path) if file_path else 'Untitled'}' has unsaved changes. Do you want to save them?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                if file_path:
                    self.file_manager.save_file(self.text_widget)
                else:
                    saved_path = self.file_manager.save_file_as(self.text_widget)
                    if saved_path:
                        self.tabs[index] = saved_path
                        self.contents[saved_path] = tab_content
                        del self.contents[file_path]
                        file_path = saved_path
                    else:
                        # Dacă utilizatorul a anulat salvarea, revenim la tab-ul original
                        self.tab_widget.setCurrentIndex(current_index)
                        return
            elif reply == QMessageBox.Cancel:
                # Dacă utilizatorul a anulat, revenim la tab-ul original
                self.tab_widget.setCurrentIndex(current_index)
                return

        # Eliminăm tab-ul
        self.tab_widget.removeTab(index)
        del self.tabs[index]
        if file_path in self.contents:
            del self.contents[file_path]

        # Actualizăm indexurile pentru tab-urile rămase
        self.update_tab_indices()

        # Verificăm dacă mai sunt tab-uri deschise
        if self.tab_widget.count() > 0:
            new_index = min(index, self.tab_widget.count() - 1)
            self.tab_widget.setCurrentIndex(new_index)
            new_file_path = self.tabs.get(new_index)
            if new_file_path and new_file_path in self.contents:
                self.current_file_path = new_file_path
                self.text_widget.setPlainText(self.contents[new_file_path])
                self.file_manager.change_opened_filename(new_file_path)
            else:
                self.text_widget.clear()
                self.current_file_path = None
                self.file_manager.change_opened_filename(None)
        else:
            self.text_widget.clear()
            self.current_file_path = None
            self.file_manager.change_opened_filename(None)
            self.setFixedHeight(0)

    
    def switch_tab(self, index):
        if index == -1:
            return

        # Salvează conținutul tab-ului curent
        if self.current_file_path is not None:
            current_content = self.text_widget.toPlainText()
            self.contents[self.current_file_path] = current_content

        # Comută la noul tab
        new_file_path = self.tabs.get(index)

        if new_file_path is None or new_file_path not in self.contents:
            return  # Iese din funcție dacă nu găsește un fișier valid

        self.current_file_path = new_file_path
        self.text_widget.setPlainText(self.contents[new_file_path])
        self.file_manager.change_opened_filename(new_file_path)

    
    def on_text_changed(self):
        if self.current_file_path is None:
            return

        # Marchează tab-ul ca modificat
        current_index = self.tab_widget.currentIndex()
        self.update_tab_title(current_index, modified=True)
    
    def update_tab_title(self, index, title=None, modified=False):
        if title is None:
            file_path = self.tabs.get(index)
            title = os.path.basename(file_path) if file_path else "Untitled"

        # Eliminăm asteriscul complet
        self.tab_widget.setTabText(index, title)
    
    def next_tab(self):
        current_index = self.tab_widget.currentIndex()
        total_tabs = self.tab_widget.count()
        next_index = (current_index + 1) % total_tabs
        self.tab_widget.setCurrentIndex(next_index)
    
    def previous_tab(self):
        current_index = self.tab_widget.currentIndex()
        total_tabs = self.tab_widget.count()
        previous_index = (current_index - 1) % total_tabs
        self.tab_widget.setCurrentIndex(previous_index)
    
    def on_tab_double_click(self, index):
        # Poți implementa funcționalitatea dorită la dublu click (de exemplu, redenumire)
        pass
    
    def eventFilter(self, obj, event):
        if obj == self.tab_widget.tabBar():
            if isinstance(event, QMouseEvent):
                if event.button() == Qt.MiddleButton:
                    # Închide tab-ul la click pe butonul din mijloc
                    tab_index = obj.tabAt(event.pos())
                    if tab_index != -1:
                        self.close_tab(tab_index)
                        return True
        return super().eventFilter(obj, event)
    
    def check_tab(self, file_path):
        return file_path in self.tabs.values()
    
    def save_current_tab(self):
        if self.current_file_path:
            content = self.text_widget.toPlainText()
            self.file_manager.save_file(self.text_widget)
            self.modified_tabs.discard(self.current_file_path)
            self.update_tab_title(self.tab_widget.currentIndex(), modified=False)
    
    def save_current_tab_as(self):
        if self.current_file_path:
            content = self.text_widget.toPlainText()
            saved_path = self.file_manager.save_file_as(self.text_widget)
            if saved_path:
                current_index = self.tab_widget.currentIndex()
                self.tabs[current_index] = saved_path
                self.contents[saved_path] = content
                del self.contents[self.current_file_path]
                self.current_file_path = saved_path
                self.file_manager.change_opened_filename(saved_path)
                self.modified_tabs.discard(saved_path)
                self.update_tab_title(current_index, os.path.basename(saved_path), modified=False)
    
    def get_open_files(self):
        return list(self.tabs.values())

    def update_tab_indices(self):
        new_tabs = {}
        for i in range(self.tab_widget.count()):
            old_index = list(self.tabs.keys())[i]
            new_tabs[i] = self.tabs[old_index]
        self.tabs = new_tabs