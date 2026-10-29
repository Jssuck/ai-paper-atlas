from geometry import verify
for name,A in [('acute triangle',(2,4)),('foot at C',(5,3)),('foot beyond C',(7,3)),('interior but obtuse A',(2,1))]:
    r=verify(A,(0,0),(5,0))
    print(f"{name}: domain={r['domain']} case={r['case']} t={r['t']} D={r['D']}")
    print(f"  BC²+BA²={r['lhs']}; AC²={r['ac2']}; 2BC·BD={r['twice_rectangle']}; checks={all(r['checks'].values())}")
