"""Original exact-configuration teaching SVG, numeric plot only."""
from pathlib import Path
from geometry import examples,point
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="510" viewBox="0 0 1000 510"><rect width="1000" height="510" fill="#fafafa"/><style>text{font-family:Arial,sans-serif;fill:#182332;font-size:16px}.small{font-size:13px}</style>']
for n,(key,title) in enumerate([('only_AC_midpoint','One midpoint is possible'),('two_diameters','Two midpoints: center intersection')]):
    cx=250+500*n;cy=245;s=34
    def xy(p):x,y=point(p);return (cx+s*float(x),cy-s*float(y))
    c=examples()[key];z=c['input']
    parts.append(f'<text x="{cx}" y="32" text-anchor="middle">{title}</text><circle cx="{cx}" cy="{cy}" r="170" fill="#eef4fa" stroke="#8e9ba9" stroke-width="2"/>')
    for a,b,col in [('A','C','#146baf'),('B','D','#bb4d20')]:
        x1,y1=xy(z[a]);x2,y2=xy(z[b]);parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="3"/>')
    pts={k:z[k] for k in ('A','B','C','D','O')};pts['E']=c['E']
    for k,p in pts.items():
        if n==1 and k=='O':continue
        x,y=xy(p);label='E = O' if n==1 and k=='E' else k
        offsets={'A':(-20,18),'B':(5,-10),'C':(8,17),'D':(-24,16),'O':(8,20),'E':(8,20)};dx,dy=offsets[k]
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#182332"/><text x="{x+dx}" y="{y+dy}">{label}</text>')
    note='AC is bisected; BD is not. Both are non-diameters.' if n==0 else 'Both chords are diameters: outside III.4 hypotheses.'
    parts.append(f'<text class="small" x="{cx}" y="465" text-anchor="middle">{note}</text>')
parts.append('</svg>');Path('figures').mkdir(exist_ok=True);Path('figures/intersecting-chords.svg').write_text(''.join(parts),encoding='utf-8');print('original SVG created')
