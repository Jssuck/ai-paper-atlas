"""Original fixed teaching diagram; geometry is checked separately with Fractions."""
from pathlib import Path
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 610" role="img" aria-labelledby="title desc">
<title id="title">Euclid II.12: external perpendicular and positive correction</title>
<desc id="desc">An obtuse triangle ABC with A between D and C. BD is perpendicular to DC. Two rectangles of sides AC and AD represent the excess of BC squared over AB squared plus AC squared.</desc>
<rect width="960" height="610" fill="#fbfcfe"/>
<g font-family="sans-serif" fill="#17263c"><text x="40" y="42" font-size="25">II.12 · External projection, positive correction</text><text x="40" y="72" font-size="17">A=(0,0), B=(-2,3), C=(5,0); D=(-2,0)</text></g>
<path d="M 280 285 L 170 120 L 555 285 Z" fill="#e2edfc" stroke="#23476f" stroke-width="3"/>
<path d="M 170 285 L 170 120" fill="none" stroke="#23476f" stroke-width="2" stroke-dasharray="6 4"/>
<path d="M 170 285 L 280 285" stroke="#d2711b" stroke-width="5"/>
<path d="M 280 285 L 555 285" stroke="#217966" stroke-width="5"/>
<path d="M 170 265 L 190 265 L 190 285" fill="none" stroke="#354b62" stroke-width="2"/>
<g fill="#17263c" font-family="sans-serif" font-size="21"><text x="144" y="310">D</text><text x="274" y="311">A</text><text x="560" y="311">C</text><text x="147" y="108">B</text><text x="120" y="210">3</text><text x="212" y="310">2</text><text x="410" y="310">5</text><text x="620" y="150">AB² = 13</text><text x="620" y="188">AC² = 25</text><text x="620" y="226">BC² = 58</text><text x="620" y="274" fill="#b76014">58 − 13 − 25 = 20</text></g>
<g stroke="#ad6a18" stroke-width="2" fill="#fff0cb"><rect x="80" y="380" width="275" height="110"/><rect x="405" y="380" width="275" height="110"/></g>
<g fill="#17263c" font-family="sans-serif" font-size="20"><text x="197" y="370">AC = 5</text><text x="519" y="370">AC = 5</text><text x="91" y="442">AC × AD = 10</text><text x="416" y="442">AC × AD = 10</text><text x="35" y="442">2</text><text x="370" y="442">+</text><text x="713" y="442">= 20</text><text x="40" y="550">CD² = AC² + AD² + 2·AC·AD; add BD² to both sides.</text><text x="40" y="582" font-size="16">Original teaching diagram; illustrative rational instance, not a proof by measurement.</text></g>
</svg>'''
Path('figures').mkdir(exist_ok=True)
Path('figures/ii12-external-projection.svg').write_text(svg+'\n')
print('wrote figures/ii12-external-projection.svg; illustrative c=5,d=2,h=3')
