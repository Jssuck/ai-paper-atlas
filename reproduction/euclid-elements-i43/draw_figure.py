"""Original I.43 teaching diagram, generated without third-party packages."""
from pathlib import Path
from fractions import Fraction as Q
from geometry import split
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="470" viewBox="0 0 1200 470">','<rect width="1200" height="470" fill="white"/>','<style>text{font-family:sans-serif;font-size:16px} .label{font-size:15px;font-weight:bold}</style>']
for j,(t,r,title) in enumerate([(Q(1,3),Q(1,3),'I.43: K on AC'),(Q(1,3),Q(2,3),'Not I.43: K off AC')]):
    ox=60+j*590; oy=350
    p=split((0,0),(6,0),(0,3),t,r)
    def xy(k): return (ox+float(p[k][0])*72,oy-float(p[k][1])*72)
    def poly(names,col):
        z=' '.join(f'{xy(k)[0]},{xy(k)[1]}' for k in names)
        s.append(f'<polygon points="{z}" fill="{col}" stroke="#394553" stroke-width="2"/>')
    s.append(f'<text x="{ox}" y="38" font-size="22">{title}</text>')
    for names,col in [('AEKH','#eeeeee'),('KGCF','#eeeeee'),('EBGK','#91c8ed'),('HKFD','#f2bf89')]: poly(names,col)
    ax,ay=xy('A'); cx,cy=xy('C')
    s.append(f'<line x1="{ax}" y1="{ay}" x2="{cx}" y2="{cy}" stroke="#bc3333" stroke-width="2" stroke-dasharray="7 5"/>')
    for k in 'ABCDEGFHK':
        x,y=xy(k); dx=-17 if k in 'ADH' else 7; dy=22 if k in 'ABE' else -8
        s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#111"/><text class="label" x="{x+dx}" y="{y+dy}">{k}</text>')
    s.append(f'<text x="{ox}" y="410">Blue EBGK: {4 if j==0 else 8}; orange HKFD: {4 if j==0 else 2}</text>')
    s.append(f'<text x="{ox}" y="438">'+('Equal area, not congruent (4 x 1 vs 2 x 2)' if j==0 else 'Fails diagonal condition; certificate rejected')+'</text>')
s.append('</svg>'); Path('figures').mkdir(exist_ok=True); Path('figures/complements.svg').write_text('\n'.join(s)+'\n')
print('Created original two-panel complements.svg')
