from PyQt6.Qsci import QsciScintilla, QsciLexerCPP
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QColor, QFont, QKeyEvent
from PySide6.QtCore import Qt

class Editor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        self.setup_lexer()
        self.add_line_numbers()

    def setup_editor(self):
        """Configure basic editor settings."""
        self.font = QFont("Consolas", 16)
        self.setUtf8(True)
        self.setFont(self.font)  
        self.setPaper(QColor("#454545"))  # Fundal închis pentru editor
        self.setAutoIndent(True)
        self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)  # Activăm potrivirea strictă a parantezelor
        self.setCaretLineBackgroundColor(QColor("#333333"))  # Culoare linie activă pentru paranteză
        self.setCaretForegroundColor(QColor("#ffffff"))  # Culoare pentru cursor (alb)
        self.setCaretLineVisible(True)
        self.setMatchedBraceBackgroundColor(QColor("#444444"))  # Culoare de fundal gri închis pentru paranteze
        self.setMatchedBraceForegroundColor(QColor("#ffffff"))  # Culoare text paranteze (alb)
        self.setUnmatchedBraceBackgroundColor(QColor("#444444"))  # Culoare de fundal gri pentru paranteze nereguli
        self.setUnmatchedBraceForegroundColor(QColor("#ffffff"))  # Culoare text paranteze nereguli (rosu)
        self.setSelectionBackgroundColor(QColor("#555555"))  # Culoare fundal selecție
        self.setIndentationGuides(True)
        self.setIndentationWidth(4)  
        self.setTabWidth(4) 

    def setup_lexer(self):
        """Set up syntax highlighting for C++."""
        lexer = QsciLexerCPP()
        lexer.setDefaultFont(self.font)
        lexer.setFont(self.font, QsciLexerCPP.Default)
        lexer.setFont(self.font, QsciLexerCPP.Keyword)
        lexer.setFont(self.font, QsciLexerCPP.Identifier)
        lexer.setFont(self.font, QsciLexerCPP.Operator)
        lexer.setFont(self.font, QsciLexerCPP.Number)
        lexer.setFont(self.font, QsciLexerCPP.SingleQuotedString)
        lexer.setFont(self.font, QsciLexerCPP.DoubleQuotedString)
        lexer.setFont(self.font, QsciLexerCPP.UnclosedString)
        lexer.setFont(self.font, QsciLexerCPP.Comment)
        lexer.setFont(self.font, QsciLexerCPP.CommentLine)
        lexer.setColor(QColor("#ffffff"), QsciLexerCPP.Default)  
        lexer.setColor(QColor("#ff6b6b"), QsciLexerCPP.Keyword)  
        lexer.setColor(QColor("#7a7a7a"), QsciLexerCPP.Comment)  
        lexer.setColor(QColor("#f1fa8c"), QsciLexerCPP.Number)  
        lexer.setColor(QColor("#8be9fd"), QsciLexerCPP.Operator)  
        lexer.setColor(QColor("#ffb86c"), QsciLexerCPP.SingleQuotedString)  
        lexer.setColor(QColor("#ffb86c"), QsciLexerCPP.DoubleQuotedString)  
        lexer.setColor(QColor("#ffb86c"), QsciLexerCPP.UnclosedString) 
        lexer.setColor(QColor("#7a7a7a"), QsciLexerCPP.PreProcessor)
        self.setLexer(lexer)

    def add_line_numbers(self):
        self.setMarginsFont(self.font) 
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "00000")  
        self.setMarginsBackgroundColor(QColor("#454545")) 
        self.setMarginsForegroundColor(QColor("#ffffff")) 

class EditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.editor = Editor()
        layout.addWidget(self.editor)
        self.setLayout(layout)
