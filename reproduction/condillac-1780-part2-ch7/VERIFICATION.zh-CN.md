# 实际验证记录

核验时间（UTC）：2026-10-12T05:42:30.918205+00:00

Python：3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]

平台：Linux-6.18.44-x86_64-with-glibc2.41

总结果：PASS。普通、-O、-OO 的演示、变异与演练 stdout 完全一致：True。

每种模式运行9个单元测试、8个行为变体和独立行列式／叉积审计（35,308个方程组、176,540次行操作）。45个参数组的整数正方形核对、729个二行系统的有理样点核对在单元测试内执行。样点测试不是一般证明。

## 命令和退出码

- `normal` / `demo`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 demo.py`；退出码 0；[stdout](evidence/demo_normal.stdout.txt) / [stderr](evidence/demo_normal.stderr.txt)
- `normal` / `tests`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest -v`；退出码 0；[stdout](evidence/tests_normal.stdout.txt) / [stderr](evidence/tests_normal.stderr.txt)
- `normal` / `mutations`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 mutation_check.py`；退出码 0；[stdout](evidence/mutations_normal.stdout.txt) / [stderr](evidence/mutations_normal.stderr.txt)
- `normal` / `walkthrough`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 walkthrough.py`；退出码 0；[stdout](evidence/walkthrough_normal.stdout.txt) / [stderr](evidence/walkthrough_normal.stderr.txt)
- `normal` / `independent_argument`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 independent_argument_checks.py`；退出码 0；[stdout](evidence/independent_argument_normal.stdout.txt) / [stderr](evidence/independent_argument_normal.stderr.txt)
- `O` / `demo`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -O demo.py`；退出码 0；[stdout](evidence/demo_O.stdout.txt) / [stderr](evidence/demo_O.stderr.txt)
- `O` / `tests`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -O -m unittest -v`；退出码 0；[stdout](evidence/tests_O.stdout.txt) / [stderr](evidence/tests_O.stderr.txt)
- `O` / `mutations`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -O mutation_check.py`；退出码 0；[stdout](evidence/mutations_O.stdout.txt) / [stderr](evidence/mutations_O.stderr.txt)
- `O` / `walkthrough`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -O walkthrough.py`；退出码 0；[stdout](evidence/walkthrough_O.stdout.txt) / [stderr](evidence/walkthrough_O.stderr.txt)
- `O` / `independent_argument`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -O independent_argument_checks.py`；退出码 0；[stdout](evidence/independent_argument_O.stdout.txt) / [stderr](evidence/independent_argument_O.stderr.txt)
- `OO` / `demo`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -OO demo.py`；退出码 0；[stdout](evidence/demo_OO.stdout.txt) / [stderr](evidence/demo_OO.stderr.txt)
- `OO` / `tests`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -OO -m unittest -v`；退出码 0；[stdout](evidence/tests_OO.stdout.txt) / [stderr](evidence/tests_OO.stderr.txt)
- `OO` / `mutations`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -OO mutation_check.py`；退出码 0；[stdout](evidence/mutations_OO.stdout.txt) / [stderr](evidence/mutations_OO.stderr.txt)
- `OO` / `walkthrough`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -OO walkthrough.py`；退出码 0；[stdout](evidence/walkthrough_OO.stdout.txt) / [stderr](evidence/walkthrough_OO.stderr.txt)
- `OO` / `independent_argument`：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -OO independent_argument_checks.py`；退出码 0；[stdout](evidence/independent_argument_OO.stdout.txt) / [stderr](evidence/independent_argument_OO.stderr.txt)

[机器可读环境、命令与源码 SHA-256](evidence/summary.json)。无网络、随机数、第三方安装。所有拒绝检查使用显式异常，测试使用 unittest，不依赖可被优化移除的 assert。

验证器保存退出码与原始日志，任一子进程失败或跨模式确定性检查失败都会使其自身退出1。日志时间与主机信息是执行事实，不是历史来源证据。
