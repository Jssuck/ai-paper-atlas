# III.3：中心线平分弦与垂直弦的精确教学核验

配套[中文深读](../../papers/ancient/euclid-elements-iii3.zh-CN.md)。只核验III.3的现代有理坐标重构，不声称实现原典全等证明、一般尺规作图器或所有实数输入。

## 原文与实现的边界

原文正向使用I.8和直角定义，逆向使用I.5/I.26。程序另用等半径展开的恒等式：`AF_squared - BF_squared = 2 * dot_EF_AB`。在非零方向下，点积为零等价于垂直；距离平方相等等价于非负距离相等。这是现代分析表示，不是把坐标公式归于欧几里得。

输入是给定圆心E、正半径平方、不同圆周点A/B、严格介于A/B间的F。弦AB必须不经过圆心。中心线直接由E/F确定，不接收任意线再默默假定它过心；程序不负责一般求交。对固定的合法输入，`bisects`和`perpendicular`可以同时真，也可以同时假。证书中的`equivalent=True`并不意味着已经平分。

非直径条件确保EF非零。直径例的斜线可平分而不垂直，因此不能省略该条件。另一方面，直径被垂直的逆向结论本身可成立，但不属于本接口的输入范围。`perpendicular`拒绝任一零向量，避免把零点积冒充方向夹角。

`certificate(E,radius_squared,A,B,F)`产生证书；`verify_certificate(c)`重算全部字段并严格比较字段类型，拒绝布尔/整数互换及额外、缺失字段。只允许内建int及Fraction，拒绝浮点和bool。返回值是Python内存对象，含Fraction/tuple；没有声称提供JSON网络反序列化接口。

## 重跑

Python标准库即可，无第三方安装。切换到本目录运行：

```sh
python -B run_all.py
```

或分别运行：

```sh
python -B test_geometry.py
python -B -O test_geometry.py
python -B -OO test_geometry.py
python -B run_examples.py
python -B create_notebook.py
python -B verify_notebook.py
python -B draw_figure.py
```

`run_all.py`保存实际命令、stdout/stderr、退出码以及不含主机名/本地路径的环境信息。运行证据见[汇总](run-summary.json)、[环境](environment.json)、[普通测试](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)、[算例](logs/examples.log)、[Notebook执行](logs/notebook-execute.log)。测试不用会在优化模式消失的裸assert作契约。

## 本次真实结果

- 24项单元测试分别在普通、`-O`、`-OO`三模式通过。
- 每模式900个精确构形：5个尺度、3个平移、4个正交同尺度线性变换、15个弦内参数。含60个中点和840个非中点。此网格不是均匀随机试验，不穷尽圆和直线。
- 4个合法命名算例，另列直径斜线、偏心垂线、零方向三个条件反例/拒绝演示。
- [教学Notebook](teaching.zh-CN.ipynb)含5个代码格，由标准库脚本生成，以compile/exec真实顺序执行、保存输出；不是Jupyter kernel，未测试内核集成。
- [原创图](figures/chord-center.svg)两面板使用相同比例，左边中点垂线，右边斜中心线。图不代替证明；浏览器显示检查由配套审查记录说明。

## 算例与反例

半径5、圆心(0,0)、A=(-3,4)、B=(3,4)：

| F | AF² | BF² | EF·AB | 结论 |
| --- | --- | --- | --- | --- |
| (0,4) | 9 | 9 | 0 | 平分且垂直 |
| (1,4) | 16 | 4 | 6 | 两者都否 |
| (-3/2,4) | 9/4 | 81/4 | -9 | 两者都否 |

直径端点(-5,0)/(5,0)的中点是圆心，方向(1,1)的直线平分直径但不垂直。偏心垂线x=1则垂直上表弦却分成4和2。前者违反非直径，后者违反过心。支持线外点、端点、离线F、非圆周端点、重合端点都被拒绝，不能以测试失败替代几何反例的解释。

有限精确运行检查实现与例子；一般结论依靠正文的证明重建。这里既未验证欧氏公理系统的一致性，也没有自动认证未知现实圆。
