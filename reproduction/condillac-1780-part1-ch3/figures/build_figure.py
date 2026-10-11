"""Create the original SVG diagram, using only the Python standard library.

Run from this directory: python build_figure.py
Optional PNG conversion with Pillow: python render_png.py
This visualization is not part of the core reconstruction experiment.
"""
from pathlib import Path
from html import escape

parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="510" viewBox="0 0 1100 510">',
'<rect width="1100" height="510" fill="#f6f8fc"/>',
'<style>text{font-family:DejaVu Sans,sans-serif;fill:#17223b}.title{font-size:24px;font-weight:bold}.label{font-size:22px}.small{font-size:18px}.node{fill:white;stroke:#40577a;stroke-width:2}.edge{stroke:#71819b;stroke-width:3}</style>']
def text(x,y,t,cls='label',anchor='middle'):
    parts.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(t)}</text>')
def node(x,y,t):
    parts.append(f'<circle cx="{x}" cy="{y}" r="30" class="node"/>');text(x,y+7,t)
def edge(x,y,a,b): parts.append(f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" class="edge"/>')
text(550,42,'Same leaves and operations; different structure','title')
parts.append('<line x1="550" y1="70" x2="550" y2="440" stroke="#d4dbe7" stroke-width="2"/>')
for dx,flip in [(0,False),(550,True)]:
    root=(275+dx,135); sub=(180+dx if not flip else 370+dx,240)
    leaf=(390+dx if not flip else 160+dx,240)
    a=(120+dx if not flip else 310+dx,345); b=(240+dx if not flip else 430+dx,345)
    edge(*root,*sub);edge(*root,*leaf);edge(*sub,*a);edge(*sub,*b)
    node(*root,'SUB');node(*sub,'SUB');node(*leaf,'1' if not flip else '2');node(*a,'2' if not flip else '1');node(*b,'1')
    text(275+dx,407,'(2 - 1) - 1 = 0' if not flip else '2 - (1 - 1) = 2','title')
    text(275+dx,442,'Leaf sequence: (2, 1, 1)','small')
text(550,487,'Original teaching diagram, not an illustration from Condillac.','small')
parts.append('</svg>')
Path(__file__).with_name('structure.svg').write_text('\n'.join(parts)+'\n',encoding='utf-8')
