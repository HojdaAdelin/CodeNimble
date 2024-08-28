from PySide6.QtWidgets import QMessageBox
import black

def formatting(text_widget, file_manager):
    file_path = file_manager.get_opened_filename()
    if file_path is None:
        QMessageBox.critical(None, "Error", "No files are open.")
        return

    if file_path.endswith(".py"):
        code = text_widget.toPlainText()

        try:
            formatted_code = black.format_str(code, mode=black.Mode())
        except black.NothingChanged:
            formatted_code = code

        text_widget.setPlainText(formatted_code)
    else:
        QMessageBox.critical(None, "Error", "Only Python files are supported for now!")
        return
