"""Generate executed nbformat 4.5 tutorial with stdlib, not a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
cells=[]; ns={}
def md(s): cells.append({'cell_type':'markdown','id':f'm{len(cells)}','metadata':{},'source':s})
def code(s):
    out=io.StringIO()
    with contextlib.redirect_stdout(out): exec(compile(s,'<tutorial-cell>','exec'),ns)
    cells.append({'cell_type':'code','id':f'c{len(cells)}','metadata':{},'source':s,'execution_count':sum(c['cell_type']=='code' for c in cells)+1,'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue()}]})
md('# I.43：余形等积\n原创有理坐标教学。以下五格由标准库compile/exec真实顺序执行，非Jupyter kernel；有限运行不证明一般定理。')
code("from fractions import Fraction as Q\nfrom geometry import example,make_certificate,verify,split,area\nd=example(); c=make_certificate(d)\nprint(c['points'])")
md('两余形分别为E-B-G-K与H-K-F-D；不是只有一条线段BK、KD。')
code("print('余形面积:',c['areas']['EBGK'],c['areas']['HKFD'])\nprint('关于对角线两块:',c['areas']['AEKH'],c['areas']['KGCF'])")
md('原证接口：大三角形等积，分别减去相等的两小三角形。')
code("a=c['areas']\nprint(Q(a['ABC'])-Q(a['AEK'])-Q(a['KGC']))\nprint(Q(a['ACD'])-Q(a['AHK'])-Q(a['KFC']))")
md('离开对角线后，两补形可不等积。这只是另一网格，不是原命题的合法输入。')
code("p=split((0,0),(6,0),(0,3),Q(1,3),Q(2,3))\nprint(area([p[x] for x in 'EBGK']),area([p[x] for x in 'HKFD']))\ntry:\n make_certificate({k:p[k] for k in 'ABCDK'})\nexcept ValueError as e:\n print(type(e).__name__,str(e))")
md('证书必须绑定输入；核验器共享构造实现，独立技术审查另提供检查。')
code("print('真实证书:',verify(d,c))\nc['areas']['EBGK']='5'\nprint('篡改证书:',verify(d,c))\ntry:\n make_certificate(example(t=Q(0)))\nexcept ValueError as e:\n print('退化端点:',str(e))")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_method':'stdlib compile/exec; no Jupyter kernel'},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Generated and executed 5 code cells via compile/exec, not a kernel')
