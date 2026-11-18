# III.26 的精确有理数教学复现

这是 Euclid III.26 的教学复现。代码及首轮审查制作于 2026-11-12，仓库路径整合于 2026-11-18。只依赖 Python 3 标准库；首轮实跑环境为 CPython 3.12.14，新整合环境及退出码见 `integration-run.json`。

## 重跑

在本目录运行：

```sh
python3 -m unittest -v test_geometry
python3 run_experiments.py
python3 -O -m unittest -v test_geometry
python3 -O run_experiments.py
python3 -OO -m unittest -v test_geometry
python3 -OO run_experiments.py
```

首轮真实结果保存在 `logs/historical-20261112/`；本次目录整合后的真实结果保存在 `logs/integration-20261118/`。两者分开留存，修改源码后必须重新运行，不可把旧日志归给新代码。

## 模型和范围

`geometry.py` 实现圆弧、精确扫掠分支、圆周角余切及等距对应。公开构造器和接受外部点的方法，对数值输入只接受整数/Fraction，显式拒绝数值位置的 bool/float；方向参数 ccw 必须是 bool。内部 add/sub/dot/scale 等向量 helper 不分别验证任意外部输入。Arc 要求正半径、圆周上的不同端点、布尔方向；不含零弧或整圆。圆周角顶点必须在同圆的目标互补开弧上。

`test_geometry.py` 有 24 项单元测试，包含优劣弧、半圆、方向、半径反例、混合角类型、变换和非法输入。`run_experiments.py` 每模式使用 66 个弧配置、42 个有理圆周样本点及两个刚体目标，完成 2,664 次圆周角检查、5,544 次点映射/成员/到起点距离检查和 66 个异半径对照。

比较相等使用 Fraction 精确算术，没有浮点容差。运行中的显式异常检查不依赖 `assert`，优化模式不会关闭这些检查。`unittest` 的断言方法也不随 `-O` 消失。

有限样本不是一般证明。实验不包含所有点对距离、噪声鲁棒性、完整证明助理认证或 GitHub 页面显示验证。普通、-O、-OO 重复同一配置，不可将覆盖数乘三后当成三倍不同数据。独立审查者的工作在 [技术审查](audit/technical/review.md)，不得与作者运行混淆。

## 整合与审查记录

- [原文审查公开摘录](audit/source-review.md)与[技术审查公开摘录](audit/technical/review.md)总结 2026-11-12 的独立审查及最终版本确认。摘录明确标注删去内部文件管理内容，不将后续字节更改冒称已在旧日期审过。
- 正文数学推导保持不变；仅修复相对链接、更新制作/验收范围说明。三份作者源码保持逐字节不变。
- 独立检查器移动到 `audit/technical/` 后，导入根目录及读取 `geometry.py` 哈希的路径随之调整；几何核查逻辑不变。
- 原始日志保存在历史子目录；当前重跑结果由 `integration-run.json` 索引。相同三模式不是三倍不同样本。

从本目录运行独立检查器：

```sh
python3 -B audit/technical/independent_checks.py
python3 -B -O audit/technical/independent_checks.py
python3 -B -OO audit/technical/independent_checks.py
```

独立检查器使用整数格点圆和循环序位，不使用作者的有理参数生成式。当前重新执行该已有检查器不等于新独立代码审查；整合包须另外审查路径、公开范围与日志归属。本文和有限实验不构成一般定理的机器证明。本地验收不等于远端发布或 GitHub 公式显示验收。
