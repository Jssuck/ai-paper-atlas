# Euclid III.8：外点、近弧与远弧的最小教学实验

本目录是原创的**现代有理坐标教学重构**，不是欧几里得原有算法，也不是对一般命题的机器证明。原命题可对照 [Joyce III.8](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII8.html)，完整原文定位、历史讨论及证明见[中文深读](../../papers/ancient/euclid-elements-iii8.zh-CN.md)。

## 模型与检查对象

圆心固定为原点，半径 `r>0`，外点 `D=(d,0)` 且 `d>r`。所有输入限整数或 `Fraction`，拒绝浮点数与布尔数，避免近似误差或 `bool` 冒充数值。圆上点 `P=(x,y)` 的距离平方满足 `DP²=d²+r²−2dx`；最小、最大分别为 `(d−r)²` 与 `(d+r)²`。

- **近暴露弧** `dx>r²`、**远弧** `dx<r²`、**切点** `dx=r²`。近暴露弧不是“正 x 半圆”：`r=5,d=6,P=(3,4)` 的 x 为正，但仍属远弧。
- 距离平方 `q` 确定 `x=(d²+r²−q)/(2d)`；`y²=r²−x²`。可行非端点有两个镜像点，最短/最长处只有一点，不可行值为零点。`equal_shell` 不宣称非有理平方根也有有理坐标，只返回其平方和实点数量。
- 已知圆上有理点 `P` 后，以 `D+s(P−D)` 参数化同一条射线。圆方程的根为 `1` 与 `(d²−r²)/|P−D|²`，故两个交点都可精确给出。根重合即切线。这个表示**不要求距离本身为有理数**。
- 对 `r=5,d=13,P=(3,4)`，另一个交点为 `(17/29,144/29)`；两点从 D 看到的斜率同为 `2/5`，但距离平方是 `116` 与 `5184/29`。故全上半圆的视角不是一一距离排序；必须先区分近/远分支。
- `run_examples.py` 在上半圆有限样本中以 `y²/DP²`（视角正弦平方）排序；近分支距离严格增、远分支严格减。该量在所检视角范围内有序，不将其当成全圆单调角度。

## 实际运行与复跑

只需 Python 3 标准库，无安装、无网络、无数据下载。在本目录执行：

```sh
python3 run_all.py
```

本次真实结果：8 个子命令全部退出 0；30 项 `unittest` 各在普通、`-O`、`-OO` 模式通过；每种模式遍历 **1071 个有限参数构形**（有重复几何点，不是1071个互异圆）。9 组 `(r,d)`、7 个分母和17个分子产生样本；检查距离恒等式、极值界、等长点数、镜像、割线方程和两段距离平方乘积。另有 **242 个分支样本**和 **236 个相邻严格次序比较**。切点样本单独检验，不混入开分支排序。

- [实际命令与退出码](run-summary.json)、[环境](environment.json)
- [普通测试](logs/tests-normal.log)、[-O 测试](logs/tests-O.log)、[-OO 测试](logs/tests-OO.log)
- [精确示例与有限计数](logs/examples.json)
- [教学 Notebook](teaching.zh-CN.ipynb)、[执行记录](logs/notebook-execute.log)、[只读重放记录](logs/notebook-replay.log)、[Notebook 检查](notebook-check.json)

Notebook 技能的安装路径模板助手不可用，未安装第三方包，采用 `create_notebook.py` 本地 nbformat 4 scaffold。5 个代码单元按顺序在同一命名空间实际 `compile/exec` 执行；再独立只读重放并逐单元比较输出。**不是 Jupyter kernel 执行**，`execution_count` 保持 `null`，保存输出不冒充 kernel 运行。可在兼容 Jupyter 中另行运行，但这里不声称已核验该环境。

## 文件和边界

`geometry.py` 是精确模型，`test_geometry.py` 是回归测试，`run_examples.py` 是例子与分支样本，`create_notebook.py` 和 `verify_notebook.py` 生成/核验 Notebook，`run_all.py` 生成所有运行证据。未使用 `assert` 作为关键检查，优化模式仍执行检查。`verify` 只重建本模型证书，不是独立几何证明器；它检查精确类型，避免整数 `1` 替代布尔 `True` 被漏过。

不处理任意坐标系变换、不解析原图、不证明 I.21 的平面内含关系，也不覆盖所有实数输入。有限测试、小实验、二次方程教学模型均不能替代正文一般证明。原文的合成推理与这里的解析重构须分开评价。
