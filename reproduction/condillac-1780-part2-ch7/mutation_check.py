"""Behavioral fault injections: exceptions are errors, never kills."""
import json
import condillac_model as m


def classify(baseline, mutant, expected):
    try:
        if baseline() != expected:
            return 'invalid_baseline'
        return 'killed' if mutant() != expected else 'survived'
    except Exception:
        return 'error'


def run():
    rows = m.transfer()
    cases = [
        ('transfer_direction', lambda:m.holds(rows,7,5),lambda:m.holds((rows[0],m.R-2*m.L-3),7,5),True),
        ('distribution',lambda:2*(m.L-1),lambda:2*m.L-1,2*m.L-2),
        ('move_term_sign',lambda:rows[0],lambda:m.R-m.L+2,m.R-m.L-2),
        ('drop_conjunct',lambda:m.holds(rows,0,5),lambda:m.holds((rows[1]-rows[0],),0,5),False),
        ('sequential_reading',lambda:m.solve(rows)['point'],lambda:m.solve(m.sequential())['point'],(7,5)),
        ('rational_as_counter',lambda:m.feasible(m.q(13)/3,m.q(7)/3),lambda:True,False),
        ('zero_scale_erases_row',lambda:m.equivalent(rows,rows),lambda:m.equivalent(rows,(rows[0]*0,rows[1])),True),
        ('rounded_solution',lambda:m.solve(m.transfer(1,1,4))['point'],lambda:(4,2),(m.q(13)/3,m.q(7)/3))]
    result = {name:classify(base,mutant,expected) for name,base,mutant,expected in cases}
    print(json.dumps(result,indent=2))
    return result

if __name__ == '__main__':
    result=run()
    raise SystemExit(0 if all(x=='killed' for x in result.values()) else 1)
