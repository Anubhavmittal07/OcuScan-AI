import os

path = "src/inference/pdf_report.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

target1 = """    if cataract_status == "blocked_domain_validation":
        cataract_val = "Blocked (Camera Gate)"
        cataract_obs = "Requires slit-lamp biomicroscopy illumination cross-section"
        cataract_meaning = "Webcam cannot resolve lens nucleus; slit-lamp domain validation gate enforced."
    elif cataract_status in ("unavailable", "unavailable_missing_data"):"""

repl1 = """    if cataract_status == "blocked_domain_validation":
        cataract_val = "Blocked (Camera Gate)"
        cataract_obs = "Requires slit-lamp biomicroscopy illumination cross-section"
        cataract_meaning = "Webcam cannot resolve lens nucleus; slit-lamp domain validation gate enforced."
    elif cataract_status in ("unsupported_image", "inconclusive_modality", "inconclusive") or (c_item and str(c_item.get("predicted_class", "")).lower() in ("inconclusive_modality", "unsupported_image", "inconclusive")):
        cataract_val = "Inconclusive (Modality)"
        cataract_obs = "Requires slit-lamp optical slit sectioning"
        cataract_meaning = "Lens clarity cannot be graded from external ambient photos; slit-lamp biomicroscopy required."
    elif cataract_status in ("unavailable", "unavailable_missing_data"):"""

target2 = """    if stye_status in ("unavailable", "unavailable_missing_data"):
        stye_val = "Unavailable"
        stye_obs = "Module not available for this session"
        stye_meaning = "Clinical validation requirements not met."
    elif stye_status == "blocked_domain_validation":"""

repl2 = """    if stye_status in ("unsupported_image", "inconclusive_view", "inconclusive") or (s_item and str(s_item.get("predicted_class", "")).lower() in ("inconclusive_view", "unsupported_image", "inconclusive")):
        stye_val = "Inconclusive (View)"
        stye_obs = "Resting eyelid margin contour required"
        stye_meaning = "Eyelid appears retracted or everted; resting margin required to assess hordeolum/stye."
    elif stye_status in ("unavailable", "unavailable_missing_data"):
        stye_val = "Unavailable"
        stye_obs = "Module not available for this session"
        stye_meaning = "Clinical validation requirements not met."
    elif stye_status == "blocked_domain_validation":"""

if target1 in content:
    content = content.replace(target1, repl1, 1)
    print("Replaced target1 successfully.")
else:
    print("target1 not found")

if target2 in content:
    content = content.replace(target2, repl2, 1)
    print("Replaced target2 successfully.")
else:
    print("target2 not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
