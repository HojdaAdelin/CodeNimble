from PySide6.QtWidgets import QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLineEdit, QMenu, QMessageBox, QFileDialog
from PySide6.QtCore import Qt, QDir, QModelIndex
from PySide6.QtGui import QKeyEvent, QAction
import os
import shutil
import subprocess

class TreeView(QWidget):
    def __init__(self, theme, win):
        super().__init__()
        self.win = win
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Crearea modelului pentru sistemul de fișiere
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # Crearea QTreeView și configurarea acestuia
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        # Ascunderea coloanelor suplimentare și a header-ului
        self.tree.setHeaderHidden(True)  # Ascunde header-ul coloanelor
        self.tree.setColumnHidden(1, True)  # Ascunde coloana Size
        self.tree.setColumnHidden(2, True)  # Ascunde coloana Type
        self.tree.setColumnHidden(3, True)  # Ascunde coloana Date Modified

        # Redimensionarea coloanei pentru numele fișierelor/folderelor
        self.tree.setColumnWidth(0, 250)  # Ajustează lățimea coloanei pentru nume
        
        # Adăugarea TreeView la layout
        self.layout.addWidget(self.tree)

        # Crearea și configurarea QLineEdit pentru editare
        self.edit_line = QLineEdit(self)
        self.edit_line.setVisible(False)
        self.layout.addWidget(self.edit_line)

        # Conectarea semnalelor
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)
        self.edit_line.returnPressed.connect(self.commit_edit)
        self.edit_line.editingFinished.connect(self.cancel_edit)
        self.edit_line.installEventFilter(self)
        self.tree.doubleClicked.connect(self.open_file_in_treeview)

        self.current_index = None
        self.current_action = None
        self.apply_theme(theme)

    def apply_theme(self, theme):
        self.tree.setStyleSheet(f"""
            QTreeView {{
                background-color: {theme['background_color']};
                color: {theme['text_color']};
                selection-background-color: {theme['selection_background_color']};
            }}
            QTreeView::item {{
                background-color: {theme['background_color']};
                color: {theme['text_color']};
            }}
            QTreeView::item:selected {{
                background-color: {theme['highlight_color']};
                color: {theme['item_hover_text_color']};
            }}
        """)

    def open_context_menu(self, position):
        index = self.tree.indexAt(position)
        if not index.isValid():
            return

        # Creăm meniul contextual
        menu = QMenu(self)

        # Adăugăm opțiunea de "Add File" și "Add Folder"
        if self.model.isDir(index):
            add_file_action = QAction("Add File", self)
            add_file_action.triggered.connect(lambda: self.start_edit(index, "add_file"))
            menu.addAction(add_file_action)

            add_folder_action = QAction("Add Folder", self)
            add_folder_action.triggered.connect(lambda: self.start_edit(index, "add_folder"))
            menu.addAction(add_folder_action)

        # Adăugăm opțiunea de "Rename"
        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(lambda: self.start_edit(index, "rename"))
        menu.addAction(rename_action)

        # Adăugăm opțiunea de "Delete"
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.delete_item(index))
        menu.addAction(delete_action)

        # Adăugăm opțiunea de "Reveal in Explorer"
        reveal_action = QAction("Reveal in Explorer", self)
        reveal_action.triggered.connect(lambda: self.reveal_in_explorer(index))
        menu.addAction(reveal_action)

        menu.exec(self.tree.viewport().mapToGlobal(position))

    def start_edit(self, index: QModelIndex, action_type: str):
        if not index.isValid():
            return

        # Setăm indexul curent și tipul de acțiune
        self.current_index = index
        self.current_action = action_type
        placeholder_text = {
            "rename": self.model.fileName(index),
            "add_file": "New File.txt",
            "add_folder": "New Folder"
        }.get(action_type, "")

        self.edit_line.setText(placeholder_text)
        self.edit_line.setVisible(True)
        self.edit_line.setGeometry(self.tree.visualRect(index))
        self.edit_line.setFocus()
        self.edit_line.selectAll()

    def commit_edit(self):
        if not self.current_index or not self.current_action:
            return

        new_name = self.edit_line.text().strip()
        parent_path = self.model.filePath(self.current_index)
        if self.current_action == "rename":
            old_name = parent_path
            new_path = os.path.join(os.path.dirname(old_name), new_name)
            try:
                os.rename(old_name, new_path)
                self.model.setRootPath(QDir.rootPath())  # Reîncarcă modelul pentru a reflecta modificările
                self.current_index = None
                self.current_action = None
                self.edit_line.setVisible(False)
            except Exception as e:
                QMessageBox.warning(self, "Rename Error", f"Could not rename {old_name}: {e}")
                self.edit_line.setText(os.path.basename(old_name))

        elif self.current_action == "add_file":
            file_path = os.path.join(parent_path, new_name)
            try:
                with open(file_path, 'w') as f:
                    pass  # Crează fișierul gol
                self.model.setRootPath(QDir.rootPath())  # Reîncarcă modelul pentru a reflecta modificările
                self.current_index = None
                self.current_action = None
                self.edit_line.setVisible(False)
            except Exception as e:
                QMessageBox.warning(self, "Add File Error", f"Could not create file {file_path}: {e}")

        elif self.current_action == "add_folder":
            folder_path = os.path.join(parent_path, new_name)
            try:
                os.makedirs(folder_path)
                self.model.setRootPath(QDir.rootPath())  # Reîncarcă modelul pentru a reflecta modificările
                self.current_index = None
                self.current_action = None
                self.edit_line.setVisible(False)
            except Exception as e:
                QMessageBox.warning(self, "Add Folder Error", f"Could not create folder {folder_path}: {e}")

    def cancel_edit(self):
        if self.current_index:
            self.edit_line.setVisible(False)
            self.current_index = None
            self.current_action = None

    def delete_item(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        if QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete {file_path}?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            try:
                if self.model.isDir(index):
                    shutil.rmtree(file_path)  # Șterge folderul
                else:
                    os.remove(file_path)  # Șterge fișierul
                self.model.setRootPath(QDir.rootPath())  # Reîncarcă modelul pentru a reflecta modificările
            except Exception as e:
                QMessageBox.warning(self, "Delete Error", f"Could not delete {file_path}: {e}")

    def reveal_in_explorer(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.run(['xdg-open', file_path], check=True)
        except Exception as e:
            QMessageBox.warning(self, "Reveal Error", f"Could not reveal {file_path} in explorer: {e}")

    def eventFilter(self, obj, event):
        if obj == self.edit_line and event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.cancel_edit()
                return True
        return super().eventFilter(obj, event)
    
    def open_file_in_treeview(self, index: QModelIndex):
        if index.isValid():
            if self.model.isDir(index):
                pass
            else:
                file_path = self.model.filePath(index)
                self.win.tab_bar.add_tab(file_path)

