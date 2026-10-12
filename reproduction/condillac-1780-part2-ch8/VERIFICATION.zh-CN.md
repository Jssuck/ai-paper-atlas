# 实际验证记录

执行时间（UTC）：2026-10-12T07:20:15.471777+00:00

Python：3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]

平台：Linux-6.18.44-x86_64-with-glibc2.41

总结果：PASS。每种模式运行34个单元测试；13个行为故障探针另行执行。

普通、-O、-OO 的 demo／mutations／walkthrough stdout 字节一致：True。
运行前后被记录源码及静态文档哈希不变：True。

## 真实命令与日志

命令按可移植解释器名称展示；实际子进程使用运行本验证器的同一个 sys.executable。安装目录不写入公开记录。

- `normal` / `demo`：`python3 demo.py`；退出码 0；[stdout](evidence/demo_normal.stdout.txt) / [stderr](evidence/demo_normal.stderr.txt)
- `normal` / `tests`：`python3 -m unittest -v`；退出码 0；[stdout](evidence/tests_normal.stdout.txt) / [stderr](evidence/tests_normal.stderr.txt)
- `normal` / `mutations`：`python3 mutation_check.py`；退出码 0；[stdout](evidence/mutations_normal.stdout.txt) / [stderr](evidence/mutations_normal.stderr.txt)
- `normal` / `walkthrough`：`python3 walkthrough.py`；退出码 0；[stdout](evidence/walkthrough_normal.stdout.txt) / [stderr](evidence/walkthrough_normal.stderr.txt)
- `normal` / `independent_argument`：`python3 independent_argument_checks.py`；退出码 0；[stdout](evidence/independent_argument_normal.stdout.txt) / [stderr](evidence/independent_argument_normal.stderr.txt)
- `O` / `demo`：`python3 -O demo.py`；退出码 0；[stdout](evidence/demo_O.stdout.txt) / [stderr](evidence/demo_O.stderr.txt)
- `O` / `tests`：`python3 -O -m unittest -v`；退出码 0；[stdout](evidence/tests_O.stdout.txt) / [stderr](evidence/tests_O.stderr.txt)
- `O` / `mutations`：`python3 -O mutation_check.py`；退出码 0；[stdout](evidence/mutations_O.stdout.txt) / [stderr](evidence/mutations_O.stderr.txt)
- `O` / `walkthrough`：`python3 -O walkthrough.py`；退出码 0；[stdout](evidence/walkthrough_O.stdout.txt) / [stderr](evidence/walkthrough_O.stderr.txt)
- `O` / `independent_argument`：`python3 -O independent_argument_checks.py`；退出码 0；[stdout](evidence/independent_argument_O.stdout.txt) / [stderr](evidence/independent_argument_O.stderr.txt)
- `OO` / `demo`：`python3 -OO demo.py`；退出码 0；[stdout](evidence/demo_OO.stdout.txt) / [stderr](evidence/demo_OO.stderr.txt)
- `OO` / `tests`：`python3 -OO -m unittest -v`；退出码 0；[stdout](evidence/tests_OO.stdout.txt) / [stderr](evidence/tests_OO.stderr.txt)
- `OO` / `mutations`：`python3 -OO mutation_check.py`；退出码 0；[stdout](evidence/mutations_OO.stdout.txt) / [stderr](evidence/mutations_OO.stderr.txt)
- `OO` / `walkthrough`：`python3 -OO walkthrough.py`；退出码 0；[stdout](evidence/walkthrough_OO.stdout.txt) / [stderr](evidence/walkthrough_OO.stderr.txt)
- `OO` / `independent_argument`：`python3 -OO independent_argument_checks.py`；退出码 0；[stdout](evidence/independent_argument_OO.stdout.txt) / [stderr](evidence/independent_argument_OO.stderr.txt)

[环境、命令、退出码与文件 SHA-256 汇总](evidence/summary.json)。

作者单元测试涵盖输入拒绝、同答案多世界、空域、逐步改写、编码纤维、测量策略和可执行因果机制。变异分类器另检验 baseline_error、invalid_baseline、mutant_error、survived 与 killed；异常不算击杀。

独立论证审计由另一审计者编写，采用位掩码分割与逐层有限深度树存在性 oracle。该脚本输出自己的范围、实际案例数和模型／脚本哈希；其 optimization 字段按模式变化，不要求整份 stdout 相同。独立审核意见与作者本地运行日志分开。

每个子进程都真实运行；任一非零退出、指定演示跨模式不一致或被记录文件运行中改变，均使 verify.py 退出1。本验证器调用的核心、演示、作者测试和穷举论证审计不使用网络、随机数或第三方安装；其他独立审核可使用固定种子补充案例。拒绝检查不依赖 assert。有限核对不是史学证据，也不是未给假设范围内的一般证明。
