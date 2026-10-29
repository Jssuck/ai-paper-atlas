# III.7：偏心内点到圆周的距离核验

本目录是原创的现代有理坐标教学重构，配合[中文深读](../../papers/ancient/euclid-elements-iii7.zh-CN.md)。它不是Euclid原文程序化实现，不是一般几何证明器，也不以有限网格证明普遍命题。

## 模型和接口

仅需Python 3标准库。所有算术使用`fractions.Fraction`，输入接受整数、有理数字符串和Fraction，不接受float、bool、NaN。二维点、轴向量必须有两个坐标。

`certificate(center, radius, offset, axis, point)`：给中心O、正半径r、偏移d、有理单位向量u及圆周点P。要求0<d<r，令F=O+du；P不能是轴端点。返回JSON可存档证书，含近端D=O+ru、远端A=O−ru、镜像H、距离平方及严格余量。

`verify(c)`：从证书输入重新计算，按规范JSON结构和类型比较；篡改、额外字段、缺项等返回False。它检查自包含坐标的一致性，不认证输入来自真实测量或正确抄录。若把输入和全部结果一致地换成另一个合法实例，验证通过是预期行为。

`compare(center,radius,offset,axis,p,q)`：两个不同非端点，须位于轴的同一开半圆。输出轴投影差与距离平方差的精确关系。它不计算Euclid文字里的“更靠近”的角度；现代投影排序与原证角序的关系须阅读正文证明。

`circle_point`是有理参数族生成器，使用((1−t²)/(1+t²),2t/(1+t²))再旋转和平移，不是一般圆线求交。它不枚举全体圆周点，遗漏参数无穷处的轴端点；测试中不使用t=0产生的另一端点。

## 一般数学依据与实现边界

令x=(P−O)·u，且|P−O|²=r²。直接展开给FP²=r²+d²−2dx。非轴端点有−r<x<r，所以FP²−(r−d)²=2d(r−x)>0，(r+d)²−FP²=2d(r+x)>0。代码核验这些精确量，恒等式的一般推导不依赖运行次数。

H=O+2xu−(P−O)与P有相同轴投影、相反垂直分量，且FP²=FH²。在二维中给定距离平方先唯一决定x，圆方程再给垂直分量的两个相反根；非极值时两根不同。这是“恰两点”的一般现代证明。程序只保存已给有理P的镜像，不求任意指定距离对应的根，不将两个样本冒称穷尽所有可能点。

圆心d=0时所有圆周点等距；端点d=r和外点d>r不在本API域。P为A或D时等距点只有一个，证书接口明确拒绝，极值端点仍由合法证书列出。不把零向量视为角的方向。

## 真实运行

在此目录运行：

```sh
python3 run_all.py
```

脚本实际执行的逐条命令、返回码与日志见[run-summary.json](run-summary.json)，运行环境见[environment.json](environment.json)。本次：

- 24项unittest在normal、`-O`、`-OO`三模式均通过，各模式检验504构形；包括平移、四个轴方向、三个半径、三种偏移比例、七个有理参数。
- 五个命名实例和一组同半圆排序见[examples.json](logs/examples.json)。基本例O=(0,0)、r=5、d=2、P=(3,4)：FP²=17，最小9，最大49；H=(3,−4)，两余量8和32。
- 类型敏感篡改、重复点、两侧半圆、中心、边界、外点、非单位轴、端点、非圆周点等测试可查[test_geometry.py](test_geometry.py)。本次测试数量不等于覆盖全部输入。
- [Notebook](teaching.zh-CN.ipynb)的五个代码格实际由标准库`compile/exec`依次运行，再只读重放逐字比对保存输出；**不是Jupyter kernel执行**，execution_count保持null。见[执行日志](logs/notebook-execute.log)、[回放日志](logs/notebook-replay.log)。用户可以在Jupyter中另行运行，但本次未声称做过该项。

## 文件和图

- [geometry.py](geometry.py)：精确模型与核验接口。
- [run_examples.py](run_examples.py)：命名算例。
- [create_notebook.py](create_notebook.py)、[verify_notebook.py](verify_notebook.py)：可重复生成和验证Notebook。
- [draw_figure.py](draw_figure.py)：原创同尺度SVG。[查看图](figures/iii7.svg)。图经本地渲染目视检查，不是原典扫描。

无外部数据集、训练、基线模型或统计指标；不据此声称完整复现古典尺规过程、一般定理自动证明或现代AI能力。日志不包含私人路径、账号或原文PDF。
