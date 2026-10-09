"""Fill the official tutorial scaffold with a compact Chinese walkthrough."""
import json
from pathlib import Path
path = Path('turing_teaching.zh-CN.ipynb')
nb = json.loads(path.read_text())
cells = []
def add(kind, source):
    cell = dict(cell_type=kind, id=f'turing-{len(cells):02d}', metadata={},
                source=source.strip().splitlines(keepends=True))
    if kind == 'code': cell.update(execution_count=None, outputs=[])
    cells.append(cell)
md = lambda text: add('markdown', text)
code = lambda text: add('code', text)
md('''# 图灵计算模型：从一步转移到有限观察的边界

面向：理解明确步骤、可阅读基础 Python 的初学者。目标：读懂一次转移；区分运行步数和结果位数；解释超时的局限；区分运行证据、规则归纳和一般定理。

路线：模型 → 手算与代码 → 两种输出行为 → 延迟实验 → 有限枚举 → 自测。

**边界**：这是现代教学转导器。它不是原文完整通用机，也不是不可判定性定理的“实验验证”。代码和 README 与本 notebook 放在同一目录。无随机过程，无训练集，无依赖下载。

**实际核验方式**：当前环境没有 nbformat、nbclient 或 ipykernel。所有代码单元已用随附标准库校验器，在一个新 Python 进程中按顺序执行；显示的 stdout 来自该校验，不是 Jupyter 内核执行记录。真正的 Jupyter 打开、内核执行和界面渲染尚未验证。''')
md('''## 1. 先把“机器”说清楚

完整配置由状态 q、读头整数位置 h、工作带 τ 和已观察到的输出 o 构成。工作带初始全空白 `_`，读头从0开始。

δ(q,a)=(q′,b,d,e)：读 a，写 b，移动 d∈{−1,0,1}，切换 q′，追加 e∈{空,0,1}。

`emit` 是现代输出标记，机器不能读回输出。输出历史不是另一条可读工作带。没有适用规则才停止；预算耗尽只返回 `cap_reached`。

源码原始依据：[原论文第1–3节，231–234页](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf)。逐字历史通用机和其编码机制不在本复现范围内。''')
code('''import sys
from simulator import (run, alternating, alternating_spaced, one_then_silent,
                       delayed_forever, silent_forever, enumerate_one_state)
print('Python:', sys.version.split()[0])
print('模型：单工作带 + 只写不读的输出观察记录')''')
md('''## 2. 先手算，再看状态表

两条规则：a 读空白 → 写0、右移、转 b、输出0；b 读空白 → 写1、右移、转 a、输出1。

请先预测：第0步状态 a、位置0；第1步应该是什么？第2步呢？

预期：输出前缀是010101；读头永远来到未访问的空白格。''')
code('''case = run(alternating(), 6)
print('step state head scanned emitted output tape')
for row in case['trace']:
    print(row['step'], row['state'], row['head'], row['scanned'],
          row['emitted'] or 'ε', row['output'] or 'ε', row['tape'])
assert case['output'] == '010101'
print('状态:', case['status'])''')
md('''**读表**：输出010101是已经观察到的事实。“无限输出”还需要另一层论证：每一步都右移到新空白格，状态交替，适用规则永远存在且每次输出一位。以步数作归纳即可证明。

由模型还可得到 |h_t|≤t、非空白格数≤t、输出长度≤t。前两者来自一次只能移动一格、改写一格；第三者来自一次至多输出一位。''')
md('''## 3. 历史布局与教学简化

对齐原文交替例的版本有四阶段，结果位之间保留空白格。状态名称被规范化，不是原文字符的逐字抄录。比较输出相同，不表示步数和内部配置相同。''')
code('''spaced = run(alternating_spaced(), 12)
print('6步简化版:', case['output'])
print('12步间隔版:', spaced['output'])
print('间隔版非空白格:', spaced['trace'][-1]['tape'])
assert spaced['output'] == case['output']
assert set(spaced['trace'][-1]['tape']) == {'0', '2', '4', '6', '8', '10'}''')
md('''## 4. 不停机不等于不断输出

新机器 first 先打印并输出一个0，之后 silent 只右移，不再输出。先预测12步后有几位结果，再运行。''')
code('''finite_output = run(one_then_silent(), 12)
print('已执行步数:', finite_output['steps'])
print('累计输出:', repr(finite_output['output']))
print('末状态:', finite_output['trace'][-1]['state'])
print('读头位置:', finite_output['trace'][-1]['head'])
assert finite_output['output'] == '0'
assert finite_output['status'] == 'cap_reached' ''')
md('''**解释**：12步日志只显示到第12步。规则本身则保证第一步后永远右移且不再输出。因此它不停机，但结果位总数为1，属于这里沿用输出判据的 circular。

“状态 silent 重复”本身不等于完整配置重复，因为读头位置每步改变。无限运行判断依赖具体规则的归纳，不能仅看状态名重复。''')
md('''## 5. 可修改的超时反例

把 T 个等待状态串起来：前 T 步无输出，第 T+1 步才输出第一位，此后持续输出0。机器的状态数为 T+1，每一个有限 T 都给出有限描述。

修改下面 T，先写下预测，再运行：在 T 步上限内看不到输出，在 T+1 步上限内应该看到什么？''')
code('''T = 20  # 练习：改为 0、5 或 50，再按顺序重跑
before = run(delayed_forever(T), T)
after = run(delayed_forever(T), T + 4)
print('预算 T:', repr(before['output']))
print('预算 T+4:', repr(after['output']))
print('首次输出步数:', next(row['step'] for row in after['trace'] if row['emitted']))
assert before['output'] == ''
assert after['output'] == '0000'
assert next(row['step'] for row in after['trace'] if row['emitted']) == T + 1''')
md('''推导：n≤T 时处于等待链，输出位数0；n>T 时执行了 n−T 次输出状态，输出位数 n−T。合并得到 max(0,n−T)。

这排除了“固定超时前没输出，因此永不输出”的推断。它没有证明“任何分析方法都不可能”，也不阻止我们阅读这台简单机器的规则并正确判断。''')
code('''silent = run(silent_forever(), T)
assert [row['output'] for row in before['trace']] == [row['output'] for row in silent['trace']]
print('前 T 步输出历史完全相同：', True)
print('注意：只比较输出历史，没有声称状态或机器描述相同。')''')
md('''## 6. 穷举324台，究竟覆盖了什么？

固定1个状态、2个工作符号；对每个输入表项可选2种写符号×3种移动×3种输出=18个动作。两个表项共18²=324张总转移表。

下面只记录20步内的输出数量，不给每台机器贴 circle-free 标签。即使受限类能有完整判定方法，也不能外推所有机器。''')
code('''from collections import Counter
hist = Counter(len(run(machine, 20)['output']) for machine in enumerate_one_state())
print('观察输出长度 -> 机器数量')
for length, count in sorted(hist.items()):
    print(length, '->', count)
assert dict(hist) == {0: 96, 1: 2, 10: 20, 19: 2, 20: 204}
print('总数:', sum(hist.values()))''')
md('''## 7. 练习与答案框架

练习：预测等待机器在 n=0、T、T+1、T+7 时的输出位数；给出一个独立于模拟预算的证明。

答案框架：对 n≤T 和 n>T 分情况；说明等待链每步推进一个状态；说明输出状态每步访问新空白格并追加一个0。下面只检查有限个预测点，不替代归纳证明。''')
code('''for n in [0, T, T + 1, T + 7]:
    observed = len(run(delayed_forever(T), n)['output'])
    predicted = max(0, n - T)
    print('n=', n, '预测=', predicted, '观察=', observed)
    assert observed == predicted''')
md('''## 8. 回到独立测试与复盘

把 notebook 的展示逻辑与核心模拟器测试分开。下一个单元启动独立进程运行15项测试，涵盖精确轨迹、负坐标、擦除、缺失规则、延迟边界和有限枚举。

拓展：增加一台先输出10位再静默右移的机器，证明其不停机但结果有限。不要尝试仅凭任意选定的模拟上限，就为所有机器赋予无限输出标签。''')
code('''import subprocess
check = subprocess.run([sys.executable, '-m', 'unittest', '-v', 'test_simulator'],
                       capture_output=True, text=True, check=True)
print('\n'.join(check.stderr.strip().splitlines()[-4:]))'''.replace("print('\n'", "print('\\n'"))
md('''## 结论的三层证据

1. 实际观察：具体预算内产生了哪些位、执行了哪些转移。
2. 特定机器的规则证明：通过归纳建立此例的无限行为。
3. 一般不可能性定理：需要论文中的反证、自指与归约，不能由本 notebook 的有限运行取代。

完整轨迹看 results.json；来源边界、公式和执行命令看 README.zh-CN.md；15项测试的记录看 tests.log。运行本 notebook 的逐单元标准库校验看 notebook_check.json。''')
nb['cells'] = cells
nb['metadata']['verification'] = {'method': 'stdlib sequential Python exec, not a Jupyter kernel',
                                'jupyter_kernel_verified': False}
path.write_text(json.dumps(nb, ensure_ascii=False, indent=2) + '\n')
