# III.16 最小复现：切线与向内射线

这是原创的现代二维有理坐标教学实现，不是古代角概念的数值化，也不是通用欧氏证明器。对应[中文深读](../../papers/ancient/euclid-elements-iii16.zh-CN.md)。

## 模型与接口

`Circle(center, radius2)` 接收两个有理坐标及严格正的半径平方。坐标和数值仅接受整数或 `fractions.Fraction`，拒绝浮点数和布尔值。`analyze(circle, point, direction)` 先验证接点在圆周上、方向非零，再独立计算投影及相交证书，不把“只有一个接点”当作输入前提。

令 v=O−P，k=v·u，q=u·u>0。射线点P+tu的圆幂为t(tq−2k)。代码直接以坐标计算幂值，测试再与展开式对照。

- k=0：整条支撑线除P外都在圆外。到心距离平方等于半径平方。
- k>0：正参数2k/q给第二圆周点，k/q给严格内部见证，幂值为−k²/q。
- k<0：正向射线在圆外，但整条直线在负参数2k/q有另一个交点。不能把向外射线误称为切线。

`ray_power` 检查非负射线参数。`verify` 从合法输入重算并严格对照证书类型与字段；它不实现独立的通用证明验证器。`narrow_example(n)` 在单位圆心(0,1)、P=(0,0)、u=(n,1)上演示任意给定正有理n仍有内部点。有限样本不是对全部实数方向的证明；一般论证见正文。

模型允许有理平移、缩放及具有有理坐标的旋转方向。它不枚举全部实数圆周点，不一般求平方根，不计算曲线角或“正无穷小角”的数值，也不将数值极限冒充原文。

## 实际运行

Python标准库，无安装依赖。在本目录运行：

```sh
python run_all.py
```

`run_all.py` 顺序执行下列命令并保存真实stdout/stderr及退出码：

```sh
python -m unittest -v test_geometry
python -O -m unittest -v test_geometry
python -OO -m unittest -v test_geometry
python run_examples.py
python create_notebook.py
python verify_notebook.py
```

- 28项单测，每种模式覆盖1728个接点/方向构形、6912次射线幂值检查。另有类型拒绝、零方向、非圆周点、狭斜方向、证书篡改等检查。
- 四个命名方向算例：切向、向内、向外、直径方向；三个n=1、10、1000000狭斜算例；两个非法输入拒绝。
- Notebook五格用标准库 `compile/exec` 真正从上往下执行并保存输出；`verify_notebook.py` 独立只读回放并逐格比较输出。**不是Jupyter kernel执行**。本次环境中已安装技能所指scaffold脚本不存在，使用本地nbformat4结构生成，未安装额外包。可在正常Jupyter环境另行打开，本文没有声称做过该kernel检查。

[环境](environment.json)、[运行摘要](run-summary.json)、[普通测试](logs/tests.log)、[优化测试](logs/tests-O.log)、[双优化测试](logs/tests-OO.log)、[算例](logs/examples.log)、[Notebook执行](logs/notebook.log)、[Notebook回放](logs/notebook-replay.log)。

## 手算对照

圆心(0,5)、半径平方25、P=(0,0)、u=(3,4)时，k=20、q=25，第二根8/5，交点(24/5,32/5)。内部参数4/5，点(12/5,16/5)，圆幂−16。改成u=(3,−4)，第二根为负，正向射线不进入圆，但其整条直线仍割圆。

切向u=(1,0)时，正参数2处幂值为4；接点本身t=0幂值为0。不要把“切线在圆外”误读为连接点也不属于圆周。

## 文件与证据范围

- `geometry.py`：精确模型与证书。
- `test_geometry.py`：有理网格、边界和非法输入。
- `run_examples.py`：可读算例。
- `create_notebook.py`、`teaching.zh-CN.ipynb`、`verify_notebook.py`：教学与输出回放。
- `diagram.svg`：原创现代示意，W为垂足/内部见证，Q为第二交点；不充当古代原图。

源码中的投影式是现代几何重构，程序输出不认证历史解释、连续性公理、原典版本或一般量词。证书复算与测试有共享计算路径，故需另行独立技术核验，不能以自测全通过取代它。
