"""Diagram uses rounded screen coordinates only; proof computations stay exact."""
from pathlib import Path
from math import sqrt
x=(sqrt(5)-1)/2
pts={'A':(0,0),'B':(1,0),'C':(0,1),'D':(1,1),'E':(0,.5),'F':(0,-x),'G':(x,-x),'H':(x,0),'K':(x,1)}
def xy(p):return (130+340*p[0],300+340*p[1])
def polygon(names,fill):
 p=' '.join(f'{xy(pts[k])[0]:.3f},{xy(pts[k])[1]:.3f}' for k in names)
 return f'<polygon points="{p}" fill="{fill}" stroke="#273449" stroke-width="2"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="700" height="780" viewBox="0 0 700 780">','<rect width="700" height="780" fill="white"/>','<text x="45" y="35" font-size="22" font-family="sans-serif">II.11: subtract the same rectangle AK</text>',polygon('FGHA','#bbdefb'),polygon('AHKC','#e4e7eb'),polygon('HBDK','#ffe0b2')]
for a,b in [('E','B'),('F','C')]:
 p,q=xy(pts[a]),xy(pts[b]);s.append(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="#667" stroke-width="2" stroke-dasharray="6 4"/>')
off={'A':(-25,-9),'B':(10,-9),'C':(-25,22),'D':(10,22),'E':(-25,5),'F':(-25,-8),'G':(10,-8),'H':(7,-10),'K':(7,22)}
for k,p in pts.items():
 X,Y=xy(p);dx,dy=off[k];s.append(f'<circle cx="{X}" cy="{Y}" r="3" fill="#172331"/><text x="{X+dx}" y="{Y+dy}" font-size="20" font-family="sans-serif">{k}</text>')
for X,Y,t in [(185,190,'FH = x²'),(180,475,'AK = ax'),(355,475,'HD = a(a-x)'),(45,705,'FK = AD; remove AK from both.'),(45,738,'Drawing rounded; algebraic checks use exact Q(sqrt(5)).')]:s.append(f'<text x="{X}" y="{Y}" font-size="18" font-family="sans-serif">{t}</text>')
s.append('</svg>');Path('figures/ii11-common-rectangle.svg').write_text('\n'.join(s)+'\n');print('wrote original SVG; rounded drawing only')
