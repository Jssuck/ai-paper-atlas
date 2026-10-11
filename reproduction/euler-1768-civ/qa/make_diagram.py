"""Original point-set diagram. Python stdlib only; not a scan reproduction."""
from pathlib import Path
from xml.sax.saxutils import escape
root = Path(__file__).resolve().parents[1]
out = root / 'results'
out.mkdir(exist_ok=True)
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="1140" height="500" viewBox="0 0 1140 500" role="img" aria-labelledby="title desc">',
     '<title id="title">Same premises, three positions of C</title>',
     '<desc id="desc">A contains a, B contains a and b. C contains b, c, or both b and c. In every panel a is in B and outside C. Regions contain only the labelled points, not every geometric point.</desc>',
     '<rect width="1140" height="500" fill="#fff"/>',
     '<style>text{font-family:DejaVu Sans, sans-serif;fill:#172437}.small{font-size:17px}.body{font-size:20px}.header{font-size:26px;font-weight:bold}.region{fill:none;stroke-width:3}.A{stroke:#ac3346}.B{stroke:#576577}.C{stroke:#19709d}</style>']
def text(x,y,t,cls='body',**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    s.append(f'<text x="{x}" y="{y}" class="{cls}" {extra}>{escape(t)}</text>')
text(30,38,'Same premises, three positions of C','header')
text(30,70,'A = {a},  B = {a, b};  some A is B,  no A is C','body')
labels = ['C = {b}', 'C = {c}', 'C = {b, c}']
relations = [('All C are B',),('No C is B',),('Some C are B;', 'some C are not B')]
for k in range(3):
    o=30+380*k
    text(o+155,108,labels[k],text_anchor='middle')
    s.append(f'<rect x="{o}" y="122" width="320" height="300" rx="10" fill="#f7f9fc" stroke="#d0d6df"/>')
    text(o+10,144,'U = {a, b, c}','small')
    s.append(f'<rect x="{o+24}" y="170" width="212" height="95" rx="28" class="region B"/>')
    s.append(f'<circle cx="{o+70}" cy="220" r="28" class="region A"/>')
    text(o+48,186,'A','small')
    text(o+135,190,'B','small')
    if k==0:
        s.append(f'<circle cx="{o+185}" cy="220" r="37" class="region C"/>')
        text(o+260,217,'C','small')
    elif k==1:
        s.append(f'<circle cx="{o+185}" cy="335" r="37" class="region C"/>')
        text(o+230,332,'C','small')
    else:
        s.append(f'<ellipse cx="{o+185}" cy="277.5" rx="56" ry="102" class="region C"/>')
        text(o+249,282,'C','small')
    for label,x,y,color in [('a',o+70,220,'#ac3346'),('b',o+185,220,'#172437'),('c',o+185,335,'#172437')]:
        s.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')
        text(x+9,y+6,label,'small')
    for j,line in enumerate(relations[k]): text(o+160,395+20*j,line,'small',text_anchor='middle')
text(30,457,'In all three models: a is in B and outside C.  Therefore some B is not C.','body')
text(30,484,'Only labelled points are objects; enclosed area and circle size have no logical meaning.','small')
s.append('</svg>')
(out/'witness-three-models.svg').write_text('\n'.join(s)+'\n')
print('Created results/witness-three-models.svg (1140 x 500)')
