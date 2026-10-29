# Euclid《几何原本》III.11：精确有理教学实验

[中文深读](../../papers/ancient/euclid-elements-iii11.zh-CN.md) · [教学 Notebook](teaching.zh-CN.ipynb) · [原创示意图](diagram.svg)

## 检验什么

这是现代二维欧氏坐标重构，不是欧几里得原文算法，也不是形式化证明器。实际读本采用 [Joyce III.11](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII11.html)：原证假设接点不在线上，用 I.20 严格三角不等式导出较小线段反而较大；其 Guide 提醒图形依赖。程序不用原文标号，使用大圆心 O、小圆心 C、公共点 T。

`verify_contact(outer,inner,t)` 的输入前提只有：正半径且 R>r、闭圆盘包含、输入点同时位于两圆周。**没有把共线作为输入，也没有先要求 d²=(R−r)²。** 包含检验先检查 R−r≥0，才平方为 d²≤(R−r)²。公共点检验使用两个独立平方距离。随后分别检查距离等式、叉积为零、正向点积及接点越过小圆心；任意结论失败会抛出异常，而不是静默输出成功。

`contact_candidate` 是单独的现代构造接口：在有序内切对上输出 O+R(C−O)/(R−r)。这不能作为证明核验器正确的唯一证据，因此测试与独立审核另外提供由单位有理方向参数化的接点。`relation` 用精确平方距离区分重合、同心不同半径、严格内含、内切、两交点、外切、分离；它不求任意两圆交点，因交点未必是有理数。

## 运行

Python 3.12 标准库（具体实跑版本见 [环境记录](environment.json)）。不依赖第三方包，无需联网或安装。

```sh
python run_all.py
```

请先进入本目录。编排脚本执行以下命令，捕获真实 stdout/stderr 与返回码；日志不包含主机路径、账户名或私人对话。

```sh
python -m unittest -v test_geometry
python -O -m unittest -v test_geometry
python -OO -m unittest -v test_geometry
python run_examples.py
python create_notebook.py
python verify_notebook.py
```

## 实跑证据与边界

- 26 个单元测试分别在普通、`-O`、`-OO` 下通过。使用 unittest 检验和显式异常，不靠会被优化移除的裸 `assert`。
- 每种模式的网格测试检查 600 个精确构形：4 个平移 × 5 个有理单位方向 × 3 个小半径 × 10 个正半径差。方向包含坐标轴、反射和非轴向的 3/5–4/5、−5/13–12/13。
- 4 个合法命名算例：水平、平移旋转、反射、有理缩放；3 个拒绝对照：两交点的非共线公共点、外切、错误圆周点。外切仍可共线，但不在本命题的内切输入域。
- 输入拒绝零/负半径、浮点、布尔值、坏点维度、颠倒内外圆和重合圆。`10^-50` 的精确位移不被容差吞没。
- [Notebook](teaching.zh-CN.ipynb) 的五个代码格确实按顺序用标准库 `compile/exec` 执行并保存输出；独立的只读回放脚本再次执行并逐格比对 stdout。**这不是 Jupyter kernel 执行记录。** 已读取 Notebook 技能，但本环境安装路径和可读技能资源均未提供模板 helper；使用本地 nbformat4 scaffold，没有安装替代软件。
- [运行摘要](run-summary.json)、[普通测试](logs/tests.log)、[优化测试](logs/tests-O.log)、[二级优化测试](logs/tests-OO.log)、[算例](logs/examples.log)、[Notebook 执行](logs/notebook.log)、[Notebook 回放](logs/notebook-replay.log)。

这是低成本有限回归，不证明所有实数构形，不从有限采样认证未知曲线为圆，不实现任意实数求交，也不补成古典公理系统。一般证明仍须在正文给出。示意图左为合法内切圆，右仅为反证假设的三角形，不能误认作同时满足内切条件的真实两圆。

## 源码

[精确模型](geometry.py)、[测试](test_geometry.py)、[算例](run_examples.py)、[执行编排](run_all.py)、[Notebook 构建执行](create_notebook.py)、[只读回放](verify_notebook.py)。

## 独立核验

[独立来源审查](source-review.zh-CN.md) · [独立技术审查](technical-review.zh-CN.md)。独立审查者另写 [外部核验](external_checks.py) 和 [Notebook 只读核验](independent_notebook.py)，不修改冻结模型；具体统计、模式日志和绑定哈希以技术审查记录为准。
