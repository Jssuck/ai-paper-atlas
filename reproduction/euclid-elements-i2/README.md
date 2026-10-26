# 《几何原本》I.2：规范族见证与独立约束检查

这是本仓原创教学代码，不是原文算法的逐操作机械化实现，也不是通用尺规引擎或证明助理认证。`exact.py` 的有理系数 `a+b√3` 工具由本仓 [I.1 教学实现](../euclid-elements-i1/euclid_i1.py) 改编；其余为本单元新增。

## 输入、模型与输出

`construct(s,r,side=1,offset=(0,0))` 接受正有理数 s、r，反射方向 ±1 和有理平移。未平移时 D=(0,0)，A=(s,0)，B=(s/2, side·s√3/2)，C=B+(r,0)。BC 是已给定非零线段，C 是输入族的一部分；这不是把待复制的长度预先搬到 A。

函数以坐标公式产生 G=(1+r/s)B、L=(s+r,0)。这使用解析表达式生成教学见证，不能把其代码运算称为只执行欧氏原始作图操作。独立 `certificate(points)` 不读取 s、r，不使用生成公式；它检查等边框架、以 B 为心经过 C 的圆、D—B—G 的向外顺序、以 D 为心经过 G 的圆、D—A—L 顺序及最终长度。两圆半径均由圆心和已经存在的点局部给出。检查器核验几何约束，不认证程序调用的原始操作历史，也不证明古代公设足够保证全部交点存在。

该族有任意正有理边长比、两个反射方向和有理平移；不覆盖所有旋转或一般实坐标输入。Q(√3) 并不对任意尺规构造所需平方根封闭。一般性由正文证明讨论，不由有限测试宣告。

A=B 时另用 `coincident_anchor(A,B,C)` 返回 C，因此 AC 就是原给定 BC；B=C 的零线段不在本题非零规格中。一般分支 s=0 不可代入，函数明确拒绝。输入拒绝浮点数、布尔值和字符串，避免把近似数说成精确数。

## 手算例与反例

s=2、r=1、side=1：D=(0,0)，A=(2,0)，B=(1,√3)，C=(2,√3)，G=(3/2,3√3/2)，L=(3,0)。距离平方 AB²=4、BC²=1、DG²=9、AL²=1。检查器全部通过。

把 G 改为 B/2=(1/2,√3/2)，仍有 BG²=BC²=1，却不满足 D—B—G 顺序：取对圆而取错分支，不能继续使用原加减长度证明。把 L 改为 (−3,0)，仍在以 D 为心经过 G 的圆上，却不满足 D—A—L，且 AL=5 而非1。真实输出保存在 [results.json](results.json)。

## 真实执行与范围

- CPython 版本及命令见 [environment.json](environment.json)，仅标准库，不安装依赖。
- 25 项单元测试在普通、`-O`、`-OO` 三模式分别通过；断言使用 unittest 而非可被优化关闭的裸 assert。
- 有限枚举 s,r 各取 1/3、1/2、1、2、3，反射方向两种，平移三种，共 150 组，零约束不一致。
- 测试包含半径大小关系、平移反射、错交点、错射线、错框架、零线段、重合锚点、输入类型与精确运算。枚举与测试不能证明一般命题。
- [tutorial.ipynb](tutorial.ipynb) 五个代码单元实际按顺序通过标准库 `exec` 执行，共享命名空间并保存输出；不是 Jupyter 内核执行、nbformat 全模式验证或页面渲染。采用仓内已有合法 Notebook 结构作为模板，因为本地未找到技能脚手架。

## 重跑

进入本目录后执行：

```sh
python3 -m unittest -v test_euclid_i2
python3 -O -m unittest -v test_euclid_i2
python3 -OO -m unittest -v test_euclid_i2
python3 euclid_i2.py > results.json
python3 run_notebook.py > logs/notebook.log
```

真实日志：[普通](logs/tests.log)、[优化](logs/tests-O.log)、[双优化](logs/tests-OO.log)、[Notebook](logs/notebook.log)。改变代码或参数后应重新生成证据，不沿用旧输出冒充新结果。源码：[模型](euclid_i2.py)、[精确算术](exact.py)、[测试](test_euclid_i2.py)、[Notebook执行器](run_notebook.py)。
