"""Original vector diagram: three projection cases and exact area differences."""
from pathlib import Path
from geometry import verify
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
<title id="title">Euclid II.13: projection cases and square-area difference</title>
<desc id="desc">Three triangles with B acute: all-acute interior foot, foot at C, and foot beyond C. Bars show BC squared plus BA squared equals AC squared plus twice BC times BD.</desc>
<rect width="1200" height="630" fill="#f7f9fc"/>
<style>text{font-family:Arial,sans-serif;fill:#182d43} .h{font-size:19px;font-weight:bold}.small{font-size:15px}.label{font-size:17px}.base{stroke:#263d52;stroke-width:2;fill:none}.tri{stroke:#184b81;stroke-width:3;fill:#dceafa;fill-opacity:.6}.alt{stroke:#c04a2a;stroke-width:2;stroke-dasharray:6 5}</style>
<text x="28" y="36" font-size="26" font-weight="bold">Euclid II.13 · the square-area shortfall</text>
<text x="28" y="65" class="label">BC² + BA² = AC² + 2BC·BD     |     B is strictly acute in every panel</text>''']
for i,(A,title,subtitle) in enumerate([((2,4),'Interior foot · original domain','All three angles acute; t = 2/5'),((5,3),'Foot at C · modern extension','Angle C right; t = 1'),((7,3),'Beyond C · modern extension','Angle C obtuse; t = 7/5')]):
    x=28+i*395; y=330; scale=40
    ax=x+A[0]*scale; ay=y-A[1]*scale; cx=x+200; dx=ax
    r=verify(A,(0,0),(5,0))
    parts.extend([f'<text x="{x}" y="105" class="h">{title}</text>',f'<text x="{x}" y="130" class="small">{subtitle}</text>',f'<path class="tri" d="M{x},{y} L{ax},{ay} L{cx},{y} Z"/>',f'<path class="base" d="M{x},{y} H{x+310}"/>',f'<path class="alt" d="M{ax},{ay} V{y}"/>',f'<path class="base" d="M{dx-10},{y} v-10 h10"/>',f'<text x="{ax-6}" y="{ay-12}" class="label">A</text>',f'<text x="{x-5}" y="{y+24}" class="label">B</text>'])
    if A[0]==5: parts.append(f'<text x="{cx-15}" y="{y+24}" class="label">C=D</text>')
    else:
        parts.extend([f'<text x="{cx-5}" y="{y+24}" class="label">C</text>',f'<text x="{dx-5}" y="{y+24}" class="label">D</text>'])
    unit=3.6
    parts.extend([f'<text x="{x}" y="385" class="label">BC² + BA² = {r["lhs"]}</text>',f'<rect x="{x}" y="397" width="{float(r["lhs"])*unit}" height="22" fill="#184b81"/>',f'<text x="{x}" y="452" class="label">AC² ({r["ac2"]}) + 2BC·BD ({r["twice_rectangle"]})</text>',f'<rect x="{x}" y="465" width="{float(r["ac2"])*unit}" height="22" fill="#739fc7"/>',f'<rect x="{x+float(r["ac2"])*unit}" y="465" width="{float(r["twice_rectangle"])*unit}" height="22" fill="#d76b40"/>'])
parts.append('''<text x="28" y="540" class="label">All area bars use the same scale. Orange = 2BC·BD, not triangle area.</text>
<text x="28" y="570" class="small">Original proof (interior division): II.7 → add AD² → I.47 twice. Other panels illustrate a modern algebraic extension.</text>
<text x="28" y="596" class="small">Interior foot alone does not imply all angles acute. Diagram coordinates: B=(0,0), C=(5,0); A=(2,4), (5,3), (7,3).</text>
</svg>''')
Path('figures').mkdir(exist_ok=True)
Path('figures/ii13-projection-cases.svg').write_text('\n'.join(parts)+'\n',encoding='utf-8')
print('Wrote original SVG: 3 projection panels, common-scale area bars.')
