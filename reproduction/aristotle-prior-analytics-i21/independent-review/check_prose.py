"""Independent explicit checks of article's concrete configurations."""
from check import oracle,check
cases=[
 ('section6',((3,3,1),(2,3,1)),[(('C','a','A','C'),True),(('D','a','B','C'),True),(('C','i','A','B'),True),(('C','o','A','B'),True),(('P','o','A','B'),True),(('D','o','A','B'),False)]),
 ('section7_1',((1,2,1),(1,1,1)),[(('D','a','A','C'),True),(('C','a','B','C'),True),(('P','i','A','B'),False),(('C','i','A','B'),False),(('C','i','C','B'),False)]),
 ('section7_2',((2,2,1),(3,1,1)),[(('D','e','A','C'),True),(('C','a','B','C'),True),(('P','o','A','B'),False)]),
 ('section7_3_instance',((1,2,1),(1,2,1)),[(('P','o','A','B'),True),(('C','o','A','B'),False),(('N','a','A','B'),False)]),
 ('section8',((1,2,3),(1,1,3)),[(('D','i','A','C'),True),(('C','i','B','C'),True),(('P','i','A','B'),False)]),
 ('section6_single_world',((3,3,1),),[(('C','a','A','C'),False)])]
for name,ws,claims in cases:
 for query,expected in claims:check(oracle(2,ws,*query)==expected,name+str(query))
print('PASS:',len(cases),'article configurations;',sum(len(x[2]) for x in cases),'claims')
