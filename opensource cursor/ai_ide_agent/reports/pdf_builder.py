import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(project_folder: str, goal_prompt: str, selected_lang: str) -> str:
    """Generates a PDF architectural documentation report for the generated project."""
    pdf_filename = os.path.join(project_folder, "Architecture_Documentation.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=12
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#1f2833'),
        spaceAfter=8
    )

    elements = []

    elements.append(Paragraph("✨ OpenSource AI Agent — Architecture Documentation", title_style))
    elements.append(Spacer(1, 10))

    meta_data = [
        ["Project Folder:", project_folder],
        ["Target Language:", selected_lang],
        ["Generated On:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    t = Table(meta_data, colWidths=[120, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(t)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Project Goal & Prompt:</b>", styles['Heading2']))
    elements.append(Paragraph(goal_prompt, body_style))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Generated Project Files:</b>", styles['Heading2']))

    files_found = []
    for root, _, files in os.walk(project_folder):
        for file in files:
            files_found.append([os.path.relpath(os.path.join(root, file), project_folder)])

    if files_found:
        file_table = Table(files_found, colWidths=[470])
        file_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(file_table)
    else:
        elements.append(Paragraph("No files were detected in the project folder.", body_style))

    doc.build(elements)
    return pdf_filename

generate_project_pdf_report = generate_pdf_report
