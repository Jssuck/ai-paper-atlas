"""Independent XML metric check of the fixed original teaching example."""
from pathlib import Path
import xml.etree.ElementTree as ET
r=ET.parse('figures/ii14-equal-area.svg').getroot()
ns={'s':'http://www.w3.org/2000/svg'}
rects=r.findall('.//s:rect',ns)
geometry=[x for x in rects if x.get('stroke')]
if len(geometry)!=2:raise RuntimeError('expected two area shapes')
a,b=geometry
if (int(a.get('width')),int(a.get('height')))!=(360,160):raise RuntimeError('rectangle dimensions')
if (int(b.get('width')),int(b.get('height')))!=(240,240):raise RuntimeError('square dimensions')
if int(a.get('width'))*int(a.get('height'))!=int(b.get('width'))*int(b.get('height')):raise RuntimeError('unequal SVG areas')
expected={(60,330),(320,330),(420,330),(580,330),(420,90)}
actual={(int(x.get('cx')),int(x.get('cy'))) for x in r.findall('.//s:circle',ns)}
if actual!=expected:raise RuntimeError('construction points')
if (420-320)**2+(90-330)**2!=260**2:raise RuntimeError('H off circle')
print('PASS: rectangle 360x160 and square 240x240, equal areas 57600 px²; same 40 px/unit.')
print('PASS: B,G,E,F,H coordinates; midpoint radius 260 px and circle membership.')
print('Fixed-example XML metric check, not a general construction verifier.')
