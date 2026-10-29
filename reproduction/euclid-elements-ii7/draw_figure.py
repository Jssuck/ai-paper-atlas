"""Original vector drawing; uses the exact teaching construction."""
from pathlib import Path
from geometry import construct,REGIONS
p=construct()['points'];scale=72
xy=lambda k:(100+float(p[k][0])*scale,90+float(p[k][1])*scale)
pts=lambda ns:' '.join('%g,%g'%xy(n) for n in ns)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="850" height="560" viewBox="0 0 850 560">','<rect width="850" height="560" fill="#fff"/>','<g font-family="sans-serif" font-size="18">','<text x="40" y="35" font-size="23">II.7 — overlapping rectangles and a gnomon</text>']
for region,color in [('AG','#dbeafe'),('GE','#c7d2fe'),('CF','#fbbf24'),('DG','#dcfce7')]:s.append(f'<polygon points="{pts(REGIONS[region])}" fill="{color}" stroke="#334155" stroke-width="2"/>')
s.append(f'<polyline points="{pts("DB")}" fill="none" stroke="#475569" stroke-width="2"/>')
for k in p:
 x,y=xy(k);dx,dy={'A':(-24,-10),'B':(8,-10),'C':(-6,-10),'D':(-24,24),'E':(8,24),'N':(-6,24),'H':(-24,5),'F':(8,5),'G':(7,-8)}[k]
 s.append(f'<text x="{x+dx}" y="{y+dy}">{k}</text>')
for x,y,t in [(175,160,'AG = 6'),(365,340,'GE = 6'),(340,160,'CF = 4'),(175,340,'DG = 9')]:s.append(f'<text x="{x}" y="{y}">{t}</text>')
for i,t in enumerate(['a = AC = 3; b = CB = 2','AF = top strip = 10','CE = right strip = 10','Overlap CF = 4','Union (gnomon) = 16','AF + CE = 16 + 4','Whole + CF = 25 + 4','2 AF + DG = 20 + 9','KLM names the gnomon,','not a triangle.']):s.append(f'<text x="510" y="{100+32*i}">{t}</text>')
s+=['<text x="70" y="520">Original teaching diagram; exact rational model; not an ancient source image.</text>','</g></svg>']
Path('figures').mkdir(exist_ok=True);Path('figures/ii7-overlap.svg').write_text('\n'.join(s)+'\n');print('original SVG written; CF counted twice in AF+CE')
