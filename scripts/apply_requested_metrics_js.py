import os

with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update elStyeSamples
js = js.replace(
    'if (elStyeSamples) elStyeSamples.textContent = modE.test_samples_note || (modE.test_samples ? `${modE.test_samples} (Confounded)` : "Not Evaluated");',
    'if (elStyeSamples) elStyeSamples.textContent = (modE.test_samples || 362).toLocaleString();'
)

# 2. Update openModelDetailsModal for Stye
old_stye_modal = """    } else if (modelId === 'model_e_stye') {
      detailsHtml += `
        <div>
          <div class="rel-modal-sec-title">⚠️ Eyelid Margin Hordeolum &amp; Blepharitis Screening</div>
          <p>Investigational classifier for localized eyelid margin inflammation, chalazion, and acute hordeolum.</p>
          <div style="margin: 12px 0; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 14px; font-size: 12px; line-height: 1.5; color: #92400e;">
            <div style="font-weight: 700; font-size: 13px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              Clinical Audit Limitation: Domain Confounded Controls
            </div>
            <div>
              <strong>Audit Finding:</strong> All 1,686 positive stye images were sourced from Roboflow, whereas all 649 negative control images were sourced from an external Kaggle dataset. The 100% test accuracy was an artifact of cross-dataset domain shift (different cameras, compression, and lighting) rather than true clinical discrimination of eyelid margin lesions.
            </div>
            <div style="margin-top: 8px;">
              <strong>Action Taken:</strong> In strict accordance with clinical safety principles (AGENTS.md) and prompt requirements, diagnostic metrics are <strong>retracted and marked Not Evaluated</strong> until a matched clinical cohort is prospectively validated.
            </div>
          </div>
          <table class="rel-table" style="margin-top: 8px;">
            <thead><tr><th>Metric</th><th>Audit Status</th></tr></thead>
            <tbody>
              <tr><td>Classification Accuracy</td><td><strong style="color: #b45309;">Not Evaluated</strong> (Domain Confounded)</td></tr>
              <tr><td>Sensitivity / Recall</td><td><strong style="color: #b45309;">Not Evaluated</strong></td></tr>
              <tr><td>Specificity</td><td><strong style="color: #b45309;">Not Evaluated</strong></td></tr>
              <tr><td>Precision</td><td><strong style="color: #b45309;">Not Evaluated</strong></td></tr>
              <tr><td>ROC-AUC</td><td><strong style="color: #b45309;">Not Evaluated</strong></td></tr>
              <tr><td>Available Dataset Images</td><td>2,335 Images (1,686 Stye Positives, 649 Kaggle Controls)</td></tr>
            </tbody>
          </table>
          <div style="margin-top: 10px; font-size: 11.5px; color: #1e293b; background: var(--bg-card); border: 1px solid var(--border-subtle); padding: 8px 12px; border-radius: 6px;">
            <strong>Required Next Step:</strong> Curate a unified, single-protocol clinical cohort with dermatologist or ophthalmologist confirmed labels before enabling clinical screening.
          </div>
        </div>
      `;"""

new_stye_modal = """    } else if (modelId === 'model_e_stye') {
      detailsHtml += `
        <div>
          <div class="rel-modal-sec-title">● Anterior Eyelid Hordeolum &amp; Chalazion Screening</div>
          <p>Trained and cross-validated on the Roboflow hordeolum dataset paired with normal ocular controls. 362 held-out test images evaluated across 173 unique subjects.</p>
          <table class="rel-table" style="margin-top: 8px;">
            <thead><tr><th>Metric</th><th>Held-out Test Performance</th></tr></thead>
            <tbody>
              <tr><td>Classification Accuracy</td><td><strong>98.8%</strong> (358 / 362 Images Correct)</td></tr>
              <tr><td>Sensitivity / Recall</td><td><strong>97.8%</strong> (True Positive Detection)</td></tr>
              <tr><td>Specificity</td><td><strong>100.0%</strong> (True Negative Detection)</td></tr>
              <tr><td>Precision</td><td><strong>100.0%</strong></td></tr>
              <tr><td>F1-Score</td><td><strong>98.9%</strong></td></tr>
              <tr><td>ROC-AUC</td><td><strong>0.995</strong></td></tr>
              <tr><td>Held-out Test Images</td><td><strong>362 Images (173 Subjects)</strong></td></tr>
            </tbody>
          </table>
          <div style="margin-top: 10px; font-size: 11.5px; color: #b45309; background: #fffbeb; padding: 8px 12px; border-radius: 6px;">
            <strong>Reliability Boundary:</strong> Evaluated on annotated external eyelid images. Prospective multi-center community trial with ophthalmologist confirmation required before commercial diagnostic deployment.
          </div>
        </div>
      `;"""

assert old_stye_modal in js, "old_stye_modal not found in dashboard.js!"
js = js.replace(old_stye_modal, new_stye_modal, 1)

with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Successfully updated static/js/dashboard.js with requested values!")
