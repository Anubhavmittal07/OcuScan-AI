import json
from PIL import Image
from src.inference.unified_service import get_inference_service

service = get_inference_service()
img = Image.open('test_images/demo/stye.jpg').convert('RGB')
res = service.predict_unified([img], capture_source='upload')

seq = res.get('image_sequence', {})
print('--- Image Sequence ---')
for k, v in seq.items():
    if isinstance(v, dict):
        print(k, v.get('title'), v.get('dimensions'), 'has_b64:', bool(v.get('image_b64')))

print('--- Attributions per model ---')
for mod in ['anemia', 'slid', 'jaundice', 'cataract', 'stye']:
    mod_res = res.get(mod, {})
    attr = mod_res.get('attribution') or {}
    print(mod, 'attr status:', attr.get('status'), 'dims:', attr.get('dimensions'), 'has_orig_b64:', bool(attr.get('original_b64')), 'has_heatmap_b64:', bool(attr.get('heatmap_b64')), 'has_overlay_b64:', bool(attr.get('overlay_b64')))

vis = res.get('visualizations', {})
if isinstance(vis, dict):
    print('visualizations keys:', list(vis.keys()))
    for k, v in vis.items():
        if isinstance(v, dict):
            print(k, 'has_input:', bool(v.get('input')), 'has_overlay:', bool(v.get('overlay')))
