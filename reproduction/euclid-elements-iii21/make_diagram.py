"""Original schematic: positions only; labels specify exact rational examples."""
from pathlib import Path
from html import escape
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480" role="img" aria-labelledby="title desc">','<title id="title">III.21: same-side equality and opposite-side supplement</title>','<desc id="desc">Three circle panels: acute angles in major segment, obtuse angles in minor segment, and opposite-side unequal supplementary angles. Blue horizontal chord is common.</desc>','<rect width="1200" height="480" fill="#fff"/>','<g font-family="sans-serif" font-size="16" fill="#142b3e">']
for cx,title,A,D,caption in [(200,'Same major segment',(0,-5),(-5,0),'cot A = cot D = 4/3'),(600,'Same minor segment',(0,5),(1.4,4.8),'cot A = cot D = -4/3'),(1000,'Opposite sides',(0,5),(0,-5),'cot A = -4/3; cot D = 4/3')]:
 def xy(p):return (cx+27*p[0],245-27*p[1])
 def line(p,q,color,width=2):
  x,y=xy(p);u,v=xy(q);return f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="{color}" stroke-width="{width}"/>'
 B,C=(-3,4),(3,4)
 parts += [f'<text x="{cx}" y="35" text-anchor="middle" font-size="22">{title}</text>',f'<circle cx="{cx}" cy="245" r="135" fill="#f6f9fc" stroke="#64748b" stroke-width="2"/>',line(B,C,'#1677b8',4)]
 for P,color in [(A,'#a93d2f'),(D,'#178250')]:parts +=[line(P,B,color),line(P,C,color)]
 for label,P in [('B',B),('C',C),('A',A),('D',D)]:
  x,y=xy(P);dx=-18 if label=='B' else 10;dy=-12 if label in ('A','D') and P[1]>4 else 21
  parts +=[f'<circle cx="{x}" cy="{y}" r="4" fill="#182e41"/>',f'<text x="{x+dx}" y="{y+dy}" font-weight="bold">{label}</text>']
 parts +=[f'<text x="{cx}" y="425" text-anchor="middle">{escape(caption)}</text>']
parts +=['<text x="600" y="465" text-anchor="middle">O=(0,0), radius=5; B=(-3,4), C=(3,4). Diagram is schematic, not a proof.</text>','</g></svg>']
Path('diagram.svg').write_text('\n'.join(parts)+'\n')
print('diagram.svg: explicit 1200 x 480')
