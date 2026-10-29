"""Original SVG from exact named examples; visualization is not proof."""
from pathlib import Path
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="480" viewBox="0 0 1000 480">','<rect width="1000" height="480" fill="#fafaf8"/>','<style>text{font-family:Arial,sans-serif;fill:#172536;font-size:17px}.title{font-size:23px;font-weight:bold}.small{font-size:14px}</style>', '<text x="30" y="35" class="title">Euclid III.5: a common point is not a common center</text>']
def circle(x,y,r,color):parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{color}" stroke-width="3"/>')
def point(x,y,label,dx=6,dy=-8):parts.extend([f'<circle cx="{x}" cy="{y}" r="4" fill="#172536"/>',f'<text x="{x+dx}" y="{y+dy}" class="small">{label}</text>'])
# Scale 22px per coordinate unit, origin (205,240).
circle(139,240,110,'#127e8b');circle(271,240,110,'#c05632');point(139,240,'O1');point(271,240,'O2');point(205,152,'P=(0,4)');point(205,328,'Q=(0,-4)',6,20)
parts.append('<text x="62" y="400">Distinct circles, two common points</text>')
# Tangency scale 45px/unit
circle(480,240,45,'#127e8b');circle(570,240,45,'#c05632');point(480,240,'O1');point(570,240,'O2');point(525,240,'P',-5,-18)
parts.append('<text x="438" y="400">One common point</text>')
# Coincident circles with visual offset-free dashed overlay
circle(820,240,92,'#127e8b');parts.append('<circle cx="820" cy="240" r="92" fill="none" stroke="#c05632" stroke-width="3" stroke-dasharray="9 7"/>');point(820,240,'O1=O2');point(875.2,166.4,'P')
parts.append('<text x="724" y="400">Coincident: distinctness fails</text>')
parts.append('<text x="30" y="450" class="small">First panel: radius 5, centers (-3,0),(3,0). Other panels use independent scales. Exact tests do not measure this drawing.</text></svg>')
Path('figures').mkdir(exist_ok=True);Path('figures/common-point-centers.svg').write_text('\n'.join(parts)+'\n',encoding='utf-8');print('wrote original figures/common-point-centers.svg')
