from pathlib import Path
from geometry import construct
from cases import BASE
P=construct(BASE)['points']
def poly(points,origin,scale):return ' '.join(f'{origin[0]+float(x)*scale},{origin[1]-float(y)*scale}'for x,y in points)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="390" viewBox="0 0 1000 390"><rect width="1000" height="390" fill="white"/><g font-family="sans-serif" font-size="18">','<text x="30" y="35">I.45: diagonal decomposition and shared-edge gluing</text>']
o=(65,300);sc=55
s.append(f'<polygon points="{poly(BASE,o,sc)}" fill="#eef4fa" stroke="#21364d" stroke-width="2"/>')
s.append(f'<polygon points="{poly([BASE[i] for i in (0,1,3)],o,sc)}" fill="#d5e9f9" stroke="#21364d"/>')
for k,(x,y)in zip('ABCD',BASE):s.append(f'<text x="{o[0]+x*sc-8}" y="{o[1]-y*sc+(-12 if y else 24)}">{k}</text>')
s.extend(['<text x="100" y="250">4</text>','<text x="220" y="205">7</text>','<text x="55" y="355">[ABD] + [DBC] = 11</text>'])
o=(520,300);sc=58
for keys,color in [('KFGH','#d5e9f9'),('HGLM','#ffe3c0')]:s.append(f'<polygon points="{poly([P[k]for k in keys],o,sc)}" fill="{color}" stroke="#21364d" stroke-width="2"/>')
for k,(x,y)in P.items():s.append(f'<text x="{o[0]+float(x)*sc-5}" y="{o[1]-float(y)*sc+(-12 if y else 24)}">{k}</text>')
s.extend(['<text x="600" y="250">4</text>','<text x="770" y="250">7</text>','<text x="500" y="355">K-H-M and F-G-L; common edge HG</text>','</g></svg>'])
Path('figures').mkdir(exist_ok=True);Path('figures/gluing.svg').write_text('\n'.join(s)+'\n');print('figures/gluing.svg generated from exact reference case')
