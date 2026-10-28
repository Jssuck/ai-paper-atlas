# Euclid II.2：精确几何教学核验

这是原创现代有理坐标模型，不是原文证明的替代，也不是《原本》的完整复现或公理系统形式化。原命题的连续任意线段范围不能由有限测试证明。

## 对应关系

- `construct(A,B,D,t)` 接受两个等长、垂直且非零的边 AB、AD，以及严格内部参数 `0 < t < 1`。坐标只接受整数或 `Fraction`；拒绝浮点和布尔值。
- 点序：正方形 **A-D-E-B**；C 在 AB 上，F 在 DE 上，CF 平行 AD。
- `AF` 是区域 **A-D-F-C**，不是线段 AF 的长度；`CE` 是区域 **C-F-E-B**。
- `verify` 不调用 `construct`。它逆解仿射坐标检验每个点和命名绑定，验证两块矩形的边、直角和共边；有序参数区间 `[0,t]` 与 `[t,1]` 认证无缝、内部不重叠的覆盖。随后用鞋带公式分别求三个多边形面积。面积和相等本身不是覆盖证书，测试特意包含等面积交换块的反例。
- 等边与垂直条件保证正方形。现代坐标、行列式、鞋带面积算法都是教学重构；它们使用现代代数，不能说成欧几里得原证。

## 环境与真实运行

只用 Python 3 标准库，不下载资料、不联网、不安装包。版本见 [environment.json](environment.json)。从本目录运行：

```sh
python run_all.py
```

该入口顺序执行并保存实际 stdout/stderr 与退出码：

1. `python -m unittest test_geometry -v` → [普通模式](logs/tests-normal.log)
2. `python -O -m unittest test_geometry -v` → [-O](logs/tests-O.log)
3. `python -OO -m unittest test_geometry -v` → [-OO](logs/tests-OO.log)
4. `python run_examples.py` → [算例](logs/examples.log)、[results.json](results.json)
5. `python create_notebook.py` → [执行日志](logs/notebook-execute.log)
6. `python verify_notebook.py` → [回放日志](logs/notebook-replay.log)、[notebook-check.json](notebook-check.json)
7. `python draw_figure.py` → [作图日志](logs/figure.log)、[原创示意图](figures/partition.svg)

每模式 **29 项测试**，其中网格项遍历 **64 个有效有理坐标构形**。网格覆盖斜置、平移、正反朝向及不同内部切点；其他测试包含分数尺度、零边、非正交、非等边、端点、外切、非法类型、错误点名、重复/换序区域和不相符切点。3 模式不等于 87 个不同定理情形。优化模式检查验证逻辑不依赖被优化删除的 `assert`。

[teaching.zh-CN.ipynb](teaching.zh-CN.ipynb) 有五格代码，逐格用标准库 `compile/exec` 在共享新命名空间真实执行，保存 stdout，execution_count 保持 null，再在独立新命名空间回放核对输出。**未启动 Jupyter kernel**，不能把这种回放说成 Jupyter 内核运行。已读取 Notebook 技能；本环境其默认 `new_notebook.py` 不存在，因此使用自行编写的 nbformat 4.5 scaffold；未安装依赖。

## 读数与边界

整数算例 AB=AD=6，AC=2、CB=4；分别得到 36、12、24。斜置和反射算例整块面积25，两块10与15。分数尺度算例得到1/4、1/12与1/6。各读数来自实际执行结果，不是手填实验日志。

原文的几何分割首先解释为何是同一个整块；本程序只检查给定精确输入在这个模型中的证书。拒绝端点与外切是模型边界；这不否认可另外定义零面积或有向扩展。`2²+4²=20` 不等于整段平方36，因为原命题是整段分别与两段构成矩形，不是两段各自平方。

原文链接与完整解释见[中文深读](../../papers/ancient/euclid-elements-ii2.zh-CN.md)。源码与日志公开前应再经独立审查；审查记录以同目录独立审查文件为准。

## 独立技术复核

独立复核另运行 `independent_check.py`，按不同边方向、反射和切点生成90个合法构形；用边长平方计算预期整块面积，并分别核对两块。逐点位移、翻转区域绑定、错误点集合容器和非正方形输入合计819个拒绝检查。分别在普通、`-O`、`-OO`模式真实通过，日志见 [normal](logs/independent-normal.log)、[-O](logs/independent-O.log)、[-OO](logs/independent-OO.log)。这三条命令独立于上面7条 `run_all.py` 命令，不混计为同一执行入口。

```sh
python independent_check.py
python -O independent_check.py
python -OO independent_check.py
```

独立审查发现并修正了坏证书把 `points` 字段改成字母列表时触发异常而非返回拒绝的问题：现在先检查该字段为字典，新增第29项回归测试。Notebook计数改为null，保留真实捕获stdout与明确的非kernel执行说明。完整修正后重新跑过全部7条主命令及上述3条独立命令。
