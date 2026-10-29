from pathlib import Path
from geometry import construct,verify
p=construct()['points'];verify({'points':p})
def xy(k):x,y=p[k];return float(85+65*x),float(285-65*y)
items=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 520" role="img" aria-labelledby="title desc">','<title id="title">II.10: two routes to AG squared</title>','<desc id="desc">A C B D are collinear. E is above C, F above D, G below D. E B G are collinear. The auxiliary right triangles AEG and ADG share AG.</desc>','<rect width="720" height="520" fill="#fff"/>','<text x="30" y="32" font-family="sans-serif" font-size="21">II.10: extend AB beyond B to D</text>']
def polygon(keys,fill):items.append('<polygon points="'+' '.join('%g,%g'%xy(k) for k in keys)+'" fill="'+fill+'" opacity="0.42"/>')
polygon('AEG','#b8d9ff');polygon('ADG','#ffe2b5')
for a,b,color,w in [('A','D','#334155',2),('C','E','#334155',2),('E','F','#334155',2),('F','G','#334155',2),('A','E','#2563eb',3),('E','G','#2563eb',3),('A','G','#b45309',3)]:
 x,y=xy(a);z,t=xy(b);items.append(f'<line x1="{x}" y1="{y}" x2="{z}" y2="{t}" stroke="{color}" stroke-width="{w}"/>')
# Axis-aligned right-angle marks at C, F, D, and a rotated mark at E.
for coords in [((292,285),(292,273),(280,273)),((593,90),(593,102),(605,102)),((593,285),(593,297),(605,297)),((272,98),(280,106),(288,98))]:
 items.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in coords)+'" fill="none" stroke="#475569" stroke-width="1.4"/>')
off={'A':(-20,18),'C':(-8,24),'B':(-7,24),'D':(10,8),'E':(-17,-13),'F':(10,-6),'G':(10,15)}
for k in 'ABCDEFG':
 x,y=xy(k);dx,dy=off[k];items.append(f'<circle cx="{x}" cy="{y}" r="3.8" fill="#0f172a"/><text x="{x+dx}" y="{y+dy}" font-family="sans-serif" font-size="19">{k}</text>')
items+=['<text x="30" y="470" font-family="sans-serif" font-size="17">h = 3, t = 2; AE² = 18, EG² = 50, AG² = 68</text>','<text x="30" y="496" font-family="sans-serif" font-size="16">AD² + DB² = 64 + 4 = 2(9 + 25)</text>','</svg>']
Path('figures').mkdir(exist_ok=True);Path('figures/ii10-exterior-routes.svg').write_text('\n'.join(items)+'\n')
print('Original SVG generated from verified seven-point certificate.')
