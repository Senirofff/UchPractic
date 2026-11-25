from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
from hashlib import sha256
import json
from lxml import etree
from docx import Document
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_TAB_ALIGNMENT,WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

ROOT=Path(__file__).resolve().parent
Image.open(ROOT/'02-counts.png').crop((117,755,910,1115)).save(ROOT/'02-counts-detail.png')
Image.open(ROOT/'01-catalog.png').crop((100,80,2150,1120)).save(ROOT/'01-catalog-trim.png')
REF=Path('D:/Download/Шаблон отчета.docx')
OUT=ROOT.parent/'outputs/П-8-24 Лабораторная 1 React Баранов Д.А.docx'
with ZipFile(REF) as z: original={n:z.read(n) for n in z.namelist()}
inventory={'reference':str(REF),'sha256':sha256(REF.read_bytes()).hexdigest(),'parts':{n:{'size':len(v),'sha256':sha256(v).hexdigest()} for n,v in original.items()}}
(ROOT/'package-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
d=Document(REF)
ps=list(d.paragraphs)
def replace(p,text):
 rpr=deepcopy(p.runs[0]._r.rPr) if p.runs and p.runs[0]._r.rPr is not None else None
 for e in list(p._p):
  if e.tag!=qn('w:pPr'):p._p.remove(e)
 r=p.add_run(text)
 if rpr is not None:r._r.insert(0,rpr)
 return p
for i,t in {6:'УП 01.02 «Учебная практика»',10:'Профессионального модуля ПМ.01 «Разработка модулей программного обеспечения компьютерных систем»',17:'Студент       Баранов Денис Алексеевич',20:'Группа\tП-8-24',28:'Дымская Анна Юрьевна',31:'«23» ноября 2026 года'}.items():replace(ps[i],t)
for p in ps[32:]: p._p.getparent().remove(p._p)

def para(text='',bold=False,center=False):
 p=d.add_paragraph(text)
 p.paragraph_format.widow_control=True
 if bold:
  for r in p.runs:r.bold=True
 if center:p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Cm(0)
 return p
def bookmark(p,name,id):
 a=OxmlElement('w:bookmarkStart');a.set(qn('w:id'),str(id));a.set(qn('w:name'),name)
 b=OxmlElement('w:bookmarkEnd');b.set(qn('w:id'),str(id));p._p.insert(1,a);p._p.append(b)
def heading(text,name,id,pagebreak=True,main=False):
 p=d.add_paragraph(text,style='Heading 1' if main else 'Normal')
 p.paragraph_format.page_break_before=pagebreak
 p.paragraph_format.keep_with_next=True
 if not main:
  p.paragraph_format.first_line_indent=Cm(0)
  for r in p.runs:r.bold=True
 bookmark(p,name,id)
 return p
def field(p,instruction,value):
 f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),instruction)
 r=OxmlElement('w:r');t=OxmlElement('w:t');t.text=str(value);r.append(t);f.append(r);p._p.append(f)
def toc(text,target,page):
 p=d.add_paragraph(style='toc 1');p.paragraph_format.first_line_indent=Cm(0)
 p.alignment=WD_ALIGN_PARAGRAPH.LEFT
 p.paragraph_format.tab_stops.add_tab_stop(Cm(16.35),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
 link=OxmlElement('w:hyperlink');link.set(qn('w:anchor'),target)
 r=OxmlElement('w:r');t=OxmlElement('w:t');t.text=text;r.append(t);link.append(r);p._p.append(link)
 p.add_run('\t');field(p,f' PAGEREF {target} \\h ',page)
def figure(file,caption,num,width=16):
 p=d.add_paragraph(style='Фотография');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.keep_with_next=True
 p.paragraph_format.line_spacing=1;p.paragraph_format.space_before=Pt(6)
 p.add_run().add_picture(str(ROOT/file),width=Cm(width))
 p=d.add_paragraph(style='Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 p.add_run('Рисунок ');field(p,' SEQ Рисунок \\* ARABIC ',num);p.add_run(' - '+caption)

p=para('СОДЕРЖАНИЕ',center=True);p.paragraph_format.page_break_before=True
for r in p.runs:r.font.size=Pt(16)
toc('Лабораторная работа № 1', 'lab1',3)
toc('Создание мини-приложения с карточкой товара и счётчиком','lab1',3)
steps=[('1 Подготовка проекта и подключение App','step1',3),('2 Данные товаров и вывод пяти карточек','step2',4),('3 Компонент ProductCard и передача props','step3',5),('4 Состояние useState и работа счётчика','step4',6),('5 Оформление карточек и кнопок','step5',7),('6 Адаптация для разных экранов','step6',8),('7 Проверка приложения и вывод','step7',9)]
for t,b,pg in steps:toc(t,b,pg)

heading('Лабораторная работа № 1\nСоздание мини-приложения с карточкой товара и счётчиком','lab1',10,main=True)
para('Цель работы:',True)
para('Разработать мини-приложение на React с каталогом товаров. Изучить передачу данных через props, создание повторно используемых компонентов, обработку нажатий и хранение количества с помощью useState. Подготовить выразительное оформление карточек и проверить работу интерфейса на разных размерах экрана.')
para('Требования задания:',True)
para('Компонент ProductCard должен получать название и цену через props и отображать изображение. Кнопка «Добавить в корзину» должна увеличивать количество выбранного товара, а текущее значение должно быть видно в карточке. Состояние необходимо хранить через useState. В App требуется вывести не менее пяти карточек и применить собственные стили.')
para('Ход работы:',True)
heading(steps[0][0],'step1',11,False)
para('В качестве темы выбран каталог плюшевых игрушек Neko Plush. Проект организован с использованием React и Vite. В src/main.jsx подключены App и общий файл styles.css. Метод createRoot связывает приложение с элементом root из index.html, после чего App отображается внутри React.StrictMode.')
figure('07-main.png','Подключение основного компонента и стилей',1,15)

heading(steps[1][0],'step2',12)
para('В файле src/App.jsx подготовлен массив products из пяти объектов. Для каждого товара указаны уникальный id, название name, числовая цена price и путь к изображению image. В каталог включены Венти, Арлекино, Колокольный зверь, Айзек и Макима. Цены используются как демонстрационные данные учебного приложения.')
para('Изображения размещены в public/images и доступны по путям вида /images/venti.png. Название и цена хранятся отдельно от разметки карточки. Благодаря этому ассортимент можно изменить в массиве, сохранив общий компонент и его обработчик кнопки.')
figure('04-app.png','Массив товаров и формирование карточек в App',2)
para('Внутри блока product-grid массив перебирается методом map. Для каждого объекта создаётся экземпляр ProductCard, в который передаются name, price и image. Значение product.id используется как key и позволяет React различать элементы списка. В результате один компонент формирует пять карточек с разными данными.')

heading(steps[2][0],'step3',13)
para('В файле src/components/ProductCard.jsx объявлен функциональный компонент ProductCard. Параметры name, price и image извлекаются из props при объявлении функции. Карточка оформлена элементом article. Внутри последовательно размещены фотография, название, цена, кнопка и подпись количества.')
figure('05-card.png','Исходный код компонента ProductCard',3)
para('Для фотографии значение image подставляется в src, а name включается в alt. Название выводится через h2. Цена форматируется вызовом price.toLocaleString(\'ru-RU\'), после числа добавляется знак рубля. Поэтому значение 1490 отображается как «1 490 ₽». Эти элементы одинаково устроены во всех экземплярах компонента.')

heading(steps[3][0],'step4',14)
para('Для хранения выбранного количества из React импортирован хук useState. Выражение const [quantity, setQuantity] = useState(0) создаёт состояние с начальным значением 0. quantity содержит текущее число, а setQuantity используется для его изменения. Хук вызывается внутри ProductCard, поэтому у каждой карточки имеется собственный счётчик.')
para('Кнопке назначен обработчик onClick={addToCart}. При нажатии выполняется setQuantity((current) => current + 1). Функциональная форма получает предыдущее состояние и возвращает значение на единицу больше. После обновления React повторно отображает компонент и подставляет quantity в строку «Выбрано:».')
figure('02-counts-detail.png','Независимые счётчики после добавления товаров',4,14)
para('Проверка выполнена на двух карточках. Кнопка Венти нажата три раза, кнопка Арлекино один раз. На экране получены значения 3 и 1, а у остальных товаров сохранён 0. Это подтверждает, что изменение одного экземпляра ProductCard не изменяет состояние другого.')
para('Для подписи количества задан aria-live="polite", а кнопка имеет aria-label с названием товара. Изменение количества может озвучиваться средствами чтения с экрана. В этой реализации количество хранится в памяти компонентов и сбрасывается при перезагрузке страницы. Отдельное сохранение корзины заданием не предусмотрено.')

heading(steps[4][0],'step5',15)
para('Оформление вынесено в src/styles.css. Для фона страницы выбран светлый бежевый цвет #FAF4E2, для карточек тёмно-синий #263345, для текста на карточках светлый оттенок фона. Лаймовые кнопки #C3D95D выделяют основное действие. Заголовок Neko Plush использует дополнительный приглушённый синий цвет и небольшой круглый акцент.')
figure('06-css.png','Сетка каталога и основные стили карточек',5,14)
para('Контейнер ограничен шириной 1400 px и размещён по центру страницы. Сетка CSS Grid содержит пять равных колонок с промежутком 20 px. У карточек заданы скругление 18 px, тонкая граница и тень. При наведении карточка поднимается на 5 px, а тень становится заметнее. Переход занимает 0,2 секунды.')
para('Изображения занимают всю ширину карточки и имеют соотношение сторон 3:4. Свойство object-fit: cover заполняет область с возможным кадрированием. Кнопки растянуты по ширине информационного блока и меняют цвет при наведении. Для клавиатурного фокуса предусмотрена заметная обводка. При prefers-reduced-motion анимационные переходы отключаются.')

heading(steps[5][0],'step6',16)
para('В CSS добавлены медиазапросы для перестроения каталога. При ширине окна больше 1100 px отображаются пять колонок. При ширине до 1100 px остаются три, до 720 px две, а до 480 px одна. На узком экране карточки располагаются вертикально, сохраняя название, цену, кнопку и счётчик.')
figure('03-mobile.png','Первый экран приложения при ширине 390 px',6,6.3)
para('На смартфоне боковые отступы контейнера уменьшены до 20 px, верхний и нижний отступы составляют 28 px. Проверка при ширине 390 px показала отсутствие горизонтального переполнения. Кнопка помещается внутри карточки, подпись количества доступна без горизонтальной прокрутки, а остальные товары находятся ниже по странице.')

heading(steps[6][0],'step7',17)
para('После запуска приложения проверено исходное состояние каталога. На странице отображаются пять карточек с разными фотографиями, названиями и ценами. У каждой карточки присутствует кнопка «Добавить в корзину» и начальное значение «Выбрано: 0». Все изображения загружаются; ошибок выполнения JavaScript при проверке не обнаружено.')
figure('01-catalog-trim.png','Общий вид каталога в исходном состоянии',7)
para('Проверка нажатий показала увеличение количества на единицу при каждом добавлении. После трёх нажатий на первую кнопку и одного на вторую получена последовательность 3, 1, 0, 0, 0. После перезагрузки начальные значения восстановлены. При контрольных ширинах 1000 и 650 px каталог содержит соответственно три и две колонки; при 390 px используется один столбец.')
para('Вывод:',True)
para('Создано мини-приложение Neko Plush с пятью карточками и независимыми счётчиками. Освоены передача props, вывод списка через map, обработка событий и обновление состояния через useState. Подготовлено адаптивное оформление. Проверка подтвердила выполнение требований задания.')

tmp=ROOT/'authored.docx';d.save(tmp)
with ZipFile(tmp) as z: authored={n:z.read(n) for n in z.namelist()}
# Preserve the template package; transfer only explicitly editable parts and new images.
allowed={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml','word/settings.xml'}
parts=dict(original)
for n,v in authored.items():
 if n in allowed or n not in original:parts[n]=v
settings=etree.fromstring(parts['word/settings.xml'])
upd=settings.find(qn('w:updateFields'))
if upd is None:upd=OxmlElement('w:updateFields');settings.append(upd)
upd.set(qn('w:val'),'true')
parts['word/settings.xml']=etree.tostring(settings,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(OUT,'w',ZIP_DEFLATED) as z:
 for n,v in parts.items():z.writestr(n,v)
assert all(parts[n]==v for n,v in original.items() if n not in allowed)
origsect=etree.fromstring(original['word/document.xml']).find('.//'+qn('w:sectPr'))
newsect=etree.fromstring(parts['word/document.xml']).find('.//'+qn('w:sectPr'))
assert etree.tostring(origsect)==etree.tostring(newsect)
assert inventory['sha256']==sha256(REF.read_bytes()).hexdigest()
print(OUT)
print('Preserved template parts and section geometry; seven figures and one laboratory.')
