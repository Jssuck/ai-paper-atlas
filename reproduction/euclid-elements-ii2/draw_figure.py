from pathlib import Path
# Original schematic: A=(0,0), B=(6,0), D=(0,6), t=1/3.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="610" viewBox="0 0 720 610" role="img" aria-labelledby="title desc">
<title id="title">Euclid II.2: square ADEB partitioned at C</title><desc id="desc">A bottom left, C one third along AB, B bottom right. D top left, F above C, E top right. Blue ADFC and orange CFEB share boundary CF.</desc>
<rect width="720" height="610" fill="white"/><text x="40" y="35" font-family="sans-serif" font-size="23">II.2 — whole × first + whole × second</text>
<path d="M100 470 L100 110 L220 110 L220 470 Z" fill="#d7eafa"/><path d="M220 470 L220 110 L460 110 L460 470 Z" fill="#ffe7c2"/>
<path d="M100 470 L100 110 L460 110 L460 470 Z M220 110 L220 470" fill="none" stroke="#172b4d" stroke-width="3"/>
<g font-family="sans-serif" font-size="25" fill="#172b4d"><text x="77" y="500">A</text><text x="211" y="500">C</text><text x="460" y="500">B</text><text x="77" y="99">D</text><text x="211" y="99">F</text><text x="460" y="99">E</text><text x="135" y="280">AF</text><text x="318" y="280">CE</text></g>
<g font-family="sans-serif" font-size="19" fill="#172b4d"><text x="132" y="310">12</text><text x="318" y="310">24</text><text x="135" y="532">AC = 2</text><text x="300" y="532">CB = 4</text><text x="490" y="280">AB = AD = 6</text><text x="100" y="577">Area(ADEB) = 12 + 24 = 36</text></g></svg>'''
Path('figures').mkdir(exist_ok=True);Path('figures/partition.svg').write_text(svg+'\n');print('Wrote original schematic figures/partition.svg; coordinates and areas match integer case.')
