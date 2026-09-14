import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QLineEdit, QPushButton, 
                             QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from core.agent_worker import AgentWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenSource AI Agent — Autonomous IDE")
        self.resize(1200, 800)
        
        # Apply dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow { background-color: #0f172a; color: #f8fafc; }
            QWidget { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }
            QLineEdit, QComboBox, QTextEdit { 
                background-color: #1e293b; 
                border: 1px solid #334155; 
                border-radius: 6px; 
                padding: 8px; 
                color: #f8fafc; 
            }
            QPushButton { 
                background-color: #6366f1; 
                color: white; 
                border-radius: 6px; 
                padding: 10px 16px; 
                font-weight: bold; 
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Header
        header = QLabel("🤖 OpenSource AI Agent — Autonomous Developer Studio")
        header.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        header.setStyleSheet("color: #818cf8; margin-bottom: 10px;")
        main_layout.addWidget(header)

        # Controls Layout
        controls_layout = QHBoxLayout()
        
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["Gemini Cloud", "Ollama Local"])

        self.model_combo = QComboBox()

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter Gemini API Key (or set GEMINI_API_KEY env)")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Connect signals after UI elements initialization
        self.provider_combo.currentTextChanged.connect(self.on_provider_change)
        self.update_models("Gemini Cloud")

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["JavaScript", "Python", "HTML/CSS", "Go", "TypeScript"])

        controls_layout.addWidget(QLabel("Provider:"))
        controls_layout.addWidget(self.provider_combo)
        controls_layout.addWidget(QLabel("Model:"))
        controls_layout.addWidget(self.model_combo)
        controls_layout.addWidget(self.api_key_input)
        controls_layout.addWidget(QLabel("Target Language:"))
        controls_layout.addWidget(self.lang_combo)

        main_layout.addLayout(controls_layout)

        # Prompt Input
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Describe the project you want OpenSource AI Agent to build...")
        self.prompt_input.setMaximumHeight(100)
        main_layout.addWidget(self.prompt_input)

        # Run Button
        self.run_btn = QPushButton("🚀 Run OpenSource AI Agent")
        self.run_btn.clicked.connect(self.start_agent)
        main_layout.addWidget(self.run_btn)

        # Output Terminal Log Window
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #020617; color: #38bdf8; font-family: monospace;")
        main_layout.addWidget(self.log_output)

    def on_provider_change(self, provider):
        self.update_models(provider)

    def update_models(self, provider):
        self.model_combo.clear()
        if provider == "Gemini Cloud":
            self.model_combo.addItems(["gemini-2.5-flash", "gemini-1.5-pro"])
            if hasattr(self, 'api_key_input'):
                self.api_key_input.setEnabled(True)
        else:
            self.model_combo.addItems(["qwen2.5-coder:0.5b", "gemma2:2b", "llama3.2:1b"])
            if hasattr(self, 'api_key_input'):
                self.api_key_input.setEnabled(False)

    def start_agent(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Warning", "Please enter a project description.")
            return

        provider = self.provider_combo.currentText()
        model_name = self.model_combo.currentText()
        api_key = self.api_key_input.text().strip() or os.getenv("GEMINI_API_KEY", "")
        selected_lang = self.lang_combo.currentText()
        project_folder = "generated_app"

        self.log_output.clear()
        self.run_btn.setEnabled(False)

        self.worker = AgentWorker(provider, model_name, api_key, project_folder, selected_lang, prompt)
        self.worker.log_signal.connect(self.append_log)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.error_signal.connect(self.on_error)
        self.worker.start()

    def append_log(self, message):
        self.log_output.append(message)

    def on_finished(self, status, pdf_path):
        self.log_output.append(f"\n🎉 {status}")
        self.log_output.append(f"📄 Architecture Report Generated: {pdf_path}")
        self.run_btn.setEnabled(True)

    def on_error(self, error_msg):
        self.log_output.append(f"\n❌ Error: {error_msg}")
        self.run_btn.setEnabled(True)
