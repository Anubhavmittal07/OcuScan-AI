import os

path = 'src/inference/pdf_report.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Font registration block to add near imports
font_reg_code = '''
# ---------------------------------------------------------------------------
# Devanagari / Hindi Font Registration
# ---------------------------------------------------------------------------
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HINDI_FONT_AVAILABLE = False
try:
    for fp in ["C:/Windows/Fonts/Nirmala.ttc", "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"]:
        if os.path.exists(fp):
            if fp.endswith(".ttc"):
                pdfmetrics.registerFont(TTFont("NirmalaUI", fp, subfontIndex=0))
                pdfmetrics.registerFont(TTFont("NirmalaUI-Bold", fp, subfontIndex=1))
                pdfmetrics.registerFontFamily("NirmalaUI", normal="NirmalaUI", bold="NirmalaUI-Bold", italic="NirmalaUI", boldItalic="NirmalaUI-Bold")
                HINDI_FONT_AVAILABLE = True
                break
except Exception as fe:
    HINDI_FONT_AVAILABLE = False
'''

if 'HINDI_FONT_AVAILABLE' not in text:
    text = text.replace('import logging', 'import logging\n' + font_reg_code, 1)

# Update _get_shared_styles signature and body
old_styles_def = '''def _get_shared_styles():
    """Builds clean, compact ReportLab styles for 2-page documents."""
    styles = getSampleStyleSheet()

    primary_blue = colors.HexColor("#0f3a69")
    accent_blue = colors.HexColor("#0284c7")
    dark_text = colors.HexColor("#0f172a")
    sub_text = colors.HexColor("#475569")
    border_color = colors.HexColor("#cbd5e1")

    return {
        "title": ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=primary_blue
        ),
        "subtitle": ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=sub_text
        ),
        "section_header": ParagraphStyle(
            "SectionHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=primary_blue,
            spaceAfter=3
        ),
        "body": ParagraphStyle(
            "DocBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10,
            textColor=dark_text
        ),
        "body_bold": ParagraphStyle(
            "DocBodyBold",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.8,
            leading=10,
            textColor=dark_text
        ),
        "disclaimer": ParagraphStyle(
            "DisclaimerText",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=9,
            textColor=colors.HexColor("#991b1b")
        ),
        "caption": ParagraphStyle(
            "DocCaption",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=6.5,
            leading=8.5,
            alignment=1,
            textColor=dark_text
        ),'''

new_styles_def = '''def _get_shared_styles(language: str = "en"):
    """Builds clean, compact ReportLab styles with proper font selection."""
    styles = getSampleStyleSheet()

    is_hi = language.lower().startswith("hi")
    fn_normal = "NirmalaUI" if (is_hi and HINDI_FONT_AVAILABLE) else "Helvetica"
    fn_bold = "NirmalaUI-Bold" if (is_hi and HINDI_FONT_AVAILABLE) else "Helvetica-Bold"

    primary_blue = colors.HexColor("#0f3a69")
    accent_blue = colors.HexColor("#0284c7")
    dark_text = colors.HexColor("#0f172a")
    sub_text = colors.HexColor("#475569")
    border_color = colors.HexColor("#cbd5e1")

    return {
        "title": ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName=fn_bold,
            fontSize=15,
            leading=18,
            textColor=primary_blue
        ),
        "subtitle": ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName=fn_normal,
            fontSize=8,
            leading=10,
            textColor=sub_text
        ),
        "section_header": ParagraphStyle(
            "SectionHeader",
            parent=styles["Normal"],
            fontName=fn_bold,
            fontSize=9.5,
            leading=12,
            textColor=primary_blue,
            spaceAfter=3
        ),
        "body": ParagraphStyle(
            "DocBody",
            parent=styles["Normal"],
            fontName=fn_normal,
            fontSize=7.8,
            leading=10,
            textColor=dark_text
        ),
        "body_bold": ParagraphStyle(
            "DocBodyBold",
            parent=styles["Normal"],
            fontName=fn_bold,
            fontSize=7.8,
            leading=10,
            textColor=dark_text
        ),
        "disclaimer": ParagraphStyle(
            "DisclaimerText",
            parent=styles["Normal"],
            fontName=fn_bold,
            fontSize=7,
            leading=9,
            textColor=colors.HexColor("#991b1b")
        ),
        "caption": ParagraphStyle(
            "DocCaption",
            parent=styles["Normal"],
            fontName=fn_normal,
            fontSize=6.5,
            leading=8.5,
            alignment=1,
            textColor=dark_text
        ),'''

text = text.replace(old_styles_def, new_styles_def, 1)

# Ensure _get_shared_styles is called with language parameter
text = text.replace('st = _get_shared_styles()\n    demo = _resolve_demographics(session_data, user_data)', 'st = _get_shared_styles(selected_lang)\n    demo = _resolve_demographics(session_data, user_data)', 1)
text = text.replace('st = _get_shared_styles()\n    demo = _resolve_demographics(session_data, user_data)\n    models = _extract_model_outputs(session_data)\n    story = []', 'st = _get_shared_styles(lang)\n    demo = _resolve_demographics(session_data, user_data)\n    models = _extract_model_outputs(session_data)\n    story = []', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated src/inference/pdf_report.py with NirmalaUI Devanagari font support!')
