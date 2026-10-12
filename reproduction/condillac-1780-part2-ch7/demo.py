import json
import condillac_model as m

def main():
    rows = m.transfer()
    trace = m.certificate(rows,[('add',1,0,-1),('scale',1,-1),('add',0,1,1)])
    output = {
        'interpretation':'modern reconstruction; two alternative transfers from the same initial state',
        'initial_solution':m.solve(rows),
        'trace':[[[str(x.r),str(x.l),str(x.c)] for x in state] for state in trace],
        'trace_preserves_rational_solutions':all(m.equivalent(rows,state) for state in trace),
        'finite_square_0_to_12':m.oracle(rows,12),
        'derived_equation_accepts_0_5':m.holds((rows[1]-rows[0],),0,5),
        'original_accepts_0_5':m.holds(rows,0,5),
        'sequential_solution':m.solve(m.sequential()),
        'k4_rational_solution':m.solve(m.transfer(1,1,4)),
        'k4_natural_solution_in_square_0_to_12':m.oracle(m.transfer(1,1,4),12),
        'k1_positive_transfers':m.solve(m.transfer(1,1,1)),
        'k1_zero_transfers':m.solve(m.transfer(0,0,1))}
    print(json.dumps(output,ensure_ascii=False,indent=2,default=str))

if __name__ == '__main__': main()
