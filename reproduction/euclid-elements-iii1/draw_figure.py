"""Original SVG, exact geometry rendered at one common scale."""
from pathlib import Path
s=['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="500" viewBox="0 0 920 500">','<rect width="920" height="500" fill="#fff"/>','<style>text{font:16px sans-serif;fill:#182d42}.label{font-weight:bold}</style>','<text x="30" y="30">Euclid III.1: two midpoints, one recovered center</text>']
for ox,diameter in ((240,False),(690,True)):
    oy=260;scale=36
    def pt(x,y):return ox+x*scale,oy-y*scale
    s.append(f'<circle cx="{ox}" cy="{oy}" r="180" fill="#edf6fc" stroke="#1d5274" stroke-width="2"/>')
    A,B=((-5,0),(5,0)) if diameter else ((-3,4),(3,4));D=(0,0 if diameter else 4)
    x1,y1=pt(*A);x2,y2=pt(*B)
    s.append(f'<path d="M{x1},{y1} L{x2},{y2} M{ox},80 L{ox},440" fill="none" stroke="#c05c25" stroke-width="2.5"/>')
    for name,(x,y),dx,dy in [('A',A,-23,-8),('B',B,9,-8),('C',(0,5),9,-8),('E',(0,-5),9,18),('D = F' if diameter else 'F',(0,0),10,22)]+([] if diameter else [('D',D,10,-9)]):
        px,py=pt(x,y);s.append(f'<circle cx="{px}" cy="{py}" r="4" fill="#182d42"/><text class="label" x="{px+dx}" y="{py+dy}">{name}</text>')
    dx,dy=pt(*D);s.append(f'<path d="M{dx+12},{dy} v12 h-12" fill="none" stroke="#1d5274"/>')
    s.append(f'<text x="{ox-180}" y="480">'+('Diameter branch: D = F' if diameter else 'Non-diameter branch: D differs from F')+'</text>')
s.append('</svg>');Path('figures/iii1-center.svg').write_text('\n'.join(s)+'\n',encoding='utf-8');print('Original SVG written, radius 5 shown at common scale.')
