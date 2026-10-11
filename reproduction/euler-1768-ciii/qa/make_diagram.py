"""Original point-set illustration; Python standard library only."""
from pathlib import Path
from xml.etree.ElementTree import fromstring
root=Path(__file__).resolve().parents[1]
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1260" height="480" viewBox="0 0 1260 480" role="img" aria-labelledby="title desc"><title id="title">Three models, the same two premises</title><desc id="desc">A is a subset of B and C is disjoint from A in all panels. C may be outside B, inside B, or overlap B. Only the labeled dots a,b,c are objects.</desc><rect width="1260" height="480" fill="#f5f7fb"/><g font-family="DejaVu Sans, sans-serif" fill="#172b4d"><text x="35" y="40" font-size="25" font-weight="bold">Same premises. Different C-to-B relationships.</text><text x="35" y="70" font-size="17">A = {a}, B = {a,b}, U = {a,b,c}. Only the labeled dots are objects.</text>''']
for i,(title,cx,cr,cset,truth) in enumerate([
 ('C outside B',365,25,'C = {c}','All: false   None: true   Some: false   Some-not: true'),
 ('C inside B',255,25,'C = {b}','All: true   None: false   Some: true   Some-not: false'),
 ('C overlaps B',310,85,'C = {b,c}','All: false   None: false   Some: true   Some-not: true')]):
 x=i*420
 parts.append(f'<g transform="translate({x},0)"><rect x="15" y="90" width="400" height="315" rx="14" fill="white" stroke="#d2dae8"/><text x="35" y="122" font-size="19" font-weight="bold">{i+1}. {title}</text>')
 parts.append('<circle cx="190" cy="255" r="105" fill="#e7effe" stroke="#3b67a5" stroke-width="2.5"/><circle cx="135" cy="255" r="35" fill="#bdd0ee" stroke="#244d83" stroke-width="2.5"/>')
 parts.append(f'<circle cx="{cx}" cy="255" r="{cr}" fill="#a9dfcc" fill-opacity="0.38" stroke="#1b8063" stroke-width="2.5"/>')
 parts.append('<text x="175" y="178" font-size="23">B</text><text x="125" y="241" font-size="20">A</text>')
 parts.append(f'<text x="{cx-7}" y="{255-cr-10}" font-size="22" fill="#15634d">C</text>')
 for dot,dx in [('a',135),('b',255),('c',365)]:parts.append(f'<circle cx="{dx}" cy="255" r="5" fill="#15263e"/><text x="{dx-5}" y="278" font-size="18">{dot}</text>')
 parts.append(f'<text x="35" y="385" font-size="19">{cset}</text><text x="25" y="433" font-size="11.8">{truth}</text></g>')
parts.append('<text x="35" y="465" font-size="16">Each panel satisfies A subset B and C disjoint A. No one of the four C-to-B statements follows.</text></g></svg>')
s=''.join(parts);fromstring(s)
(root/'results/three-models.svg').write_text(s+'\n',encoding='utf-8');print('Generated three-models.svg; 3 panels, 9 labeled object dots; SVG XML parsed.')
