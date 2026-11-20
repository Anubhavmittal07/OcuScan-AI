import os

with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add formatPct helper right before renderReliabilityDashboard
old_render_sig = "function renderReliabilityDashboard(data) {"
new_render_sig = """function formatPct(val) {
    if (val === null || val === undefined || isNaN(val)) return 'Not Evaluated';
    return (val * 100).toFixed(1) + '%';
  }

  function renderReliabilityDashboard(data) {"""

assert old_render_sig in js, "renderReliabilityDashboard signature not found!"
js = js.replace(old_render_sig, new_render_sig, 1)

# 2. Replace lines 4430-4503 for models B, C, D, E
old_block = """    // 3. Model B: SLID Redness
    const modB = models.model_b_slid_hyperemia || {};
    if (modB.accuracy !== undefined) {
      const elAcc = document.getElementById('valRednessAcc');
      if (elAcc) elAcc.textContent = modB.accuracy.toFixed(2);
      const elPrec = document.getElementById('valRednessPrec');
      if (elPrec) elPrec.textContent = (modB.precision || 0.90).toFixed(2);
      const elRec = document.getElementById('valRednessRec');
      if (elRec) elRec.textContent = (modB.recall_sensitivity || 0.91).toFixed(2);
      const elSpec = document.getElementById('valRednessSpec');
      if (elSpec) elSpec.textContent = (modB.specificity || 0.93).toFixed(2);
      const elF1 = document.getElementById('valRednessF1');
      if (elF1) elF1.textContent = (modB.f1_score || 0.90).toFixed(2);
      const elSamples = document.getElementById('valRednessSamples');
      if (elSamples) elSamples.textContent = (modB.test_samples || 1200).toLocaleString();
    }

    // 4. Model C: Jaundice
    const modC = models.model_c_jaundice_icterus || {};
    if (modC.accuracy !== undefined) {
      const elAcc = document.getElementById('valJaundiceAcc');
      if (elAcc) elAcc.textContent = modC.accuracy.toFixed(2);
      const elPrec = document.getElementById('valJaundicePrec');
      if (elPrec) elPrec.textContent = (modC.precision || 0.82).toFixed(2);
      const elRec = document.getElementById('valJaundiceRec');
      if (elRec) elRec.textContent = (modC.recall_sensitivity || 0.80).toFixed(2);
      const elSpec = document.getElementById('valJaundiceSpec');
      if (elSpec) elSpec.textContent = (modC.specificity || 0.86).toFixed(2);
      const elF1 = document.getElementById('valJaundiceF1');
      if (elF1) elF1.textContent = (modC.f1_score || 0.81).toFixed(2);
      const elSamples = document.getElementById('valJaundiceSamples');
      if (elSamples) elSamples.textContent = (modC.test_samples || 900).toLocaleString();
    }

    // 5. Model D: Cataract
    const modD = models.model_d_cataract || {};
    if (modD.accuracy !== undefined) {
      const elAcc = document.getElementById('valCataractAcc');
      if (elAcc) elAcc.textContent = modD.accuracy.toFixed(2);
      const elPrec = document.getElementById('valCataractPrec');
      if (elPrec) elPrec.textContent = (modD.precision || 0.80).toFixed(2);
      const elRec = document.getElementById('valCataractRec');
      if (elRec) elRec.textContent = (modD.recall_sensitivity || 1.00).toFixed(2);
      const elSpec = document.getElementById('valCataractSpec');
      if (elSpec) elSpec.textContent = (modD.specificity || 0.00).toFixed(2);
      const elF1 = document.getElementById('valCataractF1');
      if (elF1) elF1.textContent = (modD.f1_score || 0.89).toFixed(2);
      const elSamples = document.getElementById('valCataractSamples');
      if (elSamples) elSamples.textContent = (modD.test_samples || 50).toLocaleString();
    }

    // 6. Model E: Stye / Hordeolum (Trained MobileNetV3 Checkpoint)
    const modE = models.model_e_stye || {};
    if (modE.accuracy !== undefined) {
      const elAcc = document.getElementById('valStyeAcc');
      if (elAcc) elAcc.textContent = modE.accuracy.toFixed(2);
      const elPrec = document.getElementById('valStyePrec');
      if (elPrec) elPrec.textContent = (modE.precision || 1.00).toFixed(2);
      const elRec = document.getElementById('valStyeRec');
      if (elRec) elRec.textContent = (modE.recall_sensitivity || 1.00).toFixed(2);
      const elSpec = document.getElementById('valStyeSpec');
      if (elSpec) elSpec.textContent = (modE.specificity || 1.00).toFixed(2);
      const elF1 = document.getElementById('valStyeF1');
      if (elF1) elF1.textContent = (modE.f1_score || 1.00).toFixed(2);
      const elSamples = document.getElementById('valStyeSamples');
      if (elSamples) elSamples.textContent = (modE.test_samples || 362).toLocaleString();
    }

    // Update all 4 classification confusion matrices dynamically with accurate values
    if (modB.confusion_matrix) updateConfusionMatrix('cmWrapRedness', modB.confusion_matrix, modB.color_max || 50);
    if (modC.confusion_matrix) updateConfusionMatrix('cmWrapJaundice', modC.confusion_matrix, modC.color_max || 40);
    if (modD.confusion_matrix) updateConfusionMatrix('cmWrapCataract', modD.confusion_matrix, modD.color_max || 50);
    if (modE.confusion_matrix) updateConfusionMatrix('cmWrapStye', modE.confusion_matrix, modE.color_max || 300);"""

new_block = """    // 3. Model B: SLID Redness
    const modB = models.model_b_slid_hyperemia || {};
    const elRedAcc = document.getElementById('valRednessAcc');
    if (elRedAcc) elRedAcc.textContent = formatPct(modB.accuracy);
    const elRedPrec = document.getElementById('valRednessPrec');
    if (elRedPrec) elRedPrec.textContent = formatPct(modB.precision);
    const elRedRec = document.getElementById('valRednessRec');
    if (elRedRec) elRedRec.textContent = formatPct(modB.recall_sensitivity);
    const elRedSpec = document.getElementById('valRednessSpec');
    if (elRedSpec) elRedSpec.textContent = formatPct(modB.specificity);
    const elRedF1 = document.getElementById('valRednessF1');
    if (elRedF1) elRedF1.textContent = formatPct(modB.f1_score);
    const elRedSamples = document.getElementById('valRednessSamples');
    if (elRedSamples) elRedSamples.textContent = (modB.test_samples || 82).toLocaleString();

    // 4. Model C: Jaundice
    const modC = models.model_c_jaundice_icterus || {};
    const elJaAcc = document.getElementById('valJaundiceAcc');
    if (elJaAcc) elJaAcc.textContent = formatPct(modC.accuracy);
    const elJaPrec = document.getElementById('valJaundicePrec');
    if (elJaPrec) elJaPrec.textContent = formatPct(modC.precision);
    const elJaRec = document.getElementById('valJaundiceRec');
    if (elJaRec) elJaRec.textContent = formatPct(modC.recall_sensitivity);
    const elJaSpec = document.getElementById('valJaundiceSpec');
    if (elJaSpec) elJaSpec.textContent = formatPct(modC.specificity);
    const elJaF1 = document.getElementById('valJaundiceF1');
    if (elJaF1) elJaF1.textContent = formatPct(modC.f1_score);
    const elJaSamples = document.getElementById('valJaundiceSamples');
    if (elJaSamples) elJaSamples.textContent = (modC.test_samples || 65).toLocaleString();

    // 5. Model D: Cataract
    const modD = models.model_d_cataract || {};
    const elCatAcc = document.getElementById('valCataractAcc');
    if (elCatAcc) elCatAcc.textContent = formatPct(modD.accuracy);
    const elCatPrec = document.getElementById('valCataractPrec');
    if (elCatPrec) elCatPrec.textContent = formatPct(modD.precision);
    const elCatRec = document.getElementById('valCataractRec');
    if (elCatRec) elCatRec.textContent = formatPct(modD.recall_sensitivity);
    const elCatSpec = document.getElementById('valCataractSpec');
    if (elCatSpec) elCatSpec.textContent = formatPct(modD.specificity);
    const elCatF1 = document.getElementById('valCataractF1');
    if (elCatF1) elCatF1.textContent = formatPct(modD.f1_score);
    const elCatSamples = document.getElementById('valCataractSamples');
    if (elCatSamples) elCatSamples.textContent = (modD.test_samples || 50).toLocaleString();

    // 6. Model E: Stye / Hordeolum (Confounded Domain Audit)
    const modE = models.model_e_stye || {};
    const elStyeAcc = document.getElementById('valStyeAcc');
    if (elStyeAcc) elStyeAcc.textContent = formatPct(modE.accuracy);
    const elStyePrec = document.getElementById('valStyePrec');
    if (elStyePrec) elStyePrec.textContent = formatPct(modE.precision);
    const elStyeRec = document.getElementById('valStyeRec');
    if (elStyeRec) elStyeRec.textContent = formatPct(modE.recall_sensitivity);
    const elStyeSpec = document.getElementById('valStyeSpec');
    if (elStyeSpec) elStyeSpec.textContent = formatPct(modE.specificity);
    const elStyeF1 = document.getElementById('valStyeF1');
    if (elStyeF1) elStyeF1.textContent = formatPct(modE.f1_score);
    const elStyeSamples = document.getElementById('valStyeSamples');
    if (elStyeSamples) elStyeSamples.textContent = modE.test_samples_note || (modE.test_samples ? `${modE.test_samples} (Confounded)` : "Not Evaluated");

    // Update classification confusion matrices dynamically with accurate values
    if (modB.confusion_matrix) updateConfusionMatrix('cmWrapRedness', modB.confusion_matrix, modB.color_max || 50);
    if (modC.confusion_matrix) updateConfusionMatrix('cmWrapJaundice', modC.confusion_matrix, modC.color_max || 40);
    if (modD.confusion_matrix) updateConfusionMatrix('cmWrapCataract', modD.confusion_matrix, modD.color_max || 50);
    if (modE.confusion_matrix) {
      updateConfusionMatrix('cmWrapStye', modE.confusion_matrix, modE.color_max || 300);
    }"""

assert old_block in js, "Old models metrics block not found in dashboard.js!"
js = js.replace(old_block, new_block, 1)

# 3. Update Stye in openModelDetailsModal
old_stye_modal = """    } else if (modelId === 'model_e_stye') {
      detailsHtml += `
        <div>
          <div class="rel-modal-sec-title">● Anterior Eyelid Hordeolum &amp; Chalazion Screening</div>
          <p>Trained and cross-validated on the Roboflow hordeolum dataset paired with normal ocular controls. 362 held-out test images evaluated across 173 unique subjects.</p>
          <table class="rel-table" style="margin-top: 8px;">
            <thead><tr><th>Metric</th><th>Held-out Test Performance</th></tr></thead>
            <tbody>
              <tr><td>Classification Accuracy</td><td><strong>100.0%</strong> (362 / 362 Images Correct)</td></tr>
              <tr><td>Sensitivity / Recall</td><td><strong>100.0%</strong> (True Positive Detection)</td></tr>
              <tr><td>Specificity</td><td><strong>100.0%</strong> (True Negative Detection)</td></tr>
              <tr><td>Precision</td><td><strong>100.0%</strong></td></tr>
              <tr><td>ROC-AUC</td><td><strong>1.000</strong></td></tr>
              <tr><td>Held-out Test Images</td><td><strong>362 Images (173 Subjects)</strong></td></tr>
            </tbody>
          </table>
          <div style="margin-top: 10px; font-size: 11.5px; color: #b45309; background: #fffbeb; padding: 8px 12px; border-radius: 6px;">
            <strong>Reliability Boundary:</strong> Evaluated on annotated external eyelid images. Prospective multi-center community trial with ophthalmologist slit-lamp confirmation required before commercial diagnostic deployment.
          </div>
        </div>
      `;"""

new_stye_modal = """    } else if (modelId === 'model_e_stye') {
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

assert old_stye_modal in js, "Old stye modal block not found in dashboard.js!"
js = js.replace(old_stye_modal, new_stye_modal, 1)

with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Successfully updated static/js/dashboard.js!")
