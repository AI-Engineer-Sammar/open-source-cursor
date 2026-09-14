from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout, QPushButton, QMessageBox

class CodeViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        top_bar = QHBoxLayout()
        self.file_label = QLabel("No File Selected")
        self.file_label.setStyleSheet("font-weight: bold; color: #007ACC;")
        top_bar.addWidget(self.file_label)

        self.save_btn = QPushButton("💾 Save File")
        self.save_btn.clicked.connect(self.save_current_file)
        top_bar.addWidget(self.save_btn)

        layout.addLayout(top_bar)

        self.editor = QTextEdit()
        self.editor.setStyleSheet("font-family: Consolas, Courier, monospace; font-size: 13px;")
        layout.addWidget(self.editor)

    def load_file(self, file_path: str):
        self.current_file_path = file_path
        self.file_label.setText(f"File: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
        except Exception as e:
            self.editor.setPlainText(f"Error loading file: {str(e)}")

    def save_current_file(self):
        if not self.current_file_path:
            return
        try:
            with open(self.current_file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            QMessageBox.information(self, "Saved", f"File saved: {self.current_file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")