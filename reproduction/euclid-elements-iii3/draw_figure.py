"""Original SVG, equal horizontal/vertical scales in each panel."""
from pathlib import Path
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="480" viewBox="0 0 1000 480"><rect width="1000" height="480" fill="white"/><style>text{font:16px sans-serif;fill:#172b4d}.title{font-size:20px;font-weight:bold}</style>']
for cx,title,fx in ((260,'Midpoint: EF perpendicular to AB',0),(740,'Oblique: neither property holds',1)):
    cy=265;s=32
    def p(x,y): return (cx+s*x,cy-s*y)
    def line(a,b,color,width=2):
        x,y=p(*a);u,v=p(*b);parts.append(f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="{color}" stroke-width="{width}"/>')
    parts.append(f'<text class="title" x="{cx-215}" y="35">{title}</text><circle cx="{cx}" cy="{cy}" r="160" fill="#f0f6ff" stroke="#546e9c" stroke-width="2"/>')
    line((-3,4),(3,4),'#1565c0',4);line((0,0),(fx,4),'#c74e25',3);line((0,0),(-3,4),'#8590a0');line((0,0),(3,4),'#8590a0')
    for label,x,y,dx,dy in [('E',0,0,-22,20),('A',-3,4,-22,-8),('B',3,4,8,-8),('F',fx,4,5,-12)]:
        X,Y=p(x,y);parts.append(f'<circle cx="{X}" cy="{Y}" r="4" fill="#172b4d"/><text x="{X+dx}" y="{Y+dy}">{label}</text>')
    if fx==0:
        x,y=p(0,4);parts.append(f'<path d="M{x},{y+12} h12 v-12" fill="none" stroke="#c74e25" stroke-width="2"/>')
    caption='AF = FB = 3; EF = 4' if fx==0 else 'AF = 4, FB = 2; EF dot AB = 6'
    parts.append(f'<text x="{cx-160}" y="455">{caption}</text>')
parts.append('</svg>');Path('figures').mkdir(exist_ok=True);Path('figures/chord-center.svg').write_text('\n'.join(parts)+'\n')
print('Wrote original two-panel SVG with equal coordinate scales.')
