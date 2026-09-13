import os
import sys
import time
import subprocess
import streamlit as st

# ---------------------------------------------------------------------------
# 1. PDF Report Generator Tool
# ---------------------------------------------------------------------------

def generate_project_pdf_report(output_pdf_path: str, project_dir: str, code_language: str, analysis_summary: str) -> str:
    """Generates a professional PDF documentation covering infrastructure and code understanding."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

        doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, spaceAfter=12)
        heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, spaceAfter=8)
        body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, spaceAfter=6)
        code_style = ParagraphStyle('CodeStyle', parent=styles['Code'], fontSize=8, backColor='#f4f4f4', spaceAfter=6)

        story.append(Paragraph("<b>Project Complete Documentation & Architecture Report</b>", title_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("<b>1. Overview</b>", heading_style))
        story.append(Paragraph(f"<b>Target Language:</b> {code_language}", body_style))
        story.append(Paragraph(f"<b>Root Directory:</b> {os.path.abspath(project_dir)}", body_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("<b>2. Project Infrastructure</b>", heading_style))
        tree_str = ""
        for root, dirs, files in os.walk(project_dir):
            level = root.replace(project_dir, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree_str += f"{indent}{os.path.basename(root)}/\n"
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                tree_str += f"{subindent}{f}\n"

        story.append(Preformatted(tree_str if tree_str else "No files created.", code_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("<b>3. Code Understanding & Logic Flow</b>", heading_style))
        story.append(Paragraph(analysis_summary.replace("\n", "<br/>"), body_style))

        doc.build(story)
        return f"PDF documentation generated successfully at: {output_pdf_path}"
    except Exception as e:
        return f"PDF generation error: {str(e)}"

# ---------------------------------------------------------------------------
# 2. Cursor-like IDE Capabilities Tools
# ---------------------------------------------------------------------------

def list_workspace_tree(dir_path: str = ".") -> str:
    """Lists directory structure and files in the project."""
    try:
        tree_str = ""
        for root, dirs, files in os.walk(dir_path):
            level = root.replace(dir_path, '').count(os.sep)
            indent = ' ' * 4 * level
            tree_str += f"{indent}{os.path.basename(root)}/\n"
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                tree_str += f"{subindent}{f}\n"
        return tree_str if tree_str else "Directory is empty."
    except Exception as e:
        return f"Error listing directory: {str(e)}"

def read_file_content(file_path: str, start_line: int = 1, end_line: int = -1) -> str:
    """Reads specific lines or entire content of a file."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if end_line == -1 or end_line > len(lines):
            end_line = len(lines)
        selected_lines = lines[start_line - 1:end_line]
        return "".join(selected_lines)
    except Exception as e:
        return f"Error reading file: {str(e)}"

def search_codebase_grep(search_term: str, project_dir: str = ".") -> str:
    """Searches for keywords or text patterns across the entire codebase."""
    try:
        result = subprocess.run(
            ["grep", "-rnI", search_term, project_dir],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout if result.stdout else "No matches found."
    except Exception as e:
        return f"Grep search error: {str(e)}"

def replace_code_block(file_path: str, old_code: str, new_code: str) -> str:
    """Replaces a targeted chunk of code in a file without re-writing the whole file."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if old_code not in content:
            return f"Error: Exact target 'old_code' chunk not found in {file_path}."
        updated_content = content.replace(old_code, new_code, 1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        return f"Successfully patched code in '{file_path}'."
    except Exception as e:
        return f"Replace error: {str(e)}"

def write_project_file(file_path: str, content: str) -> str:
    """Creates a new file or overwrites an existing file entirely."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{file_path}' written successfully."
    except Exception as e:
        return f"File write error: {str(e)}"

def execute_terminal_command(command: str, working_dir: str = ".") -> str:
    """Executes a bash terminal command (e.g. pytest, npm test, go build, pip install)."""
    try:
        result = subprocess.run(
            command, shell=True, cwd=working_dir,
            capture_output=True, text=True, timeout=40
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Terminal command execution error: {str(e)}"

def vscode_focus_file(file_path: str, line: int = 1) -> str:
    """Focuses target file in VS Code editor at exact line."""
    try:
        subprocess.run(["code", "-r", "-g", f"{file_path}:{line}"], capture_output=True, text=True)
        return f"VS Code opened {file_path} at line {line}."
    except Exception as e:
        return f"VS Code focus error: {str(e)}"

# ---------------------------------------------------------------------------
# 3. Streamlit Application Interface
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Cursor-like AI Developer Agent", layout="wide")
st.title("⚡ Cursor-like Autonomous AI IDE Agent")

st.sidebar.header("🔑 Agent Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
selected_lang = st.sidebar.selectbox("Select Target Language:", ["Python", "Go", "JavaScript", "Rust"])
project_folder = st.sidebar.text_input("Project Folder Name:", value="generated_app")

if not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to start.")
    st.stop()

# Initialize Google GenAI SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    st.error("Google GenAI SDK is missing. Run: pip install google-genai")
    st.stop()

os.environ["GEMINI_API_KEY"] = api_key
client = genai.Client()

goal_prompt = st.text_area("Enter Project Goal:", value=f"Build a clean project in {selected_lang} with full file handling, tests, and modular structure.")

if st.button("🚀 Start Cursor-like Autonomous Agent"):
    st.write("---")
    status_box = st.empty()
    log_area = st.container()

    config = types.GenerateContentConfig(
        system_instruction=(
            f"You are a Cursor-like AI Code Agent operating on directory '{project_folder}'.\n"
            f"Programming Language: {selected_lang}.\n\n"
            "WORKFLOW RULES:\n"
            "1. Inspect existing files using `list_workspace_tree`, `read_file_content`, or `search_codebase_grep`.\n"
            "2. Make new files using `write_project_file` or edit code blocks via `replace_code_block`.\n"
            "3. Execute test/compile/build terminal commands via `execute_terminal_command` to verify functionality.\n"
            "4. Focus modified files in VS Code via `vscode_focus_file`.\n"
            "5. Automatically fix errors until the project compiles and runs cleanly without any issues.\n"
            "6. Output the exact string 'TASK_COMPLETE' followed by a detailed architecture summary ONLY when the task is 100% finished."
        ),
        tools=[
            list_workspace_tree,
            read_file_content,
            search_codebase_grep,
            replace_code_block,
            write_project_file,
            execute_terminal_command,
            vscode_focus_file
        ],
        temperature=0.2
    )

    chat = client.chats.create(model="gemini-3.5-flash", config=config)
    
    current_prompt = f"Goal: {goal_prompt}. Target Language: {selected_lang}. Begin implementation."
    iteration = 1
    completed = False
    full_thoughts = ""

    while not completed:
        with log_area:
            st.markdown(f"### 🔄 Iteration {iteration}")
            with st.spinner("Cursor Agent searching code, running terminal commands, and editing..."):
                response = chat.send_message(current_prompt)
                
                # Safe Text Extraction
                response_text = response.text or ""

                if response_text:
                    st.text_area(f"Developer Log Iteration {iteration}:", response_text, height=150)
                    full_thoughts += f"\n--- Iteration {iteration} ---\n" + response_text

                if "TASK_COMPLETE" in response_text.upper():
                    completed = True
                    st.success("🎉 Project Completed Successfully!")
                    
                    pdf_filename = f"{project_folder}_Documentation.pdf"
                    pdf_result = generate_project_pdf_report(
                        output_pdf_path=pdf_filename,
                        project_dir=project_folder,
                        code_language=selected_lang,
                        analysis_summary=full_thoughts
                    )
                    
                    st.info(pdf_result)
                    if os.path.exists(pdf_filename):
                        with open(pdf_filename, "rb") as pdf_file:
                            st.download_button(
                                label="📄 Download Project Documentation PDF",
                                data=pdf_file,
                                file_name=pdf_filename,
                                mime="application/pdf"
                            )
                    break

                current_prompt = "Analyze execution results. Fix remaining issues, run tests via terminal, and continue. Output 'TASK_COMPLETE' when done."
                iteration += 1
                time.sleep(1)