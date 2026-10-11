"""Rasterize this project's simple SVG with Pillow (optional figure dependency).

Tested: Pillow 12.3.0, DejaVu Sans system fonts. Run: python render_png.py
Core model/tests do not import Pillow and do not require these fonts.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).parent
im=Image.new('RGB',(1100,510),'#f6f8fc'); d=ImageDraw.Draw(im)
fonts={}
for size,bold in [(24,True),(22,False),(18,False)]:
    fonts[(size,bold)]=ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',size)
for e in ET.parse(root/'structure.svg').getroot():
    tag=e.tag.rsplit('}',1)[-1]; a=e.attrib
    if tag=='line':
        d.line(tuple(float(a[k]) for k in ['x1','y1','x2','y2']),fill=a.get('stroke','#71819b'),width=int(a.get('stroke-width',3)))
    elif tag=='circle':
        x,y,r=map(float,[a['cx'],a['cy'],a['r']]);d.ellipse((x-r,y-r,x+r,y+r),fill='white',outline='#40577a',width=2)
    elif tag=='text':
        size,bold={'title':(24,True),'label':(22,False),'small':(18,False)}[a['class']]
        d.text((float(a['x']),float(a['y'])),e.text,font=fonts[(size,bold)],fill='#17223b',anchor='ms')
im.save(root/'structure.png')
