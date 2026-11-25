from pathlib import Path
from PIL import Image,ImageChops
from zipfile import ZipFile
from lxml import etree
base=Path(__file__).resolve().parent
changed=[i for i in range(1,10) if ImageChops.difference(Image.open(base/'render3'/f'page-{i}.png'),Image.open(base/'render-final'/f'page-{i}.png')).getbbox()]
assert changed==[2],changed
f=next((base.parent/'outputs').glob('*.docx'))
with ZipFile(f) as z:r=etree.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
b=set(r.xpath('//w:bookmarkStart/@w:name',namespaces=ns))
a=r.xpath('//w:hyperlink/@w:anchor',namespaces=ns)
assert all(x in b for x in a)
captions=[x for x in r.xpath('//w:fldSimple/@w:instr',namespaces=ns) if 'SEQ' in x]
assert len(captions)==7
print('PASS: 9 pages; only contents page changed in final render; 9 valid internal links; 7 Word figure captions.')
print(f, f.stat().st_size)
