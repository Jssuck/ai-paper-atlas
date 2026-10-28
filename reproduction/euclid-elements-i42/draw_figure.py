"""Draw the exact three constructions as an original SVG; no dependencies."""
from fractions import Fraction as Q
from geometry import make_certificate
from cases import example
from pathlib import Path
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1260" height="390" viewBox="0 0 1260 390"><rect width="1260" height="390" fill="#faf9f5"/><style>text{font-family:Arial,sans-serif;font-size:17px} .small{font-size:14px}</style>']
for index,(u,title) in enumerate([(Q(-1,3),'Obtuse: F = A'),(Q(0),'Right angle'),(Q(1),'Acute: F beyond A')]):
 c=make_certificate(example(u));p={k:tuple(map(Q,v)) for k,v in c['points'].items()};p.update(A=(Q(1),Q(3)),B=(Q(0),Q(0)),C=(Q(4),Q(0)))
 def xy(v):return (index*420+65+35*float(v[0]),260-55*float(v[1]))
 def pts(keys):return ' '.join(','.join(map(str,xy(p[k]))) for k in keys)
 parts += [f'<text x="{index*420+25}" y="35">{title}</text>',f'<polygon points="{pts("FECG")}" fill="#b7dbf2" stroke="#17628e" stroke-width="2"/>',f'<polygon points="{pts("ABC")}" fill="#f0c76a" fill-opacity="0.45" stroke="#946b0a" stroke-width="2"/>',f'<line x1="{index*420+30}" y1="95" x2="{index*420+385}" y2="95" stroke="#999" stroke-dasharray="5 4"/>']
 for k in ['A','B','C','E','F','G']:
  if index==0 and k=='F':continue
  x,y=xy(p[k]);label='A = F' if index==0 and k=='A' else k
  dx,dy=(-5,24) if k in 'BCE' else (-5,-12)
  parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#263442"/><text x="{x+dx}" y="{y+dy}">{label}</text>')
 parts.append(f'<text x="{index*420+25}" y="325" class="small">B=(0,0), C=(4,0), A=(1,3), E=(2,0)</text><text x="{index*420+25}" y="350" class="small">area(ABC) = area(FECG) = 6</text>')
parts.append('</svg>');Path('figures').mkdir(exist_ok=True);Path('figures/constructions.svg').write_text('\n'.join(parts)+'\n')
print('Wrote three exact-coordinate constructions.')
