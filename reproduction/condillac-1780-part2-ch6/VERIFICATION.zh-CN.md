# 实际验证记录

本记录对应 2026-10-12T04:53:55.595508+00:00 完成的最终验证运行。日志是实际执行所得，并非预期输出占位。

## 环境

- 操作系统：`Linux-6.18.44-x86_64-with-glibc2.41`
- Python：`3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]`
- 解释器：`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3`
- 工作目录：本附录目录 `reproduction/condillac-1780-part2-ch6/`
- 依赖：仅 Python 标准库；没有安装包、连接网络、下载数据或执行远程写入
- 子进程固定 `PYTHONHASHSEED=0`，设置 `PYTHONDONTWRITEBYTECODE=1`，移除外部 `PYTHONOPTIMIZE` 后分别显式传入优化标志

每种模式的环境日志另记录 `sys.flags.optimize`：普通模式为 0，`-O` 为 1，`-OO` 为 2。

## 可重跑命令

在附录目录运行：

```sh
export PYTHONDONTWRITEBYTECODE=1
python3 verify.py
```

该脚本执行以下三模式矩阵，并将每次标准输出、标准错误、退出码、耗时和校验和保存到 `evidence/`：

```sh
export PYTHONDONTWRITEBYTECODE=1
python3 -m unittest discover -v
python3 -O -m unittest discover -v
python3 -OO -m unittest discover -v
python3 mutation_check.py
python3 -O mutation_check.py
python3 -OO mutation_check.py
python3 demo.py
python3 -O demo.py
python3 -OO demo.py
```

另执行三个环境探针及一个演练运行器，共 13 个子进程。演练运行器从 `WALKTHROUGH.zh-CN.md` 提取全部 Python 代码块，按文中顺序在同一进程运行；结果保存在 `evidence/walkthrough.stdout.txt`。它验证代码块能够顺序执行；注释中的预期值还由作者逐项核对输出，不把普通注释冒充自动断言。

## 结果

| 项目 | 普通模式 | `-O` | `-OO` |
| --- | --- | --- | --- |
| `unittest` | 45 / 45 通过 | 45 / 45 通过 | 45 / 45 通过 |
| 变异基线探针 | 6 / 6 通过 | 6 / 6 通过 | 6 / 6 通过 |
| 定向变异的行为差异 | 6 / 6 检出 | 6 / 6 检出 | 6 / 6 检出 |
| 变异框架意外异常 | 0 | 0 | 0 |
| 演示退出码 | 0 | 0 | 0 |

全部 13 个子进程退出码为 0；三份演示 JSON 的解析结果一致。`summary.json` 的总结果为 `passed: true`。

测试方法中不存在裸 `assert`。独立的 AST 检查确认作者交付的六个 Python 源文件的 `ast.Assert` 节点数为 0，避免靠普通模式才生效的断言伪造优化模式验证。

## 穷举边界与 oracle

| 检查 | 明确的穷举范围 | 个案数 |
| --- | --- | --- |
| 布尔表达式真值表 | 0、1、2 个原始变量的全部布尔函数 | 22 张表 |
| 两层显式定义 | 首层为全部小原始函数，次层为首层的一元布尔函数，并交换定义输入顺序 | 176 个系统，592 个旧世界个案 |
| 观察可表示性 | 0、1、2 个原始变量，0、1、2 个特征，对全部特征/目标真值表组合 | 4,466 个案 |
| 规则闭包 | 两个名称的全部 8 条可能规则的所有子集，配全部种子子集 | 1,024 个案 |
| 次序检查 | 上述个案下，长度 0、1、2 的所有无重复名称排列 | 5,120 个案 |

定义 oracle 穷举所有新名赋值并逐条检查等式；观察 oracle 枚举观察签名到布尔值的全部映射；规则 oracle 取全部闭合超集之交。oracle 与被测算法的关系和共享求值器的限制在模型说明中公开。

## 六个定向变异是什么

| 变异名称 | 注入的错误 | 实际捕获方式 |
| --- | --- | --- |
| `flip_defined_value` | 翻转正确扩张中的新定义值 | 与预期完整扩张比较失败 |
| `ignore_fiber_conflict` | 忽略同一观察下相反目标 | 可表示性布尔值比较失败 |
| `any_instead_of_all_premises` | 有一个前提就允许导出 | 闭包集合比较失败 |
| `future_premises_allowed` | 让未来步骤为当前步骤供给前提 | 反序合法性比较失败 |
| `ignore_evidence` | 不执行证据过滤 | 剩余世界集合比较失败 |
| `overwrite_old_name` | 覆盖固定的旧值 | 满足扩张集合比较失败 |

只有 `BehaviorMismatch` 被记为行为检测。`RuntimeError` 等意外异常记为 `harness_error`，不计为检测成功，并令整个变异脚本失败。测试另人为触发框架异常来检查这个分类边界。六个选定故障均检出，不等于所有可能程序变异都被覆盖。

## 如何追溯

- [结构化总记录](evidence/summary.json)：实际时间、命令、退出码、耗时、文件校验和，以及六个变异的逐项细节
- [普通模式测试日志](evidence/tests_normal.stderr.txt)
- [优化模式测试日志](evidence/tests_O.stderr.txt)
- [双重优化模式测试日志](evidence/tests_OO.stderr.txt)
- [普通模式变异结果](evidence/mutations_normal.stdout.txt)
- [演示 JSON](evidence/demo_normal.stdout.txt)
- [演练实跑输出](evidence/walkthrough.stdout.txt)
- [源文件和断言检查](evidence/source_validation.json)

这些记录验证了当前实现和列出的边界，没有进行性能压测、外部历史资料检索或心理学实验。一般数学断言的依据是 [MODEL.zh-CN.md](MODEL.zh-CN.md) 中的证明；历史解释的依据应由主文的原典引文给出。
