import os

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update summary stats cards in index.html
html = html.replace(
    '<div class="rel-stat-value" id="statPassingEval">5</div>',
    '<div class="rel-stat-value" id="statPassingEval">4</div>'
)
html = html.replace(
    '<div class="rel-stat-sub">Held-out benchmark verified</div>\n        </div>\n        <div class="rel-stat-card">\n          <div class="rel-stat-icon icon-amber"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>\n          <div class="rel-stat-value" id="statUnderValidation">5</div>',
    '<div class="rel-stat-sub">Held-out benchmark verified</div>\n        </div>\n        <div class="rel-stat-card">\n          <div class="rel-stat-icon icon-amber"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>\n          <div class="rel-stat-value" id="statUnderValidation">1</div>'
)
html = html.replace(
    '<div class="rel-stat-value" id="statTotalTestImages">689</div>',
    '<div class="rel-stat-value" id="statTotalTestImages">327</div>'
)

# 2. Update Card 1 (Anemia) metrics formatting
html = html.replace(
    '<div class="rel-metric-row"><span class="rel-metric-label">MAE</span><span class="rel-metric-value" id="valAnemiaMae">1.50</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">RMSE</span><span class="rel-metric-value" id="valAnemiaRmse">2.07</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">R² Score</span><span class="rel-metric-value" id="valAnemiaR2">0.28</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valAnemiaSamples">130</span></div>',
    '<div class="rel-metric-row"><span class="rel-metric-label">MAE</span><span class="rel-metric-value" id="valAnemiaMae">1.50 g/dL</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">RMSE</span><span class="rel-metric-value" id="valAnemiaRmse">2.07 g/dL</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">R² Score</span><span class="rel-metric-value" id="valAnemiaR2">0.28</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valAnemiaSamples">130</span></div>'
)

# 3. Update Card 2 (Redness) metrics formatting
html = html.replace(
    '<div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valRednessAcc">0.99</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valRednessPrec">1.00</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valRednessRec">0.98</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valRednessSpec">1.00</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valRednessF1">0.99</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valRednessSamples">82</span></div>',
    '<div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valRednessAcc">98.8%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valRednessPrec">100.0%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valRednessRec">97.8%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valRednessSpec">100.0%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valRednessF1">98.9%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valRednessSamples">82</span></div>'
)

# 4. Update Card 3 (Jaundice) metrics formatting
html = html.replace(
    '<div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valJaundiceAcc">0.80</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valJaundicePrec">0.90</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valJaundiceRec">0.63</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valJaundiceSpec">0.94</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valJaundiceF1">0.75</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valJaundiceSamples">65</span></div>',
    '<div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valJaundiceAcc">80.0%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valJaundicePrec">90.5%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valJaundiceRec">63.3%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valJaundiceSpec">94.3%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valJaundiceF1">74.5%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valJaundiceSamples">65</span></div>'
)

# 5. Update Card 4 (Cataract) metrics formatting
html = html.replace(
    '<div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valCataractAcc">0.80</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valCataractPrec">0.80</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valCataractRec">1.00</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valCataractSpec">0.00</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valCataractF1">0.89</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valCataractSamples">50</span></div>',
    '<div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valCataractAcc">80.0%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valCataractPrec">80.0%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valCataractRec">100.0%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valCataractSpec">0.0%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valCataractF1">88.9%</span></div>\n            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valCataractSamples">50</span></div>'
)

# 6. Update Card 5 (Stye) to reflect Not Evaluated / Confounded Controls
old_stye_card = """        <!-- Card 5: Stye / Hordeolum (Trained MobileNetV3 Checkpoint) -->
        <div class="rel-model-card" id="cardRelStye">
          <div class="rel-model-header">
            <div class="rel-model-left">
              <div class="rel-model-icon icon-red">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                  <circle cx="15" cy="9" r="2.5" fill="#f43f5e" stroke="none"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              </div>
              <div class="rel-model-titles">
                <span class="rel-model-name">Stye (Hordeolum)</span>
              </div>
            </div>
            <span class="badge-status badge-eval" id="badgeStye">&bull; Available for Evaluation</span>
          </div>
          <p class="rel-model-desc">Detect focal eyelid margin inflammation, acute hordeolum, or chalazion from eyelid imagery.</p>
          <div class="rel-metrics-section-title">Classification Metrics</div>
          <div class="rel-metrics-list">
            <div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valStyeAcc">1.00</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valStyePrec">1.00</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valStyeRec">1.00</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valStyeSpec">1.00</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valStyeF1">1.00</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valStyeSamples">362</span></div>
          </div>
          <div class="rel-viz-box">
            <div class="rel-viz-title">Confusion Matrix</div>
            <div class="cm-container" id="cmWrapStye">
              <div class="cm-matrix-wrap">
                <div class="cm-top-labels">
                  <div class="cm-top-col-label">Normal</div>
                  <div class="cm-top-col-label">Stye</div>
                </div>
                <div class="cm-matrix-body">
                  <span class="cm-left-title">Actual</span>
                  <div class="cm-left-labels">
                    <div class="cm-left-row-label">Normal</div>
                    <div class="cm-left-row-label">Stye</div>
                  </div>
                  <div class="cm-grid-cells">
                    <div class="cm-cell cell-deep">98</div>
                    <div class="cm-cell cell-light">0</div>
                    <div class="cm-cell cell-light">0</div>
                    <div class="cm-cell cell-deep">264</div>
                  </div>
                </div>
                <div style="font-size: 10.5px; color: var(--text-muted); margin-top: 4px; font-weight: 600;">Predicted</div>
              </div>
              <div class="cm-colorbar-wrap">
                <span class="cm-colorbar-text">300</span>
                <div class="cm-colorbar"></div>
                <span class="cm-colorbar-text">0</span>
              </div>
            </div>
          </div>
        </div>"""

new_stye_card = """        <!-- Card 5: Stye / Hordeolum (Confounded Domain Audit) -->
        <div class="rel-model-card" id="cardRelStye">
          <div class="rel-model-header">
            <div class="rel-model-left">
              <div class="rel-model-icon icon-red">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                  <circle cx="15" cy="9" r="2.5" fill="#f43f5e" stroke="none"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              </div>
              <div class="rel-model-titles">
                <span class="rel-model-name">Stye (Hordeolum)</span>
              </div>
            </div>
            <span class="badge-status badge-eval" id="badgeStye" style="background:#fffbeb; color:#b45309; border:1px solid #fef3c7;">&bull; Evaluation Incomplete</span>
          </div>
          <p class="rel-model-desc">Detect focal eyelid margin inflammation, acute hordeolum, or chalazion from eyelid imagery.</p>
          <div class="rel-metrics-section-title">Classification Metrics</div>
          <div class="rel-metrics-list">
            <div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valStyeAcc" style="color: #b45309; font-weight: 600;">Not Evaluated</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valStyePrec" style="color: #b45309; font-weight: 600;">Not Evaluated</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valStyeRec" style="color: #b45309; font-weight: 600;">Not Evaluated</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valStyeSpec" style="color: #b45309; font-weight: 600;">Not Evaluated</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valStyeF1" style="color: #b45309; font-weight: 600;">Not Evaluated</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Test Samples</span><span class="rel-metric-value" id="valStyeSamples" style="font-size: 11.5px;">362 (Confounded)</span></div>
          </div>
          <div class="rel-viz-box">
            <div class="rel-viz-title">Domain Confounder Audit</div>
            <div id="cmWrapStye" style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; padding: 12px; font-size: 11px; color: #92400e; line-height: 1.45; text-align: left; min-height: 130px; display: flex; flex-direction: column; justify-content: center;">
              <div style="font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 5px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                Metrics Withheld (Audit Incomplete)
              </div>
              <div>Positives (Roboflow) and normal controls (Kaggle) originate from disjoint sources, creating cross-dataset shortcuts (artificial 100% score). Authentic clinical evaluation remains <strong>Not Evaluated</strong> until paired controls are acquired.</div>
            </div>
          </div>
        </div>"""

assert old_stye_card in html, "Old stye card not found in index.html!"
html = html.replace(old_stye_card, new_stye_card, 1)

# 7. Update table in index.html for Stye status
html = html.replace(
    '<td>Stye (Hordeolum)</td>\n                  <td>Classification</td>\n                  <td><span class="badge-status badge-eval">&bull; Available for Evaluation</span></td>',
    '<td>Stye (Hordeolum)</td>\n                  <td>Classification</td>\n                  <td><span class="badge-status badge-eval" style="background:#fffbeb; color:#b45309; border:1px solid #fef3c7;">&bull; Evaluation Incomplete</span></td>'
)

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated static/index.html!")
