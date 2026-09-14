import os
import shutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import pyqtSignal

class WorkspaceFileTree(QWidget):
    file_selected_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.workspace_path = "."
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        top_bar = QHBoxLayout()
        self.btn_upload = QPushButton("📂 Import File")
        self.btn_upload.setStyleSheet("font-weight: bold; background-color: #7c3aed; color: white; padding: 6px;")
        self.btn_upload.clicked.connect(self.upload_file)
        top_bar.addWidget(self.btn_upload)
        layout.addLayout(top_bar)

        self.model = QFileSystemModel()
        self.model.setRootPath("")

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAnimated(True)
        self.tree.setIndentation(18)
        self.tree.setSortingEnabled(True)

        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

        self.tree.doubleClicked.connect(self.on_file_double_clicked)
        layout.addWidget(self.tree)

    def set_workspace_path(self, path: str):
        self.workspace_path = os.path.abspath(path)
        os.makedirs(self.workspace_path, exist_ok=True)
        self.model.setRootPath(self.workspace_path)
        self.tree.setRootIndex(self.model.index(self.workspace_path))

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select File to Import into Workspace", 
            "", 
            "All Files (*);;Python Files (*.py);;JavaScript (*.js);;Text Files (*.txt)"
        )
        
        if file_path:
            filename = os.path.basename(file_path)
            destination_path = os.path.join(self.workspace_path, filename)

            try:
                shutil.copy(file_path, destination_path)
                QMessageBox.information(self, "Success", f"File '{filename}' imported into Stoni workspace!")
            except Exception as e:
                QMessageBox.critical(self, "Upload Error", f"Failed to upload file: {str(e)}")

    def on_file_double_clicked(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.file_selected_signal.emit(file_path)
