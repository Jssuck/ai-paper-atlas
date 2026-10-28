"""Original SVG from the exact model; no external assets."""
from geometry import construct
from pathlib import Path
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="480" viewBox="0 0 1000 480">','<rect width="1000" height="480" fill="white"/>','<style>text{font-family:sans-serif;font-size:18px} .edge{stroke:#25445d;stroke-width:3;fill:#d8eeef}</style>']
for j,(A,B,side,title) in enumerate([((0,0),(3,0),1,'I.46: A-D-E-B'),((0,0),(3,4),-1,'Opposite side; rotated base')]):
 p=construct(A,B,side)['points'];xs=[v[0] for v in p.values()];ys=[v[1] for v in p.values()];unit= min(340/float(max(xs)-min(xs)),310/float(max(ys)-min(ys)))
 def screen(v):return (j*500+75+float(v[0]-min(xs))*unit,405-float(v[1]-min(ys))*unit)
 q={k:screen(v) for k,v in p.items()};s.append(f'<text x="{j*500+40}" y="35">{title}</text>')
 s.append('<polygon class="edge" points="'+' '.join(f'{q[k][0]},{q[k][1]}' for k in 'ADEB')+'"/>')
 s.append(f'<path d="M {q["A"][0]} {q["A"][1]} L {q["C"][0]} {q["C"][1]}" stroke="#777" stroke-width="2" stroke-dasharray="6 5"/>')
 s.append(f'<path d="M {q["A"][0]} {q["A"][1]} L {q["B"][0]} {q["B"][1]}" stroke="#b64539" stroke-width="5"/>')
 for k,(x,y) in q.items():
  s.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#263947"/><text x="{x+9}" y="{y-8}">{k}</text>')
 s.append(f'<text x="{j*500+40}" y="455">Red: given AB. Dashed: auxiliary AC.</text>')
s.append('</svg>');Path('figures').mkdir(exist_ok=True);Path('figures/squares.svg').write_text('\n'.join(s)+'\n');print('wrote original figures/squares.svg')
