from geometry import inspect_triangle

def positive_cases():
    result=[]
    for scale in (1,2,3):
        for h in (-4,-2,1,3):
            for x in (-3,-1,0,1,3,5):
                A=[0,0]; B=[2*scale,0]; C=[x*scale,h*scale]
                if inspect_triangle(A,B,C)['angle_relation']==1:
                    result.append((A,B,C))
    for den in (2,3,5):
        for shift in (-2,0,3):
            for h in (2,4,6):
                result.append(([str(shift), '0'],[str(shift+1),'0'],[str(shift),f'{h+den}/{den}']))
    return result

def invalid_cases():
    return [([0,0],[0,0],[1,1]),([0,0],[1,1],[2,2]),([0,0],[1,0],[2,0]),
            ([True,0],[1,0],[0,2]),([0.0,0],[1,0],[0,2]),(['nan',0],[1,0],[0,2]),
            (['1/0',0],[1,0],[0,2]),([None,0],[1,0],[0,2]),([0],[1,0],[0,2]),
            ([0,0,0],[1,0],[0,2]),([0,0],[2,0],[1,1]),([0,0],[3,0],[0,1])]
