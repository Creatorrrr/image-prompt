"""Read-only observational derivatives; keep the generated image unchanged."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ARM=Path(__file__).resolve().parent
META=json.loads((ARM/'native-result-metadata.json').read_text())
SOURCE=Path(META['project_image_path'])
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==META['image_sha256']
DEST=ARM/'review_views'
DEST.mkdir(exist_ok=True)
with Image.open(SOURCE) as im:
    assert im.size==(1024,1536)
    thumb=im.copy()
    thumb.thumbnail((320,480))
    thumb.save(DEST/'thumbnail.png')
    regions={
        'knit_and_three_layers':(354,342,739,892),
        'upper_clip_contact':(178,68,387,305),
        'lower_hand_and_cuff':(310,559,718,804),
        'upper_body_projection':(192,76,785,901),
        'lower_stance':(318,1185,845,1536),
        'skirt_boundaries':(333,790,841,1382),
    }
    for name, box in regions.items():
        im.crop(box).save(DEST/(name+'.png'))
    # Native region crops preserve one source pixel per output pixel.
    manifest={'source_image':str(SOURCE),'source_sha256':META['image_sha256'],
              'native_dimensions':list(im.size),'purpose':'pixel observation only; no generated-image edit',
              'thumbnail':{'path':str(DEST/'thumbnail.png'),'dimensions':list(thumb.size)},
              'native_regions':[{'name':n,'box_xyxy':list(b),'path':str(DEST/(n+'.png'))} for n,b in regions.items()]}
(ARM/'review-view-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==META['image_sha256']
print(json.dumps({'status':'prepared','thumbnail':manifest['thumbnail'],'native_region_count':len(regions)}))
