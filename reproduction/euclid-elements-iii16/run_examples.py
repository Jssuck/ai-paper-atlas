from geometry import *
def examples():
 c=Circle((0,5),25)
 for label,u in [('tangent',(1,0)),('inward',(3,4)),('outward',(3,-4)),('diameter',(0,1))]:
  a=analyze(c,(0,0),u);print(label, 'k=',a['k'],'second=',a['second_parameter'],'foot=',a['foot'],'power=',a['interior_power'])
 for n in [1,10,1000000]:
  a=narrow_example(n);print('narrow',n,'interior t=',a['interior_parameter'],'power=',a['interior_power'])
 for p,u in [((0,1),(1,1)),((0,0),(0,0))]:
  try:analyze(c,p,u)
  except ValueError as e:print('rejected:',str(e))
if __name__=='__main__':examples()
