# I.15 复现附件：独立代码核验

## 核验范围与结论

独立复核了 `model.py`、`demo.py`、`test_model.py` 及附件说明的契约。未发现需修改的实现错误。核验针对本文**固定论域、实际主项、逐对象模态**教学语义；不认证它是亚里士多德唯一语义，不认证历史论证的所有解释，也不以有限运行证明一般定理。

精确输入 SHA256 与运行环境记录在 [review-inputs.json](code-review/review-inputs.json)。这里的哈希绑定源码、作者测试、说明、作者结果及独立检查器；任一被绑定文件修改后，须重核受影响部分，不能沿用此结论。

## 独立方法

[check_semantics.py](code-review/check_semantics.py) 不调用作者的模型生成器来建立样本，也不以作者的语义函数生成期望值。它自行用集合构造各世界的词项外延，显式逐对象、逐世界计算期望真值，再与作者接口比较：

- 全部三个词项两两组合的 AEIO，含明确世界索引；
- 全部词项对的 K、M+、M− 与全称／特称；
- 对象正反可能、逐世界稳定包含／不交；
- 实际主项范围上，同一世界的全称共同实现；
- 强结论额外见证条件，特别是特称条件中同一对象绑定；
- 长度1–5的布尔向量可能性与跨全部位置的后承。

规模是：1与2对象、1与2世界，以及1对象3世界；对各模型分别使用每个实际索引。共 **9,928个模型／实际索引配置**，不去除同构或空词项。

| 比较类别 | 每次运行的比较数 |
|---|---:|
| AEIO（所有项对及世界） | 767,520 |
| K／M+／M−及全称／特称 | 536,112 |
| 对象正反可能 | 109,104 |
| 稳定包含／不交 | 178,704 |
| 强结论见证条件 | 39,712 |
| 同一世界共同实现 | 178,704 |
| 布尔后承向量对 | 1,364 |

独立检查器在普通、`-O`、`-OO` 三模式均通过；日志分别为 [normal](code-review/oracle-normal.json)、[-O](code-review/oracle-O.json)、[-OO](code-review/oracle-OO.json)。检查用显式异常，不依赖会被优化掉的 `assert`。

## 作者测试与结果复核

独立重跑作者28项测试，普通、`-O`、`-OO`均通过：[普通日志](code-review/tests-normal.log)、[-O日志](code-review/tests-O.log)、[-OO日志](code-review/tests-OO.log)。

独立重新执行演示，产出 [demo-independent.json](code-review/demo-independent.json)，并以字节比较确认与作者 `results/demo.json` 完全一致。8,320个演示配置、各桥接分支计数与说明表一致；这些分支有重叠，不可相加当作独立样本。预期的强结论失败与时间片失败是反例检查，不是被隐瞒的运行错误。

## 选择性变异检验

[check_mutations.py](code-review/check_mutations.py) 在临时副本中分别改变实现，运行原作者测试，不修改原文件。九个选择性错误均被测试识别，原始退出码与测试输出见 [mutations.json](code-review/mutations.json)：

1. 忽略实际索引；
2. 双向偶然删掉反向见证；
3. 特称误用全称聚合；
4. 稳定大前提只在实际世界检查；
5. 共同实现误用逐对象可能；
6. 强桥额外见证符号翻转；
7. 将布尔值接受为论域整数；
8. 可能性误作必要性；
9. 后承只检查实际位置。

这是有针对性的敏感性检查，不是穷尽所有潜在缺陷、所有变异算子或安全审计。九个检出也不能推出任何未测实现绝无错误。

## 重跑命令

在附件目录执行：

```sh
python code-review/check_semantics.py
python -O code-review/check_semantics.py
python -OO code-review/check_semantics.py
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python code-review/check_mutations.py
python demo.py
```

源码只依赖标准库，无网络、密钥或付费服务。未声称运行Jupyter内核、完整古典自动证明器、现实数据实验、无限模型枚举或GitHub CI。
