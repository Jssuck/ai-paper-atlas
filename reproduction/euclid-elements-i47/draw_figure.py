from geometry import construct
from pathlib import Path
p=construct((0,0),(3,0),(0,4))
def xy(q):return (300+q[0]*45,380-q[1]*45)
def coords(keys):return ' '.join('%g,%g'%xy(p[k]) for k in keys)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="650" viewBox="0 0 900 650">','<rect width="900" height="650" fill="white"/>','<g font-family="sans-serif" font-size="18">','<text x="30" y="32">I.47: congruent triangles transfer areas to two rectangles</text>']
for keys,color in [('ABFG','#d7e9ff'),('ACKH','#ffe1bb'),('BDLM','#d7e9ff'),('MLEC','#ffe1bb'),('ABC','#f1f5f9')]:s.append(f'<polygon points="{coords(keys)}" fill="{color}" stroke="#334155" stroke-width="2"/>')
for a,b in [('A','D'),('F','C'),('A','E'),('B','K'),('A','L')]:s.append(f'<polyline points="{coords(a+b)}" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5 4"/>')
off={'A':(-20,5),'B':(5,18),'C':(-15,-10),'D':(8,0),'E':(8,-8),'F':(8,18),'G':(-20,18),'H':(-20,0),'K':(-20,-10),'M':(-22,0),'L':(8,-3)}
for k,q in p.items():
    x,y=xy(q);dx,dy=off[k];s.append(f'<circle cx="{float(x)}" cy="{float(y)}" r="3" fill="#0f172a"/><text x="{float(x+dx)}" y="{float(y+dy)}">{k}</text>')
s+=['<text x="640" y="220">AB square = 9</text>','<text x="640" y="250">BDLM = 9</text>','<text x="640" y="300">AC square = 16</text>','<text x="640" y="330">MLEC = 16</text>','<text x="30" y="580">A=(0,0), B=(3,0), C=(0,4). M is an added foot-point label.</text>','<text x="30" y="612">Illustration only: finite coordinates are not the general proof.</text>','</g></svg>']
Path('figures').mkdir(exist_ok=True);Path('figures/area-transfer.svg').write_text('\n'.join(s));print('wrote original figures/area-transfer.svg')
