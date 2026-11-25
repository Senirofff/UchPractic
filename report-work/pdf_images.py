import pypdfium2 as pdfium,sys
from pathlib import Path
src=Path(sys.argv[1]); out=Path(sys.argv[2]);out.mkdir(exist_ok=True,parents=True)
d=pdfium.PdfDocument(src)
for i,p in enumerate(d):
 p.render(scale=1.5).to_pil().save(out/f'page-{i+1}.png')
 print(i+1,repr(p.get_textpage().get_text_range()[:120]))
