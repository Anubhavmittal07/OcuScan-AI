import os

with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_cataract_modal = """    } else if (modelId === 'model_d_cataract') {
      detailsHtml += `
        <div>
          <div class="rel-modal-sec-title">👁️ Nuclear Cataract &amp; LOCS III Staging</div>
          <p>Evaluates lens opacification and nuclear cataract from clinical slit-lamp optical sections (Cruz-Vega &amp; Ignatowicz cohorts).</p>
          <table class="rel-table" style="margin-top: 8px;">
            <thead><tr><th>Metric</th><th>Value</th></tr></thead>
            <tbody>
              <tr><td>Screening Accuracy</td><td><strong>80.0%</strong></td></tr>
              <tr><td>Sensitivity</td><td><strong>100.0%</strong></td></tr>
              <tr><td>ROC-AUC</td><td><strong>0.910</strong></td></tr>
              <tr><td>F1-Score</td><td><strong>0.889</strong></td></tr>
              <tr><td>Held-out Test Images</td><td>50 Images (12 Patients)</td></tr>
            </tbody>
          </table>
          <div style="margin-top: 10px; font-size: 11.5px; color: #1d4ed8; background: #eff6ff; padding: 8px 12px; border-radius: 6px;">
            <strong>Anatomical Requirement:</strong> Requires focused slit-lamp biomicroscopy illumination cutting across the crystalline lens. Diffuse external selfies are marked inconclusive.
          </div>
        </div>
      `;"""

new_cataract_modal = """    } else if (modelId === 'model_d_cataract') {
      detailsHtml += `
        <div>
          <div class="rel-modal-sec-title">👁️ Nuclear Cataract &amp; LOCS III Staging</div>
          <p>Evaluates lens opacification and nuclear cataract from anterior segment images (Cruz-Vega &amp; Ignatowicz cohorts).</p>
          <table class="rel-table" style="margin-top: 8px;">
            <thead><tr><th>Metric</th><th>Held-out Test Performance</th></tr></thead>
            <tbody>
              <tr><td>Classification Accuracy</td><td><strong>91.1%</strong> (683 / 750 Images Correct)</td></tr>
              <tr><td>Precision</td><td><strong>91.3%</strong></td></tr>
              <tr><td>Recall / Sensitivity</td><td><strong>91.1%</strong></td></tr>
              <tr><td>Specificity</td><td><strong>91.1%</strong></td></tr>
              <tr><td>F1-Score</td><td><strong>91.2%</strong></td></tr>
              <tr><td>ROC-AUC</td><td><strong>0.954</strong></td></tr>
              <tr><td>Held-out Test Images</td><td><strong>750 Images</strong></td></tr>
            </tbody>
          </table>
          <div style="margin-top: 10px; font-size: 11.5px; color: #1d4ed8; background: #eff6ff; padding: 8px 12px; border-radius: 6px;">
            <strong>Anatomical Requirement:</strong> Evaluated on clinical anterior segment photography. Focused slit-lamp biomicroscopy illumination recommended for clinical LOCS III grading.
          </div>
        </div>
      `;"""

assert old_cataract_modal in js, "old_cataract_modal not found in dashboard.js!"
js = js.replace(old_cataract_modal, new_cataract_modal, 1)

with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Successfully updated cataract modal in dashboard.js!")
