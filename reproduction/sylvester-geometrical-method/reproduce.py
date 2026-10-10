"""Regenerate deterministic numerical evidence and original SVG illustrations."""
from __future__ import annotations

import json
from html import escape
from math import cos, sin, sqrt
from pathlib import Path

from polynomial_certificate import certificate
from sylvester import (DomainError, Triangle, circle_chord, divider_geometry,
                       near_segment, opposite_sign_example, exact_opposite_sign_example, sine_residual,
                       tangent_ratios)

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'output'
BLUE, ORANGE, GRAY = '#146b9c', '#c76324', '#596775'


def finite_sweeps():
    reports = []
    for n in [-3, -2, -1, -.5, .5, 1, 2, 3]:
        report = {'n': n, 'angle_step_degrees': 5, 'triangles_tested': 0,
                  'degenerate_intersections': 0, 'signed_equal_isosceles': 0,
                  'signed_equal_nonisosceles': 0, 'absolute_equal_nonisosceles': 0,
                  'tolerance': 1e-10}
        for A in range(5, 180, 5):
            for B in range(5, 180 - A, 5):
                report['triangles_tested'] += 1
                try:
                    g = divider_geometry(Triangle(A, B), n)
                except DomainError:
                    report['degenerate_intersections'] += 1
                    continue
                if abs(g.t_A - g.t_B) < 1e-10:
                    key = 'signed_equal_isosceles' if A == B else 'signed_equal_nonisosceles'
                    report[key] += 1
                if A != B and abs(abs(g.t_A) - abs(g.t_B)) < 1e-10:
                    report['absolute_equal_nonisosceles'] += 1
        reports.append(report)
    return reports


def svg_header(width, height, title, description):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
            f'<title>{escape(title)}</title><desc>{escape(description)}</desc>',
            '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#152f43} .title{font-size:22px;font-weight:700}.label{font-size:17px}.small{font-size:15px}.note{font-size:14px}</style>',
            f'<rect width="{width}" height="{height}" fill="#f7fafc"/>']


def text(x, y, value, cls='label', extra=''):
    return f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" {extra}>{escape(str(value))}</text>'


def line(p, q, color=GRAY, width=2, dashed=False):
    dash = ' stroke-dasharray="7 5"' if dashed else ''
    return (f'<line x1="{p[0]:.3f}" y1="{p[1]:.3f}" x2="{q[0]:.3f}" y2="{q[1]:.3f}" '
            f'stroke="{color}" stroke-width="{width}"{dash}/>')


def geometry_svg(examples):
    svg = svg_header(1200, 950, 'Signed dividers, rays and internal cevians',
        'Four original coordinate constructions. Blue is AD; orange is BE. '
        'D and E may lie on extended sides. A negative t parameter is not on the selected ray.')
    svg += [text(28, 34, 'Same-length statements need a geometric domain', 'title'),
            text(28, 60, 'Blue: AD   Orange: BE   Gray dashed: side extensions   Dashed blue: negative line parameter', 'small')]
    titles = ['n = 2: ordinary internal bisectors', 'n = 1/2: non-isosceles, both rays forward',
              'n = -1/2: non-isosceles, both rays forward', 'n = -2: equal absolute lengths only']
    for index, g in enumerate(examples):
        ox, oy = (index % 2) * 600, 80 + (index // 2) * 425
        svg.append(f'<rect x="{ox+12}" y="{oy}" width="576" height="408" rx="12" fill="white" stroke="#d7e1e8"/>')
        svg.append(text(ox+28, oy+30, titles[index], 'label'))
        svg.append(text(ox+28, oy+55, f'A = {g.triangle.A_deg:.6g} deg, B = {g.triangle.B_deg:.8g} deg, AB = 1', 'small'))
        points = {'A': (0,0), 'B': (1,0), 'C': g.triangle.C, 'D': g.D, 'E': g.E}
        if g.t_A < 0:
            points['ray'] = (.45*cos(g.theta), .45*sin(g.theta))
        xs, ys = [p[0] for p in points.values()], [p[1] for p in points.values()]
        xmin,xmax,ymin,ymax = min(xs),max(xs),min(ys),max(ys)
        scale = min(480/max(xmax-xmin, .01), 240/max(ymax-ymin, .01))
        cx, cy = ox+300, oy+205
        def project(p):
            return (cx+(p[0]-(xmin+xmax)/2)*scale, cy-(p[1]-(ymin+ymax)/2)*scale)
        p = {name: project(value) for name,value in points.items()}
        svg += [line(p['A'],p['B'],width=2.5), line(p['A'],p['C']),line(p['B'],p['C'])]
        svg += [line(p['C'],p['D'],dashed=True),line(p['C'],p['E'],dashed=True)]
        svg += [line(p['A'],p['D'],BLUE,3,g.t_A<0),line(p['B'],p['E'],ORANGE,3,g.t_B<0)]
        if 'ray' in p:
            svg += [line(p['A'],p['ray'],BLUE,1.5), text(p['ray'][0]-15,p['ray'][1]+20,'chosen A-ray','note')]
        offsets={'A':(-22,18),'B':(7,20),'C':(-8,-13),'D':(-20,-10),'E':(9,-8)}
        if index==3:
            offsets.update({'A':(10,3),'E':(-23,18),'C':(10,-4)})
        for name in ['A','B','C','D','E']:
            x,y = p[name]
            svg.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="3.5" fill="#152f43"/>')
            dx,dy=offsets[name]
            svg.append(text(x+dx,y+dy,name))
        svg += [text(ox+28,oy+365,f'signed tA = {g.t_A:.10f}; tB = {g.t_B:.10f}','small'),
                text(ox+28,oy+390,('Internal cevians: yes' if g.both_internal_cevians else 'Internal cevians: no')+'; '+('both rays: yes' if g.both_forward_rays else 'both rays: no'),'small')]
    svg += [text(28, 946, 'Coordinate-generated original diagrams. Last panel: exact angles A=96 deg, B=24 deg give tA=-1 and tB=1.', 'note'),'</svg>']
    return '\n'.join(svg)+'\n'


def chord_svg():
    svg=svg_header(1100,590,'Two chords from the midpoint of an arc',
        'Unit circle with P=(0,1), U and V at height one half. The two chords are reflected across the vertical diameter. Near segments are blue, remote segments orange.')
    svg += [text(28,36,'Circle example: near x, remote a, half-arc chord b = PU = PV', 'title'),
            text(28,63,'P is the midpoint of the minor arc UV. The base UV cuts each chord PQ at S.', 'small')]
    def project(p):return 285+180*p[0], 302-180*p[1]
    O=project((0,0))
    svg.append(f'<circle cx="{O[0]}" cy="{O[1]}" r="180" fill="#edf5f9" stroke="#8399aa" stroke-width="2"/>')
    P,U,V=(0,1),(-sqrt(3)/2,.5),(sqrt(3)/2,.5)
    svg += [line(project(U),project(V),GRAY,2.5),line(project(P),project(U),GRAY,1.5,True),line(project(P),project(V),GRAY,1.5,True)]
    for index,angle in enumerate([-30,30],start=1):
        g=circle_chord(angle)
        svg += [line(project(g['P']),project(g['S']),BLUE,5),line(project(g['S']),project(g['Q']),ORANGE,5)]
        for name,key in [('S','S'),('Q','Q')]:
            x,y=project(g[key])
            dx=-28 if index==1 else 10
            svg.append(text(x+dx,y-8,f'{name}{index}'))
    for name,p,dx,dy in [('P',P,-7,-12),('U',U,-27,-8),('V',V,11,-8),('O',(0,0),-8,21)]:
        x,y=project(p)
        svg.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="3" fill="#152f43"/>')
        svg.append(text(x+dx,y+dy,name))
    details=[('Construction','R = 1; base y = 1/2; directions +/-30 deg'),
             ('Measured segments','x = 1/sqrt(3); a = 2/sqrt(3); b = 1'),
             ('Page 369 equation','x(x + a) = b^2'),
             ('Positive root','x = 2b^2 / (sqrt(a^2 + 4b^2) + a)'),
             ('Converse: symbols reset','near = a; remote = x; a(a + x) = b^2')]
    for index,(heading,body) in enumerate(details):
        y=122+index*79
        svg += [text(540,y,heading,'label'),text(540,y+29,body,'small')]
    svg += [text(28,550,'Blue: near segments PS1, PS2. Orange: remote segments S1Q1, S2Q2.', 'small'),
            text(28,576,'Original diagram generated by this package; no scanned source image is embedded.', 'note'),'</svg>']
    return '\n'.join(svg)+'\n'


def main():
    OUTPUT.mkdir(exist_ok=True)
    examples=[divider_geometry(Triangle(50,70),2),divider_geometry(Triangle(30,60),.5),
              divider_geometry(Triangle(15,105),-.5),exact_opposite_sign_example()]
    result={
        'scope':'Modern original reconstruction of selected equations in Sylvester 1852, pp. 367–369; not a reproduction of every historical geometric proof.',
        'limitations':['Finite sweeps are observations, not proofs of universal claims.',
                       'No result decides the universal claim that indirect proof is necessary.',
                       'Supporting-line parameters, forward rays, and internal cevians are reported separately.',
                       'Page 368 corrected special-case equations are reconstructions, not diplomatic transcriptions.'],
        'examples':[g.as_dict() for g in examples],
        'supplementary_numerical_root':opposite_sign_example().as_dict(),
        'half_case_tangent_ratios':[list(tangent_ratios(g.triangle,g.n)) for g in examples[1:3]],
        'polynomial_certificate':certificate(),
        'exact_integer_triangle_substitutions':4010,
        'finite_sweeps':finite_sweeps(),
        'chord_example':circle_chord(30),
        'root_example':{'remote_a':2,'half_chord_b':3,'near_x':near_segment(2,3)},
    }
    (OUTPUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUTPUT/'divider-domains.svg').write_text(geometry_svg(examples),encoding='utf-8')
    (OUTPUT/'equal-chords.svg').write_text(chord_svg(),encoding='utf-8')
    print('Wrote output/results.json and 2 original SVG diagrams.')
    print('Exact polynomial coefficient residual:',result['polynomial_certificate']['residual_nonzero_terms'])
    print('Grid cases:',sum(r['triangles_tested'] for r in result['finite_sweeps']))
    print('Finite observations only; no universal proof-method claim is established.')


if __name__=='__main__':main()
