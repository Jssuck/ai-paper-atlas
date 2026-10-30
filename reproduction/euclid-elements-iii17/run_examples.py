from geometry import *
def examples():
 for r,d,side in [(3,5,1),(3,5,-1),(5,13,1),(3,3,1)]:
  c=construct(r,d,side=side)
  print('r,d,side=',r,d,side,'kind=',c['kind'],'B=',str(c['B']),'verified=',verify(c),'power(t=2)=',line_power(c,2))
 for r,d in [(3,2),(1,2)]:
  try:construct(r,d)
  except ValueError as e:print('r,d=',r,d,'rejected:',str(e))
if __name__=='__main__':examples();print(grid())
