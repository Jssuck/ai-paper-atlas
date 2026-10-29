from pathlib import Path
from geometry import construct,verify
c=construct();verify(c);p=c['points']
def pos(name):
 x,y=p[name];return (60+float(x)*50,330-float(y)*50)
def poly(names):return ' '.join(','.join(map(str,pos(n))) for n in names)
a=['<svg xmlns="http://www.w3.org/2000/svg" width="680" height="450" viewBox="0 0 680 450">','<rect width="680" height="450" fill="white"/>','<text x="30" y="32" font-family="sans-serif" font-size="19">Euclid II.9 — two routes to AF² (h=5, d=2)</text>']
for ns,col in [('ACE','#dbeafe'),('EGF','#ffedd5'),('FDB','#dcfce7')]:a.append(f'<polygon points="{poly(ns)}" fill="{col}"/>')
for ns in ['AB','AE','EB','CE','DF','GF','AF']:
 x,y=pos(ns[0]);xx,yy=pos(ns[1]);a.append(f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" stroke="{"#9333ea" if ns=="AF" else "#334155"}" stroke-width="{3 if ns=="AF" else 2}"/>')
off={'A':(-20,20),'C':(-7,23),'B':(6,20),'D':(-6,23),'E':(-8,-12),'F':(10,-6),'G':(-22,-5)}
for n in p:
 x,y=pos(n);dx,dy=off[n];a.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#0f172a"/><text x="{x+dx}" y="{y+dy}" font-family="sans-serif" font-size="18">{n}</text>')
a+=['<text x="45" y="392" font-family="sans-serif" font-size="16">AE² + EF² = 50 + 8 = 58 = AD² + DF² = 49 + 9</text>','<text x="45" y="421" font-family="sans-serif" font-size="14">Original teaching diagram; exact coordinates checked by geometry.py.</text>','</svg>']
Path('figures').mkdir(exist_ok=True);Path('figures/ii9-two-routes.svg').write_text('\n'.join(a)+'\n');print('SVG generated from verified seven-point certificate')
