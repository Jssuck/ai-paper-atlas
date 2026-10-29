"""Original to-scale SVG for BE=9, ED=4, EH=6; no copied source image."""
from pathlib import Path
from geometry import construct
r=construct(9,4)
if r['side_squared']!=36:raise ArithmeticError('figure example')
# Cartesian (x,y) -> SVG (60+40*x,330-40*y).
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560" viewBox="0 0 900 560" role="img" aria-labelledby="title desc">
<title id="title">Euclid II.14: rectangle to equal-area square</title>
<desc id="desc">Original to-scale diagram. B=(0,0), G=(6.5,0), E=(9,0), F=(13,0), H=(9,6), D=(9,-4). Rectangle sides 9 and 4, square side 6. Semicircle radius 6.5. Square is drawn separately.</desc>
<rect width="900" height="560" fill="white"/>
<g font-family="sans-serif" font-size="17" fill="#172638">
<text x="30" y="32" font-size="22">II.14 · Same area, different shape</text>
<path d="M60 330 A260 260 0 0 1 580 330" fill="none" stroke="#3264a3" stroke-width="3"/>
<rect x="60" y="330" width="360" height="160" fill="#dceaf7" stroke="#3264a3" stroke-width="2"/>
<line x1="60" y1="330" x2="580" y2="330" stroke="#172638" stroke-width="2"/>
<line x1="420" y1="490" x2="420" y2="90" stroke="#16816a" stroke-width="3"/>
<line x1="320" y1="330" x2="420" y2="90" stroke="#b46b16" stroke-width="2"/>
<path d="M404 330 V314 H420" fill="none" stroke="#172638"/>
<g fill="#172638"><circle cx="60" cy="330" r="4"/><circle cx="320" cy="330" r="4"/><circle cx="420" cy="330" r="4"/><circle cx="580" cy="330" r="4"/><circle cx="420" cy="90" r="4"/></g>
<text x="44" y="320">B</text><text x="302" y="354">G</text><text x="427" y="354">E</text><text x="588" y="337">F</text><text x="429" y="89">H</text><text x="429" y="493">D</text>
<text x="115" y="410">Rectangle: 9 × 4 = 36</text><text x="430" y="205" fill="#16816a">EH = 6</text><text x="270" y="190" fill="#b46b16">GH = 6.5</text>
<text x="458" y="354">EF = 4</text><text x="335" y="310">GE = 2.5</text>
<rect x="630" y="190" width="240" height="240" fill="#d9f1e7" stroke="#16816a" stroke-width="3"/>
<text x="660" y="300">Square: 6² = 36</text><text x="650" y="455">Separate placement</text>
<text x="30" y="535">6.5² − 2.5² = 36 = 6² · Length scale is identical in both figures.</text>
</g></svg>'''
Path('figures').mkdir(exist_ok=True)
Path('figures/ii14-equal-area.svg').write_text(svg,encoding='utf-8')
print('SVG written: 900x560; BE=9, ED=EF=4, EH=6; 40 px/unit; square separately placed.')
