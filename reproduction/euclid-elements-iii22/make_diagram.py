"""Original explanatory drawing, not a measured proof."""
from pathlib import Path
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480" role="img" aria-label="Convex cyclic quadrilateral and crossed vertex order">','<rect width="1200" height="480" fill="white"/>','<g font-family="sans-serif" font-size="22" fill="#17243a">']
for cx,title,crossed in [(300,'Boundary order A-B-C-D',False),(900,'Crossed order: excluded',True)]:
 s.append(f'<text x="{cx}" y="38" text-anchor="middle">{title}</text><circle cx="{cx}" cy="235" r="155" fill="#f5f8ff" stroke="#94a3b8" stroke-width="2"/>')
 pts=[(cx+155,235),(cx,80),(cx-155,235),(cx,390)]
 if crossed: pts=[pts[0],pts[2],pts[1],pts[3]]
 s.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#167d93" stroke-width="4"/>')
 if not crossed:
  for i,j in [(0,2),(1,3)]:
   x,y=pts[i];u,v=pts[j];s.append(f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="#bb6b1f" stroke-width="2" stroke-dasharray="7 5"/>')
 for name,(x,y) in zip('ABCD',pts):
  dx=20 if x>cx else (-20 if x<cx else 0);dy=-18 if y<235 else (30 if y>235 else 7)
  s.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#17243a"/><text x="{x+dx}" y="{y+dy}" text-anchor="middle">{name}</text>')
 s.append(f'<text x="{cx}" y="460" text-anchor="middle" font-size="19">'+('Opposite interior angles: 90 + 90 = 180' if not crossed else 'Nonreflex opposite angles: 45 + 45 = 90')+'</text>')
s.append('</g></svg>');Path('diagram.svg').write_text('\n'.join(s)+'\n');print('Wrote original 1200 x 480 SVG')
