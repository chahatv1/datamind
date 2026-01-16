from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

def generate_pdf_report(quality_report, patterns, anomalies, story):
    """Generates a professional PDF report from session data."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # --- Title ---
    title_style = styles['Title']
    elements.append(Paragraph("DataMind Intelligence Report", title_style))
    elements.append(Spacer(1, 20))

    # --- Section 1: Executive Summary (AI Story) ---
    if story:
        elements.append(Paragraph("1. Executive Summary", styles['Heading2']))
        # Split story into paragraphs to handle newlines
        for part in story.split('\n'):
            if part.strip():
                elements.append(Paragraph(part, styles['Normal']))
                elements.append(Spacer(1, 6))
        elements.append(Spacer(1, 12))

    # --- Section 2: Data Quality Metrics ---
    elements.append(Paragraph("2. Data Quality Overview", styles['Heading2']))
    
    data = [
        ["Metric", "Value"],
        ["Total Rows", f"{quality_report.get('rows', 0):,}"],
        ["Total Columns", str(quality_report.get('columns', 0))],
        ["Missing Data %", f"{quality_report.get('missing_%', 0):.2f}%"],
        ["Duplicate Rows", str(quality_report.get('duplicates', 0))]
    ]

    t = Table(data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')), # Brand Color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))

    # --- Section 3: Anomaly Detection ---
    if anomalies:
        elements.append(Paragraph("3. Anomaly Detection", styles['Heading2']))
        count = anomalies.get('count', 0)
        status = f"CRITICAL: Found {count} anomalies" if count > 0 else "PASS: No significant anomalies found"
        elements.append(Paragraph(status, styles['Normal']))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer