"""Generate a tutorial using nbformat 4 JSON; stdlib execution, NOT a kernel."""
import json,io,contextlib
from pathlib import Path
sections=[
('1. 精确量与适用域','from fractions import Fraction as F\nfrom geometry import certificate, CASES, grid\nprint("Fraction arithmetic; all points on one circle; no endpoint vertices")'),
('2. 同侧：优弓形的锐角与劣弓形的钝角','for name in ("same_major_segment", "same_minor_segment"):\n    print(name, certificate(*CASES[name]))'),
('3. 异侧反例及直径例外','for name in ("opposite_not_equal", "diameter_exception"):\n    print(name, certificate(*CASES[name]))'),
('4. 条件不能略去','bad = list(CASES["same_major_segment"])\nbad[4] = (0, 0)\ntry:\n    certificate(*bad)\nexcept ValueError as error:\n    print("Rejected off-circle vertex:", error)'),
('5. 有限枚举不是一般证明','print(grid())\nprint("Finite rational checks do not prove the theorem over all real points.")')]
cells=[dict(cell_type='markdown',metadata={},source=['# III.21：同弓形中的角\n','原创现代有理数教学重构，不是古代计算实验。\n','此文件的输出由标准库 compile/exec 顺序执行保存，**未启动 Jupyter kernel**。在本目录打开可重新运行。角在 (0,π) 内，cot 单射；同侧同 cot，异侧 cot 互为相反数。\n'])]
ns={'__name__':'__notebook__'}
for i,(title,code) in enumerate(sections,1):
 cells.append(dict(cell_type='markdown',metadata={},source=[title]))
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf):exec(compile(code,f'cell-{i}','exec'),ns)
 cells.append(dict(cell_type='code',metadata={},source=code.splitlines(True),execution_count=None,outputs=[dict(output_type='stream',name='stdout',text=buf.getvalue().splitlines(True))]))
nb=dict(nbformat=4,nbformat_minor=5,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python'),execution_method='stdlib compile/exec, not Jupyter kernel'),cells=cells)
for i,c in enumerate(cells):c['id']=f'iii21-{i:02d}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed and output saved; method=compile/exec; kernel=false')
