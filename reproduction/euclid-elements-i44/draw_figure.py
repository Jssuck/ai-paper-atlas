"""Original diagram from exact model; only its display is converted to float."""
from geometry import construct
from pathlib import Path
P=construct(3,2,6,1,1)['points']
def xy(p):return (90+(float(p[0])+5)*60,360-float(p[1])*60)
def ps(names):return ' '.join('%.1f,%.1f'%xy(P[k]) for k in names)
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="600" viewBox="0 0 1120 600">','<rect width="1120" height="600" fill="#fff"/>','<text x="40" y="45" font-family="sans-serif" font-size="24">I.44 | Apply area 6 to base AB = 3</text>',f'<polygon points="{ps("HLKF")}" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>',f'<polygon points="{ps("BEFG")}" fill="#bfdbfe" stroke="#2563eb" stroke-width="2"/>',f'<polygon points="{ps("ABML")}" fill="#fed7aa" stroke="#c2410c" stroke-width="2"/>']
for names in ['HK','AE','GM']:
 a.append(f'<polyline points="{ps(names)}" fill="none" stroke="#334155" stroke-width="2" stroke-dasharray="6 4"/>')
for k,p in P.items():
 x,y=xy(p);dx,dy={'A':(-18,22),'B':(7,22),'E':(8,22),'F':(8,-8),'G':(3,-10),'H':(-20,-10),'K':(8,24),'L':(-16,24),'M':(0,24)}[k]
 a += [f'<circle cx="{x}" cy="{y}" r="4" fill="#0f172a"/>',f'<text x="{x+dx}" y="{y+dy}" font-family="sans-serif" font-size="20">{k}</text>']
a += ['<text x="750" y="170" font-family="sans-serif" font-size="20" fill="#1d4ed8">BEFG: initial area = 6</text>','<text x="750" y="215" font-family="sans-serif" font-size="20" fill="#9a3412">ABML: applied area = 6</text>','<text x="750" y="275" font-family="sans-serif" font-size="17">H, B, K are collinear.</text>','<text x="750" y="310" font-family="sans-serif" font-size="17">F, E, K are collinear.</text>','<text x="750" y="350" font-family="sans-serif" font-size="17">Opposite rays preserve angle.</text>','<text x="40" y="565" font-family="sans-serif" font-size="16">Original coordinate teaching diagram. A rotated presentation of the source construction.</text>','</svg>']
Path('figures/application.svg').write_text('\n'.join(a)+'\n');print('figures/application.svg')
