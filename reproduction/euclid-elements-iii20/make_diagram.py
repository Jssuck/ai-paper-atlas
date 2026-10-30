"""Illustration only: floating-point trigonometry never enters exact test oracle."""
import math
from pathlib import Path
from geometry import EXAMPLES,check
W,H=1140,700
s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc"><title id="title">III.20 same-arc cases</title><desc id="desc">Five cases: addition, subtraction, a side through the center, diameter base, and modern reflex extension. Orange marks the arc excluding A.</desc><rect width="1140" height="700" fill="#f8fafc"/><style>text{{font-family:Arial,sans-serif;fill:#0f172a}}.label{{font-size:15px}}.caption{{font-size:14px;fill:#475569}}</style><text x="30" y="34" font-size="24" font-weight="bold">III.20 · Same arc, not merely same endpoints</text><text x="30" y="58" class="caption">Orange: selected arc excludes A. Blue: inscribed rays. Dashed: radii to B and C.</text>']
labels=[('addition','1  Addition','Euclid: center inside'),('subtraction','2  Subtraction','Euclid: center outside'),('side_boundary','3  Side through center','Boundary completion'),('base_diameter','4  Base is a diameter','Straight central angle'),('reflex_extension','5  Reflex central angle','Modern extension, not original case')]
for i,(key,title,subtitle) in enumerate(labels):
 col=i%3;row=i//3;cx=190+col*380;cy=215+row*300;R=98
 def xy(p):return (cx+R*float(p[0]),cy-R*float(p[1]))
 def line(a,b,color,dash=''):
  x,y=xy(a);xx,yy=xy(b);return f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{xx:.2f}" y2="{yy:.2f}" stroke="{color}" stroke-width="2" {dash}/>'
 A,B,C=EXAMPLES[key];r=check(A,B,C)
 s += [f'<text x="{cx-155}" y="{cy-127}" font-size="18" font-weight="bold">{title}</text>',f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="white" stroke="#cbd5e1" stroke-width="2"/>']
 theta=math.atan2(float(r['central'][1]),float(r['central'][0]))%(2*math.pi);start=math.atan2(float(B[1]),float(B[0]));pts=[]
 for j in range(101):
  angle=start+r['orientation']*theta*j/100;pts.append(f'{cx+R*math.cos(angle):.2f},{cy-R*math.sin(angle):.2f}')
 s.append('<polyline points="'+' '.join(pts)+'" fill="none" stroke="#ea580c" stroke-width="6"/>')
 s += [line(A,B,'#2563eb'),line(A,C,'#2563eb'),line((0,0),B,'#64748b','stroke-dasharray="5 4"'),line((0,0),C,'#64748b','stroke-dasharray="5 4"')]
 for name,p in [('A',A),('B',B),('C',C),('O',(0,0))]:
  x,y=xy(p);s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="#0f172a"/><text x="{x+8:.2f}" y="{y-8:.2f}" class="label">{name}</text>')
 s.append(f'<text x="{cx-155}" y="{cy+132}" class="caption">{subtitle}</text>')
s.append('<text x="790" y="505" font-size="18">Exact checks use Fraction.</text><text x="790" y="534" class="caption">This drawing uses floating point only</text><text x="790" y="557" class="caption">for display; it is not a proof.</text></svg>')
Path('diagram.svg').write_text('\n'.join(s)+'\n')
