from docx import Document
from zipfile import ZipFile
from lxml import etree
from pathlib import Path
for name in ['Шаблон отчета.docx','П-8-24 УП 01.02 Баранов Д.А.docx']:
 d=Document('D:/Download/'+name)
 print('\nFILE',name)
 for i,s in enumerate(d.sections):
  print('SECTION',i,[(x,str(getattr(s,x))) for x in ['page_width','page_height','top_margin','bottom_margin','left_margin','right_margin','header_distance','footer_distance']])
 for i,p in enumerate(d.paragraphs):
  print(i,p.style.name,repr(p.text), 'align',p.alignment,'size',[(r.font.name,r.font.size.pt if r.font.size else None,r.bold) for r in p.runs[:2]])
 for t in d.tables:
  print('TABLE',[[c.text for c in row.cells] for row in t.rows])
 with ZipFile('D:/Download/'+name) as z:
  for n in z.namelist():
   if n.startswith('word/header') or n.startswith('word/footer'):
    print(n,z.read(n).decode()[:5000])
 for st in ['Normal','Heading 1','Heading 2','Caption','Title']:
  s=d.styles[st] if st in d.styles else None; print('STYLE',st,s.element.xml if s else 'ABSENT')

