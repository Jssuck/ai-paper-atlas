"""Independent bounded checks; not a proof of kernel consistency/completeness."""
import random
from curry import *
rng=random.Random(1930)
a,b,c=map(Atom,['a','b','c'])
leaves=[B,C,W,K,a,b,c]
def gen(depth):
 if depth==0 or rng.random()<.3:return rng.choice(leaves)
 return App(gen(depth-1),gen(depth-1))
def independent_root(t):
 # Exact nested constructors; does not call library spine/root_contract.
 if isinstance(t,App) and isinstance(t.fn,App):
  u=t.fn.fn;x=t.fn.arg;y=t.arg
  if u==W:return App(App(x,y),y)
  if u==K:return x
  if isinstance(u,App):
   h=u.fn;z=u.arg
   if h==B:return App(z,App(x,y))
   if h==C:return App(App(z,y),x)
 return None
def independent_any(t):
 v=independent_root(t)
 out=[] if v is None else [v]
 if isinstance(t,App):
  out += [App(v,t.arg) for v in independent_any(t.fn)]
  out += [App(t.fn,v) for v in independent_any(t.arg)]
 return out
count=0
for i in range(1500):
 t=gen(4)
 assert parse(pretty(t))==t
 s=step(t); options=independent_any(t)
 assert (s is None)==(not options)
 if s:
  assert s.after in options
  assert check(certify_step(s))==(t,s.after)
  count+=1
for name,arity in AXIOM_ARITIES.items(): saturated_axiom_check(name,arity)
for bad in [Proof('extensionality',premises=(refl(a),)),Proof('eta'),Proof('trans',premises=(refl(a),refl(b))),Proof('axiom',('does_not_exist',)),Proof('B',(a,b))]:
 try:check(bad)
 except InvalidProof:pass
 else:raise AssertionError('malformed certificate accepted')
for t in [app(K,a,app(W,W,W)),app(I,a),app(C,a,b,c)]:
 run=normalize(t)
 assert check(certify_run(run))==(t,run.end)
print('seed=1930; 1500 random depth<=4 terms round-trip and independent redex-enumerator checks PASS')
print(f'{count} emitted steps independently recognized and certificate checked PASS')
print('16 axioms at stated symbolic arities PASS (selected p534 BW variant)')
print('5 malformed/extensionality certificates rejected PASS')
print('3 additional strategy/trace cases PASS')

# Universal proof constructors must not evaluate divergent replacement terms.
omega=parse("W W W")
assert check(right_identity_proof(omega))==(dot(omega,I),omega)
assert check(distribution_proof(omega,omega))==(app(B,dot(omega,omega)),dot(app(B,omega),app(B,omega)))
assert check(associativity_proof(omega,omega,omega))==(dot(dot(omega,omega),omega),dot(omega,dot(omega,omega)))
print('3 theorem constructors with divergent WWW arguments PASS (finite structural proofs)')
