"""Original diagram generated from verified exact coordinates; no source image copied."""
from pathlib import Path
from geometry import construct,verify,REGIONS
p=construct()['points'];verify({'points':p});scale=65;ox=70;oy=60
xy=lambda k:f'{float(p[k][0])*scale+ox:g},{float(p[k][1])*scale+oy:g}'
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="850" height="620" viewBox="0 0 850 620">','<rect width="850" height="620" fill="white"/>','<title>Elements II.8: eight cells and a completing square</title>']
for k in ('CK','KD','GR','RN','AG','MQ','QL','RF','OH'):
 color='#c8ddf0' if k in ('CK','KD','GR','RN') else '#f8d6ad' if k!='OH' else '#d5edce'
 svg.append(f'<polygon points="{" ".join(xy(n) for n in REGIONS[k])}" fill="{color}" stroke="#333" stroke-width="1.5"/>')
svg.append(f'<line x1="{ox}" y1="{oy+7*scale}" x2="{ox+7*scale}" y2="{oy}" stroke="#555" stroke-width="2"/>')
for k in p:
 x,y=map(float,p[k]);dx=8;dy=-8
 if k in ('A','M','O','E'):dx=-23
 if k in ('E','H','L','F'):dy=24
 svg.append(f'<text x="{ox+x*scale+dx:g}" y="{oy+y*scale+dy:g}" font-family="sans-serif" font-size="18">{k}</text>')
for i,(txt,col) in enumerate([('CK = KD = GR = RN = 4','#c8ddf0'),('AG = MQ = QL = RF = 6','#f8d6ad'),('OH = 9','#d5edce')]):
 y=140+65*i;svg.append(f'<rect x="570" y="{y-20}" width="20" height="20" fill="{col}"/><text x="600" y="{y-3}" font-family="sans-serif" font-size="16">{txt}</text>')
svg+=['<text x="570" y="365" font-family="sans-serif" font-size="17">AK = 10; eight cells = 40</text>','<text x="570" y="400" font-family="sans-serif" font-size="17">40 + 9 = 49</text>','<text x="70" y="580" font-family="sans-serif" font-size="17">a = AC = 3; b = BC = BD = 2. Diagonal ED passes Q and K.</text>','</svg>']
Path('figures').mkdir(exist_ok=True);Path('figures/ii8-eight-cells.svg').write_text('\n'.join(svg)+'\n');print('Original SVG written from verified coordinates.')
