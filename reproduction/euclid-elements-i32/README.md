# I.32 最小精确教学复现

这是原创 Python 标准库有理坐标核验，不是古代尺规操作的完整复现，也不是一般综合几何定理的机器证明。源码不导入第三方库，不使用浮点角度。完整原文论证见[深读](../../papers/ancient/euclid-elements-i32.zh-CN.md)。

## 输入与边界

输入为恰含 A、B、C、D、E 的字典；每点为两个规范有理数字符串的列表，如 `"0"`、`"-3/2"`。拒绝布尔、整数、浮点、非规范分数和额外字段。ABC 必须非共线；D 必须在 BC 越过 C 的延长线上；CE 必须正向平行 BA，并严格位于外角 ACD 内部。这里 E 是现代坐标见证，不认证 I.31 构造操作的历史。

`geometry.make_certificate(data)` 对不合条件的输入直接抛出 ValueError；`verify_certificate(expected_input, certificate)` 重算并逐类型逐字段比较，绑定完整输入而不仅绑定结论。证书包括原输入、SHA256、点序比例、角对及角乘积。摘要不是安全签名；攻击者可以重算摘要，因此核验器仍重算几何条件。

## 重跑

在本目录执行：

```sh
python3 run_all.py
```

该命令分别运行普通、`-O`、`-OO` 单元测试，演示、Notebook 生成执行及独立回放比对。测试不依赖可被优化移除的裸 assert。全部返回码见 [run-summary.json](run-summary.json)，执行环境见 [environment.json](environment.json)，命令和实际标准输出/错误在 [logs](logs/)。

本次 27 测试在三种模式通过；[results.json](results.json)记录576个正输入及9类负输入直接拒绝。正例涵盖锐/钝/直角、正负方向、四种旋转、平移与不同延长比例，不代表所有实数输入。

[Notebook](teaching.zh-CN.ipynb)六代码格使用标准库 `compile/exec` 真实自上而下执行，并重新执行比对输出，见 [notebook-check.json](notebook-check.json)。这不是 Jupyter kernel 会话。已检查安装技能指定的 scaffold helper，其本地路径不存在，故用仓库自有 [create_notebook.py](create_notebook.py)生成；未安装新技能或依赖。

## 文件

- [geometry.py](geometry.py)：精确条件与证书。
- [cases.py](cases.py)、[test_geometry.py](test_geometry.py)：有限样例与单元测试。
- [run_examples.py](run_examples.py)：演示数据。
- [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：角对原理、手算与反例。
- [verify_notebook.py](verify_notebook.py)：Notebook输出回放检查。
- [SHA256SUMS.json](SHA256SUMS.json)：本目录文件摘要（清单自身除外）。

欧氏坐标空间已经采用欧氏结构。实跑不证明第五公设、不证明其独立性，也不验证非欧几何的一般结论；坐标验证不得倒灌为欧几里得原文的公理依赖。
