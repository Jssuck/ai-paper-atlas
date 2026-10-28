"""Original diagram; paper-down y direction, r=5 and d=2."""
from pathlib import Path
from geometry import construct,verify,REGIONS
c=construct();a=verify(c);p=c['points']
def xy(name):
 x,y=p[name];return (int(380+55*x),int(90+55*y))
def poly(names):return ' '.join(f'{x},{y}' for x,y in map(xy,names))
parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 460" role="img" aria-labelledby="title desc">','<title id="title">Euclid II.5: equal complements and the missing square</title>','<desc id="desc">A C D B are collinear. C B F E is the large square. H lies on diagonal B E. Four tiles CH, DM, HF, LG have areas 6, 9, 6, 4. Rectangle AH has area 21.</desc>','<rect width="760" height="460" fill="white"/>']
for key,col in [('AL','#e5e7eb'),('CH','#93c5fd'),('DM','#fcd34d'),('HF','#93c5fd'),('LG','#bbf7d0')]:parts.append(f'<polygon points="{poly(REGIONS[key])}" fill="{col}" stroke="#111827" stroke-width="2"/>')
x1,y1=xy('B');x2,y2=xy('E');parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#be123c" stroke-width="2" fill="none"/>')
for name in p:
 x,y=xy(name);dx,dy=(-16,-12) if name in 'ACDB' else (-17,20)
 if name=='H':dx,dy=(7,-10)
 parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#111827"/><text x="{x+dx}" y="{y+dy}" font-size="18" font-family="sans-serif">{name}</text>')
for x,y,s in [(225,170,'AL = 15'),(420,170,'CH = 6'),(560,170,'DM = 9'),(420,320,'LG = 4'),(560,320,'HF = 6')]:parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="17" font-family="sans-serif">{s}</text>')
parts.append('<text x="380" y="415" text-anchor="middle" font-size="18" font-family="sans-serif">AH = AL + CH = 21; gnomon = CH + DM + HF = 21; 21 + 4 = 25</text></svg>')
Path('figures').mkdir(exist_ok=True);Path('figures/partition.svg').write_text('\n'.join(parts)+'\n');print('Original SVG written: figures/partition.svg')
