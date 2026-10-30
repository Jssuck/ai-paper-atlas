"""Original sampled SVG; floats here are display only."""
from pathlib import Path
from math import sin,cos,asin,pi
W,H=1040,460
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">', '<title id="title">III.24 equal segments before rigid placement</title>', '<desc id="desc">Two congruent major circular segments in different positions. Equal bases alone align endpoints; similarity supplies matching circular boundaries.</desc>', '<rect width="1040" height="460" fill="#fbfaf6"/>','<g font-family="sans-serif" fill="#182e42">','<text x="35" y="38" font-size="23">III.24 · equal bases + equal contained angles</text>']
def text(x,y,s,size=18): svg.append(f'<text x="{x}" y="{y}" font-size="{size}">{s}</text>')
def shape(cx,cy,angle,labels):
 a,k,R,scale=2,1.5,2.5,48
 def p(x,y):
  return cx+scale*(x*cos(angle)-y*sin(angle)),cy-scale*(x*sin(angle)+y*cos(angle))
 beta=-asin(k/R)
 pts=[p(R*cos(beta+(pi-2*beta)*j/120),k+R*sin(beta+(pi-2*beta)*j/120)) for j in range(121)]
 points=' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)
 svg.append(f'<polygon points="{points}" fill="#ccebe7" stroke="#176f72" stroke-width="3"/>')
 A,B=p(-a,0),p(a,0); P=p(1.5,3.5)
 svg.append(f'<polyline points="{A[0]},{A[1]} {P[0]},{P[1]} {B[0]},{B[1]}" fill="none" stroke="#ac6435" stroke-width="2"/>')
 for z,name in [(A,labels[0]),(B,labels[1]),(P,labels[2])]:
  svg.append(f'<circle cx="{z[0]}" cy="{z[1]}" r="4" fill="#182e42"/>');text(z[0]+8,z[1]+16,name)
shape(215,305,0,('A','B','E'))
shape(760,285,-0.35,('C','D','F'))
text(420,190,'rigid placement',18);text(440,222,'A → C, B → D',17)
text(55,360,'AB = CD = 4; cot(E) = cot(F) = 3/4',19)
text(55,397,'Different locations before placement; coincident regions after placement.',18)
text(55,430,'Original teaching coordinates; sampled drawing is not proof evidence.',15)
svg.append('</g></svg>');Path('diagram.svg').write_text('\n'.join(svg)+'\n')
print('Generated original 1040x460 SVG; floating-point display only')
