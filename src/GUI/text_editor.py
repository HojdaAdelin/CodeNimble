import json
import re
from PySide6.QtCore import Slot, Qt, QRect, QSize, QEvent, QTimer, QStringListModel
from PySide6.QtGui import QColor, QPainter, QTextFormat, QFont, QTextCharFormat, QSyntaxHighlighter, QKeyEvent, QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QListView, QListWidget, QCompleter

class SuggestionManager:
    def __init__(self, theme):
        self.theme = theme
        self.keywords = [
            "auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "goto", "using",
            "long", "register", "return", "short", "signed", "sizeof", "static",
            "struct", "switch", "typedef", "union", "unsigned", "void", "volatile",
            "class", "namespace", "try", "catch", "throw", "public", "private", "protected",
            "virtual", "friend", "operator", "template", "this", "new", "delete"
        ]
        self.functions = [
            "cout", "cin", "endl", "printf", "scanf", "malloc", "free", "memcpy", "strlen"
        ]
        self.completer = None

    def get_all_suggestions(self):
        return self.keywords + self.functions

    def create_completer(self, widget):
        words = self.get_all_suggestions()
        self.completer = QCompleter(words)
        self.completer.setWidget(widget)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.popup().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Setarea unui QListView personalizat ca popup
        list_view = QListView()
        self.completer.setPopup(list_view)
        
        self.apply_theme(self.theme) 

        return self.completer
    
    def set_completer_font_size(self, size):
        popup = self.completer.popup()
        font = popup.font()
        font.setPointSize(size)
        popup.setFont(font)

    def apply_theme(self, theme):
        
        # Aplicare stil CSS
        self.completer.popup().setStyleSheet(f"""
              QListView {{
                background-color: {theme['treeview_background']};
                color: {theme['text_color']};
            }}
            QListView::item:selected {{
                background-color: {theme['item_hover_background_color']};
                color: {theme['item_hover_text_color']};
            }}
        """)

    def insert_completion(self, completion, text_cursor):
        extra = len(completion) - len(self.completer.completionPrefix())
        text_cursor.movePosition(QTextCursor.Left)
        text_cursor.movePosition(QTextCursor.EndOfWord)
        text_cursor.insertText(completion[-extra:])
        return text_cursor

    def should_show_popup(self, completion_prefix):
        return len(completion_prefix) >= 1

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self._code_editor = editor
    def sizeHint(self):
        return QSize(self._code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._code_editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, config, theme):
        super().__init__()
        self.theme = theme
        self.highlighter = CPPHighlighter(self.document(), self.theme)
        self.line_number_area = LineNumberArea(self)
        self.setFrameStyle(QPlainTextEdit.NoFrame)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.config = config

        self.suggestion_manager = SuggestionManager(self.theme)
        self.completer = self.suggestion_manager.create_completer(self)
        self.completer.activated.connect(self.insert_completion)
        self.apply_settings()
        self.apply_theme(self.theme)
        # Conectează semnalele și sloturile
        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QRect, int].connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)

    def apply_settings(self):
        font_size_str = self.config.get("editor_font_size", "10px")
        font_size = int(font_size_str)
        self.font = QFont("Courier", font_size)
        self.setFont(self.font)
        self.suggestion_manager.set_completer_font_size(font_size-5)

    def apply_theme(self, theme):
        highlight_color = theme.get("highlight_color", "#ffff99")
        self.highlight_color = QColor(highlight_color)
        self.highlight_current_line()
        self.background_color = QColor(theme["line_number_background"])
        self.foreground_color = QColor(theme["line_number_text_color"])
        self.highlighter.setTheme(theme)
        self.suggestion_manager.apply_theme(theme)

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    # Code suggestions

    def insert_completion(self, completion):
        tc = self.textCursor()
        tc = self.suggestion_manager.insert_completion(completion, tc)
        self.setTextCursor(tc)

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()
    
    def update_completion(self):
        completion_prefix = self.text_under_cursor()

        if self.suggestion_manager.should_show_popup(completion_prefix):
            if completion_prefix != self.completer.completionPrefix():
                self.completer.setCompletionPrefix(completion_prefix)
                self.completer.popup().setCurrentIndex(
                    self.completer.completionModel().index(0, 0))

            cr = self.cursorRect()
            cr.setWidth(self.completer.popup().sizeHintForColumn(0) +
                        self.completer.popup().verticalScrollBar().sizeHint().width() + 30)
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), self.background_color)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setFont(self.font)
                number = str(block_number + 1)
                painter.setPen(self.foreground_color)
                width = self.line_number_area.width()
                height = self.fontMetrics().height()
                painter.drawText(0, top, width, height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

        painter.end()

    @Slot()
    def update_line_number_area_width(self, newBlockCount):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    @Slot()
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    @Slot()
    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            # Folosește culoarea de highlight din themes.json
            selection.format.setBackground(self.highlight_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)


    def insertCompletion(self, key):
        cursor = self.textCursor()
        
        # Define the pairs of characters and their type
        pairs = {
            Qt.Key_ParenLeft: (')', '('),
            Qt.Key_BracketLeft: (']', '['),
            Qt.Key_BraceLeft: ('}', '{'),
            34: ('"', '"'),  # 34 is the code for double quotes
            39: ("'", "'")   # 39 is the code for single quote
        }

        if key in pairs:
            closing, opening = pairs[key]
            
            # Insert the pair of characters
            cursor.insertText(opening + closing)
            
            # Position the cursor between the pair of characters
            cursor.movePosition(QTextCursor.PreviousCharacter)
            self.setTextCursor(cursor)


    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab):
                current_item = self.completer.popup().currentIndex().data()
                if current_item:
                    self.insert_completion(current_item)
                    self.completer.popup().hide()
                    event.accept()
                    return
            elif event.key() == Qt.Key_Escape:
                self.completer.popup().hide()
                event.accept()
                return
            elif event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_PageUp, Qt.Key_PageDown):
                self.completer.popup().keyPressEvent(event)
                return

        if event.key() == Qt.Key_Backspace and event.modifiers() == Qt.ControlModifier:
            super().keyPressEvent(event)
            return

        if event.key() in {Qt.Key_Return, Qt.Key_Enter}:
            self.handleNewLine()
            return

        if event.key() in {Qt.Key_ParenLeft, Qt.Key_BracketLeft, Qt.Key_BraceLeft, 34, 39}:
            self.insertCompletion(event.key())
            return

        if event.key() == Qt.Key_Backspace and not event.modifiers():
            self.handleBackspace()
            self.update_completion()
            return

        # Altele (de exemplu, săgețile)
        super().keyPressEvent(event)
        self.update_completion()

    def handleNewLine(self):
        cursor = self.textCursor()
        current_line = cursor.block().text()
        indent = self.getIndentation(current_line)

        completions = {
            "IF": "if() {\n\n}",
            "FOR": "for(int i = 1; i <= n; i++) {\n\n}",
            "WHILE": "while() {\n\n}",
            "INT": "int () {\n\n}",
            "CPP": "#include <bits/stdc++.h>\n\nusing namespace std;\n\nint main() {\n\n    return 0;\n}"
        }
        if current_line in completions or current_line.startswith("FOR-"):
            # Obținem codul de completare de bază
            if current_line in completions:
                code = completions[current_line]
            elif current_line.startswith("FOR-"):
                # Extragem litera variabilei (de exemplu FOR-J => litera va fi 'J')
                variable = current_line.split('-')[1] if len(current_line.split('-')) > 1 else 'i'
                code = re.sub(r'\bi\b', variable.lower(), completions["FOR"])
            
            # Ștergem linia curentă și inserăm șablonul
            cursor.select(QTextCursor.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.insertText(code)

            # Poziționăm cursorul la începutul blocului pentru a edita după inserție
            cursor.movePosition(QTextCursor.StartOfBlock)

            # Comportament specific pentru fiecare comandă
            if current_line == "IF":
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            elif current_line.startswith("FOR"):
                # Mutăm cursorul pentru a ajunge la prima poziție de editare (după 'n')
                pos = code.index("n")  # Poziția lui 'n' în for(int i = 1; i <= n; i++) {...}
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, pos + 1)  # Mutăm la poziția lui 'n'
            elif current_line == "WHILE":
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            elif current_line == "INT":
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            elif current_line == "CPP":
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            
            # Setăm cursorul la poziția corectă pentru utilizator
            self.setTextCursor(cursor)
            return

        # Check if the cursor is between brackets
        if self.isCursorBetweenBrackets(cursor):
            super().keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier))
            self.insertPlainText(indent + "    ")
            self.insertPlainText("\n" + indent)
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Up)
            cursor.movePosition(QTextCursor.EndOfLine)
            self.setTextCursor(cursor)
        else:
            super().keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier))
            self.insertPlainText(indent)

    def getIndentation(self, line):
        return line[:len(line) - len(line.lstrip())]

    def isCursorBetweenBrackets(self, cursor):
        doc = self.document()
        pos = cursor.position()
        
        if pos > 0 and pos < doc.characterCount() - 1:
            prev_char = doc.characterAt(pos - 1)
            next_char = doc.characterAt(pos)
            return ((prev_char == '(' and next_char == ')') or
                    (prev_char == '[' and next_char == ']') or
                    (prev_char == '{' and next_char == '}'))
        return False

    def handleOpeningBracket(self, bracket):
        cursor = self.textCursor()
        super().keyPressEvent(QKeyEvent(QEvent.KeyPress, ord(bracket), Qt.NoModifier))
        
        closing_bracket = {'{': '}', '[': ']', '(': ')'}[bracket]
        self.insertPlainText(closing_bracket)
        cursor.movePosition(QTextCursor.Left)
        self.setTextCursor(cursor)

    def handleClosingBracket(self, bracket):
        cursor = self.textCursor()
        next_char = self.document().characterAt(cursor.position())
        
        if next_char == bracket:
            cursor.movePosition(QTextCursor.Right)
            self.setTextCursor(cursor)
        else:
            super().keyPressEvent(QKeyEvent(QEvent.KeyPress, ord(bracket), Qt.NoModifier))

    def handleBackspace(self):
        cursor = self.textCursor()
        
        # Dacă există text selectat, îl ștergem și ieșim din funcție
        if cursor.hasSelection():
            cursor.removeSelectedText()
            return
        
        # Verificăm dacă nu suntem la începutul documentului
        if cursor.atStart():
            return
        
        # Salvăm poziția curentă
        position = cursor.position()
        
        # Obținem caracterul de dinainte de cursor
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
        char_before = cursor.selectedText()
        
        # Definim perechile de caractere
        pairs = {"(": ")", "[": "]", "{": "}", "\"": "\"", "'": "'"}
        
        # Verificăm dacă caracterul de dinainte este o deschidere de paranteză
        if char_before in pairs:
            # Salvăm selecția curentă
            cursor.setPosition(position)
            # Selectăm caracterul următor
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            char_after = cursor.selectedText()
            
            # Dacă caracterul următor este perechea potrivită, ștergem ambele caractere
            if char_after == pairs[char_before]:
                cursor.removeSelectedText()
                cursor.deletePreviousChar()
                return
        
        # Dacă nu am șters o pereche, ștergem doar caracterul anterior
        cursor.setPosition(position)
        cursor.deletePreviousChar()

    def insertSuggestion(self, text):
        cursor = self.textCursor()
        
        # Selectează cuvântul sub cursor
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.removeSelectedText()
        
        # Inserează textul completării
        cursor.insertText(text)
        self.setTextCursor(cursor)

class CPPHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, theme=None):
        super().__init__(parent)
        self.theme = theme or {}
        self._mappings = {}
        self.setup_highlighting()

    def setTheme(self, theme):
        self.theme = theme
        self._mappings.clear()
        self.setup_highlighting()
        self.rehighlight()  # Reaplică evidențierea pentru a reflecta schimbările de temă

    def setup_highlighting(self):
        # Format pentru #include
        include_format = QTextCharFormat()
        include_format.setForeground(QColor(self.theme.get("include_color", "#5C6370")))
        self.add_mapping(r'#include\s*[<"].*?[">]', include_format)

        # Format pentru keyword-uri
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(self.theme.get("keyword_color", "#C678DD")))
        keywords = r'\b(?:class|return|if|else|for|while|switch|case|break|continue|namespace|public|private|protected|void|int|float|double|char|bool|const|static|virtual|override|explicit|vector|cout|cin|short|import|print|printf|max|min)\b'
        self.add_mapping(keywords, keyword_format)

        # Format pentru simboluri
        symbol_format = QTextCharFormat()
        symbol_format.setForeground(QColor(self.theme.get("symbol_color", "#56b6c2")))
        self.add_mapping(r'[\-*%&|^!~<>=?:;]', symbol_format)

        # Format pentru cifre
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(self.theme.get("number_color", "#d19a66")))
        self.add_mapping(r'\b\d+\b', number_format)

        # Format pentru paranteze
        parenthesis_format = QTextCharFormat()
        parenthesis_format.setForeground(QColor(self.theme.get("parenthesis_color", "#e06c75")))
        self.add_mapping(r'[()\[\]{}]', parenthesis_format)

        # Format pentru stringuri între ghilimele
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(self.theme.get("string_color", "#98C379")))
        self.add_mapping(r'\".*?\"', string_format)

        # Format pentru stringuri între apostroafe
        self.add_mapping(r'\'[^\'\n]*\'', string_format)

        # Format pentru comentarii
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(self.theme.get("comment_color", "#5C6370")))
        self.add_mapping(r'\/\/.*', comment_format)
        self.add_mapping(r'\/\*.*?\*\/', comment_format)  # Comentarii de tip bloc
        self.add_mapping(r'\#.*', comment_format)

    def add_mapping(self, pattern, format):
        self._mappings[pattern] = format

    def highlightBlock(self, text):
        for pattern, format in self._mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format)

