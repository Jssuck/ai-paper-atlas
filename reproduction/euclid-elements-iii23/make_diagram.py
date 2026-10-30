"""Original schematic. Floating point only for drawing, not proof."""
import math
from pathlib import Path
from geometry import ordered_witness
def xy(p):return (280+150*float(p[0]),400-130*float(p[1]))
def arc(k):
 r=math.sqrt(1+k*k);a=math.asin(-k/r)
 return [xy((r*math.cos(a+(math.pi-2*a)*j/160),k+r*math.sin(a+(math.pi-2*a)*j/160))) for j in range(161)]
def path(ps):return 'M '+' L '.join(f'{x:.3f},{y:.3f}' for x,y in ps)
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="480" viewBox="0 0 1000 480"><rect width="1000" height="480" fill="white"/><g font-family="sans-serif" font-size="18" fill="#172b4d">','<text x="35" y="30">III.23: common base and same side</text>']
for k,color in ((1,'#2864ac'),(0,'#b95519')):
 parts.append(f'<path d="{path(arc(k))}" stroke="{color}" stroke-width="3" fill="none"/>')
A=(-1,0);B=(1,0);z=ordered_witness(0,1);C=z['C'];D=z['D']
for p,q in ((A,B),(A,D),(B,C),(B,D)):
 x,y=xy(p);u,v=xy(q);parts.append(f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="#40516c" stroke-width="2"/>')
for name,p,dx,dy in (('A',A,-20,25),('B',B,10,25),('C',C,-25,-13),('D',D,10,-10)):
 x,y=xy(p);parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#111"/><text x="{x+dx}" y="{y+dy}">{name}</text>')
for y,text in ((80,'A=(-1,0), B=(1,0)'),(120,'Inner upper arc: k=0'),(150,'Outer upper arc: k=1'),(200,'A-C-D on one ray (t=1/4)'),(235,'cot(angle ACB)=0'),(265,'cot(angle ADB)=1'),(315,'angle ACB &gt; angle ADB'),(360,'Exterior angle in triangle CBD'),(410,'Schematic only; exact values in code.')):
 parts.append(f'<text x="550" y="{y}">{text}</text>')
parts.append('</g></svg>')
Path('diagram.svg').write_text('\n'.join(parts)+'\n')
print('wrote original SVG 1000x480; plotting floats do not enter exact checks')
