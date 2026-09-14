import os
import sys
import json
import traceback
from PyQt6.QtCore import QThread, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.tools import AGENT_TOOLS, execute_tool_call
from core.safety import validate_command
from reports.pdf_builder import generate_pdf_report

class AgentWorker(QThread):
    log_signal = pyqtSignal(str)
    approval_request_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str, str)
    error_signal = pyqtSignal(str)

    def __init__(self, provider, model_name, api_key, project_folder, selected_lang, goal_prompt):
        super().__init__()
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key
        self.project_folder = project_folder
        self.selected_lang = selected_lang
        self.goal_prompt = goal_prompt

        self.approval_pending = False
        self.command_approved = False

    def run(self):
        try:
            self.log_signal.emit(f"🚀 Initializing Stoni Agent ({self.provider} - {self.model_name})...")
            os.makedirs(os.path.abspath(self.project_folder), exist_ok=True)

            system_instruction = (
                f"You are an autonomous AI Developer Agent working in target directory '{os.path.abspath(self.project_folder)}'.\n"
                f"Target Programming Language: {self.selected_lang}.\n"
                f"Goal: {self.goal_prompt}\n\n"
                "CRITICAL INSTRUCTION:\n"
                "You MUST invoke tool `write_file_content` to actually write full working source files into the target folder. "
                "Do NOT just print code in text responses. Create all required project files (HTML, CSS, JS, README, etc.) step-by-step."
            )

            if self.provider == "Gemini Cloud":
                self.run_gemini(system_instruction)
            else:
                self.run_ollama(system_instruction)

        except Exception as e:
            err_msg = f"Error during agent execution: {str(e)}\n{traceback.format_exc()}"
            self.log_signal.emit(f"❌ {err_msg}")
            self.error_signal.emit(str(e))

    def run_gemini(self, system_instruction):
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=self.api_key)
        
        chat = client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=AGENT_TOOLS,
                temperature=0.2
            )
        )

        response = chat.send_message(f"Start building the project for: {self.goal_prompt}. Make sure to write files to disk.")

        while True:
            if response.text:
                self.log_signal.emit(f"\n🤖 Agent Output:\n{response.text}")

            if not response.function_calls:
                self.log_signal.emit("\n✅ Execution finished. Generating architecture documentation...")
                pdf_file = generate_pdf_report(self.project_folder, self.goal_prompt, self.selected_lang)
                self.finished_signal.emit("Project completed successfully!", pdf_file)
                break

            for function_call in response.function_calls:
                tool_name = function_call.name
                tool_args = dict(function_call.args)

                self.log_signal.emit(f"🛠️ Tool Invoked: {tool_name}({tool_args})")

                if tool_name == "execute_terminal_command":
                    cmd = tool_args.get("command", "")
                    is_safe, reason = validate_command(cmd)
                    if not is_safe:
                        self.log_signal.emit(f"⚠️ Security Intercepted: {reason}")
                        self.approval_pending = True
                        self.approval_request_signal.emit(cmd)
                        
                        while self.approval_pending:
                            self.msleep(200)

                        if not self.command_approved:
                            tool_result = "Command execution rejected by user."
                            response = chat.send_message(
                                types.Part.from_function_response(name=tool_name, response={"result": tool_result})
                            )
                            continue

                tool_result = execute_tool_call(tool_name, tool_args, self.project_folder)
                self.log_signal.emit(f"📋 Output: {str(tool_result)[:300]}")

                response = chat.send_message(
                    types.Part.from_function_response(name=tool_name, response={"result": tool_result})
                )

    def run_ollama(self, system_instruction):
        import ollama

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Build the project for: {self.goal_prompt}"}
        ]

        response = ollama.chat(
            model=self.model_name,
            messages=messages,
            tools=AGENT_TOOLS
        )

        message = response.get("message", {})
        if message.get("content"):
            self.log_signal.emit(f"\n🤖 Agent:\n{message['content']}")

        pdf_file = generate_pdf_report(self.project_folder, self.goal_prompt, self.selected_lang)
        self.finished_signal.emit("Ollama Agent Task finished!", pdf_file)
