import json
from geometry import *
cases=[('ordinary',[(5,0),(0,5),(-3,-4)],(0,0)),('diameter',[(5,0),(-5,0),(0,5)],(0,0)),('translated',[(7,3),(2,8),(-1,-1)],(2,3)),('rational',[(F(5,2),0),(0,F(5,2)),(F(-3,2),-2)],(0,0)),('obtuse_external',[(0,0),(4,0),(1,1)],(2,-1))]
if __name__=='__main__':
    print(json.dumps({name:make_certificate(p,d) for name,p,d in cases},indent=2))
