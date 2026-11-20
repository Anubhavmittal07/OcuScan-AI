import os

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_metrics = """            <div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valCataractAcc">72.7%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valCataractPrec">74.6%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valCataractRec">69.7%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valCataractSpec">75.7%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valCataractF1">72.1%</span></div>"""

new_metrics = """            <div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valCataractAcc">91.1%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valCataractPrec">91.3%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valCataractRec">91.1%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valCataractSpec">91.1%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valCataractF1">91.2%</span></div>"""

old_cm = """                  <div class="cm-grid-cells">
                    <div class="cm-cell cell-deep">280</div>
                    <div class="cm-cell cell-light">90</div>
                    <div class="cm-cell cell-light">115</div>
                    <div class="cm-cell cell-deep">265</div>
                  </div>"""

new_cm = """                  <div class="cm-grid-cells">
                    <div class="cm-cell cell-deep">337</div>
                    <div class="cm-cell cell-light">33</div>
                    <div class="cm-cell cell-light">34</div>
                    <div class="cm-cell cell-deep">346</div>
                  </div>"""

assert old_metrics in html, "old_metrics not found in index.html!"
assert old_cm in html, "old_cm not found in index.html!"

html = html.replace(old_metrics, new_metrics, 1)
html = html.replace(old_cm, new_cm, 1)

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated cataract in index.html!")
