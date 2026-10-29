"""Original SVG built from the exact model, not copied from a source diagram."""
from geometry import construct
from pathlib import Path
p=construct()['points'];scale=62
xy=lambda n:(75+float(p[n][0])*scale,410-float(p[n][1])*scale)
def poly(names,color):
 pts=' '.join(f'{xy(n)[0]},{xy(n)[1]}' for n in names)
 return f'<polygon points="{pts}" fill="{color}" stroke="#22334a" stroke-width="2"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="700" height="500" viewBox="0 0 700 500">','<rect width="700" height="500" fill="white"/>','<text x="35" y="35" font-size="22" font-family="sans-serif">II.6 | a = 3, b = 2</text>']
for names,col in [('ACLK','#ffe8b5'),('CBHL','#ffe8b5'),('BDMH','#cfeaf5'),('HMFG','#ffe8b5'),('LHGE','#dfebd2')]:s.append(poly(names,col))
for x,y in [('A','D'),('D','E')]:
 a,b=xy(x),xy(y);s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#26374a" stroke-width="2"/>')
for n in p:
 x,y=xy(n);dx,dy=(-16,22) if n in 'ACBD' else (-19,-8)
 s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#182b44"/><text x="{x+dx}" y="{y+dy}" font-family="sans-serif" font-size="18">{n}</text>')
for x,y,t in [(150,355,'AL = 6'),(335,355,'CH = 6'),(510,355,'DM = 4'),(510,205,'HF = 6'),(335,205,'LG = 9')]:s.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="17">{t}</text>')
s.append('<text x="35" y="475" font-size="17" font-family="sans-serif">AM = CM + HF = 16; 16 + LG = 25. H lies on DE.</text></svg>')
Path('figures').mkdir(exist_ok=True);Path('figures/ii6-gnomon.svg').write_text('\n'.join(s)+'\n');print('Original figure: figures/ii6-gnomon.svg')
