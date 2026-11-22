import os

pdf_report_path = 'src/inference/pdf_report.py'
with open(pdf_report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update titles
content = content.replace(
    '"screening_title": "OcuScan — Ocular Health Screening Report",\n        "screening_subtitle": "Patient-Friendly Screening Summary & Visual Biomarkers • Research Prototype",',
    '"screening_title": "OcuScan — Comprehensive Major Screening Report",\n        "screening_subtitle": "Patient-Friendly Screening Summary, Specialist ML Architectures & Clinical Evidence",',
    1
)
content = content.replace(
    '"screening_title": "ऑक्यूस्कैन — नेत्र स्वास्थ्य स्क्रीनिंग रिपोर्ट",\n        "screening_subtitle": "मरीज-अनुकूल स्क्रीनिंग सारांश एवं विजुअल बायोमार्कर • अनुसंधान प्रोटोटाइप",',
    '"screening_title": "ऑक्यूस्कैन — व्यापक प्रमुख स्क्रीनिंग रिपोर्ट",\n        "screening_subtitle": "मरीज-अनुकूल सारांश, विशेषज्ञ एआई मॉडल आउटपुट एवं नैदानिक साक्ष्य",',
    1
)

# 2. Extract technical scorecard story
target_func = '''def build_technical_scorecard_pdf(
    session_data: Dict[str, Any],
    user_data: Optional[Dict[str, Any]] = None,
    language: str = "en"
) -> bytes:'''

new_tech_story_func = '''def _build_technical_scorecard_story(
    session_data: Dict[str, Any],
    user_data: Optional[Dict[str, Any]] = None,
    language: str = "en"
) -> List[Any]:
    """
    Builds the story flowables for the Technical Research & Clinician Review pages.
    """
    lang = "hi" if language.lower().startswith("hi") else "en"
    t = REPORT_TEXTS[lang]
    st = _get_shared_styles()
    demo = _resolve_demographics(session_data, user_data)
    models = _extract_model_outputs(session_data)
    story = []
'''

idx = content.find(target_func)
if idx != -1:
    end_doc_build = content.find('doc.build(story)\n    pdf_bytes = buffer.getvalue()\n    buffer.close()\n    return pdf_bytes', idx)
    if end_doc_build != -1:
        old_block = content[idx:end_doc_build + len('doc.build(story)\n    pdf_bytes = buffer.getvalue()\n    buffer.close()\n    return pdf_bytes')]
        
        header_to_remove = '''def build_technical_scorecard_pdf(
    session_data: Dict[str, Any],
    user_data: Optional[Dict[str, Any]] = None,
    language: str = "en"
) -> bytes:
    """
    Builds the 2-Page Technical Research Scorecard & Clinician Review.
    Page 1: Specialist Model Architectures, Outputs, Segmentation Coverage, MedSigLIP Case Retrieval.
    Page 2: Cross-Modal Concordance, Reliability Gating Audits (Mendeley Confound), Dataset Provenance, Safe Boundaries.
    """
    lang = "hi" if language.lower().startswith("hi") else "en"
    t = REPORT_TEXTS[lang]
    st = _get_shared_styles()
    demo = _resolve_demographics(session_data, user_data)
    models = _extract_model_outputs(session_data)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )
    story = []'''
        
        inner_story = old_block.replace(header_to_remove, new_tech_story_func).replace(
            'doc.build(story)\n    pdf_bytes = buffer.getvalue()\n    buffer.close()\n    return pdf_bytes',
            'return story'
        )
        
        replacement_block = inner_story + '''\n\n
def build_technical_scorecard_pdf(
    session_data: Dict[str, Any],
    user_data: Optional[Dict[str, Any]] = None,
    language: str = "en"
) -> bytes:
    """
    Builds the Technical Research Scorecard & Clinician Review PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )
    story = _build_technical_scorecard_story(session_data, user_data, language)
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
'''
        content = content[:idx] + replacement_block + content[idx + len(old_block):]
        print('Successfully refactored _build_technical_scorecard_story and build_technical_scorecard_pdf')
    else:
        print('Could not find end of doc.build')
else:
    print('Could not find target_func')

# 3. Append technical story to build_screening_report_pdf
scr_build_target = '''    story.append(alert_box)

    doc.build(story)'''

scr_build_replacement = '''    story.append(alert_box)

    # EXACT PAGE BREAK FOR TECHNICAL SPECIALIST PAGES (MAJOR REPORT INTEGRATION)
    story.append(PageBreak())
    tech_story = _build_technical_scorecard_story(session_data, user_data, selected_lang)
    story.extend(tech_story)

    doc.build(story)'''

if scr_build_target in content:
    content = content.replace(scr_build_target, scr_build_replacement, 1)
    print('Successfully merged technical scorecard into build_screening_report_pdf')
else:
    print('Could not find scr_build_target')

with open(pdf_report_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved updated src/inference/pdf_report.py successfully')
