"""Generate executed nbformat 4.5 tutorial with stdlib, not a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
cells=[];ns={}
def md(s):cells.append({'cell_type':'markdown','id':f'm{len(cells)}','metadata':{},'source':s})
def code(s):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(s,'<tutorial-cell>','exec'),ns)
 cells.append({'cell_type':'code','id':f'c{len(cells)}','metadata':{},'source':s,'execution_count':sum(c['cell_type']=='code' for c in cells)+1,'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue()}]})
md('# I.44：把面积施于给定底边\n五格标准库compile/exec真实执行，非Jupyter kernel。规范有理坐标模型不是尺规动作模拟器；有限运行不证明一般定理。')
code("from geometry import construct,verify,area,sub,det\nfrom fractions import Fraction as F\nc=construct(3,2,6,1,1); P=c['points']\nprint(P)")
md('先有面积为6的BEFG，再用HB与FE的延长交点K把底边改为AB=3。')
code("print('HB与HK共线:',det(sub(P['B'],P['H']),sub(P['K'],P['H']))==0)\nprint('K:',P['K'],'M:',P['M'],'L:',P['L'])")
md('I.43给出余形等积，坐标面积只是现代核验。')
code("print('BEFG面积:',area([P[k] for k in 'BEFG']))\nprint('ABML面积:',area([P[k] for k in 'ABML']))\nprint('核验:',verify(c))")
md('改变初始BE长度，最终给定底边上的结果不变；这不声称一般尺规证书完整性。')
code("d=construct(3,7,6,1,1)\nprint('最终四点相同:',all(P[k]==d['points'][k] for k in 'ABML'))")
md('错摆A或输入退化角会被拒绝；等积数值不能替代全部前提。')
code("c['points']['A']=(3,0)\nprint('错摆核验:',verify(c))\ntry:\n construct(3,2,6,1,0)\nexcept ValueError as e:\n print('退化角:',type(e).__name__)")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_method':'stdlib compile/exec; not Jupyter kernel'},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Generated and executed 5 code cells via compile/exec, not a kernel')
