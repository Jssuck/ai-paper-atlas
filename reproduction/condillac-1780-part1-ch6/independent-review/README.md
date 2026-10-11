# 独立代码复核：复跑说明

本目录由独立复核者编写，不把作者的 `tests/test_model.py` 或 `finite_oracle.py` 当作独立预期值来源。仅使用 Python 标准库；不需要安装、网络、账号、Notebook 或 GPU。

## 一键复跑

在上一层复现根目录运行：

```sh
python3 -B independent-review/run_review.py
```

脚本也可从别处通过路径启动；内部工作目录固定为复现根目录。记录中的命令采用实际解释器的文件名，省略机器私有绝对路径。实际 Python 版本、平台、UTC 时间、退出码、耗时、源码 SHA-256 见[执行环境](logs/environment.json)与[验证汇总](logs/verification.json)。

这会实际执行普通、`-O`、`-OO` 三种模式下的独立测试、作者单元测试、作者有限 oracle 和演示，并执行三种模式的独立有效语义变异。日志写入本目录 `logs/`；生产文件不被修改。变异副本位于自动清理的临时目录。

单独复跑独立检查：

```sh
python3 -B independent-review/test_independent.py
python3 -B -O independent-review/test_independent.py
python3 -B -OO independent-review/test_independent.py
python3 -B independent-review/mutations_independent.py
```

快速边界／变异基准：

```sh
python3 -B -OO independent-review/test_independent.py --quick
```

## 文件与证据

- [复核报告](review.zh-CN.md)：结论、修复记录、精确覆盖范围和限制。
- [独立测试脚本](test_independent.py)：12 个快速回归方法及 6 个完整复核方法，共 18 个；内部有限枚举次数见日志，不把循环次数误称为独立测试方法。
- [独立变异脚本](mutations_independent.py)：23 个独立语义变异，每个在三种优化模式执行，共 69 次。必须语法合法、全部快速测试运行、至少一项断言检查失败且零测试错误，才记为 `KILLED_BY_ASSERTION`。
- [完整复跑脚本](run_review.py)：三模式执行、裸 `assert` AST 扫描、模式结果比较、路径清理检查，以及执行前后的源码／作者文档哈希一致性检查。
- [验证汇总](logs/verification.json)：最终结构化汇总。作者测试和作者 oracle 在本日志中的复跑仍然属于作者检查，不因复跑而变成独立 oracle。
- [当前变异结果](logs/mutations.json)、[当前变异完整日志](logs/mutation-details.txt)：当前 69 次有效语义检出证据。
- [初轮变异结果](logs/mutations-initial.json)、[初轮变异完整日志](logs/mutation-details-initial.txt)：初轮证据。最初扩大接受所有布尔数的变异引发错误异常类型，被严格分类为无效检出，未计入通过；随后缩小为“错误接受布尔初值”，以检查失败而非运行错误检出。该初轮不是当前生产代码失败，也不是当前变异集的计数。
- [初步数学检查](logs/preliminary-normal.txt)：修复前第一次数学复核记录；当时尚无独立裸字符串回归方法。不得将它代替最终三模式记录。

所有检查使用 `unittest` 或显式异常，不依赖会被 `-O` 删除的裸 `assert`。变异仅衡量列出的故障能否检出；有限范围没有证明所有输入都正确，也没有证明模型是实际心理、道德或历史机制。
