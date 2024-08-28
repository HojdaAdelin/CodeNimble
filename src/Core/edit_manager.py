class EditManager:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def undo(self):
        self.text_widget.undo()

    def redo(self):
        self.text_widget.redo()

    def copy(self):
        if self.text_widget.textCursor().hasSelection():
            self.text_widget.copy()

    def cut(self):
        if self.text_widget.textCursor().hasSelection():
            self.text_widget.cut()

    def paste(self):
        self.text_widget.paste()

    def delete(self):
        
        cursor = self.text_widget.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()

    def clear(self):
        
        self.text_widget.clear()

    def select_all(self):
        self.text_widget.selectAll()
