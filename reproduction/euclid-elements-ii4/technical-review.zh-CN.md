# Euclid II.4 独立技术审查

结论：**通过所声明范围的技术审查**。2026-10-28独立检查；这不是证明助理认证或人类专家背书，不把有限执行替代一般几何证明。

## 绑定终稿

- 正文：`papers/ancient/euclid-elements-ii4.zh-CN.md`
- 正文 SHA256：`3d3e811063cfd3b5c00fda4dcc55f1ca54f3d4c141251bdca00e7ef925852fd7`

## 数学与教学核对

完整重读正文原证、教学坐标、手算反例、多段推广和练习。BD是对角线，GH不是；CF与BD交于G，HK必须过G。I.29/I.5/I.6依次承担平行角、等腰角、等角对等边；I.34补小块对边，等边与直角分别建立。HF的补证通过AD=AB、AH=CB同减得HD=AC，再用HG=AC和直角，未偷用面积恒等式。AG/GE是余形，HF/CK才是关于对角线的两方块。I.43条件与四区无重叠覆盖分别说明。

现代模型的交点解G=A+t·u+(1−t)·v、内部参数、非奇异坐标覆盖和面积映射正确。整数/分数/旋转算例、反射、错误HK、外切和斜菱形反例手算通过。多段推导按对角格与成对非对角格解释，明确不列为代码已测功能。Heath平方差评注的AF=A-D-F-C及FK=F-E-K-G区域与共同边AC一致。原证、后世路线、现代数域扩展、有限运行分层清楚。

初审发现正文称原创图上下翻转，但SVG实际保留A上D下；已修正后重读。独立目视原创图：BD经过G，四块4、9、6、6标号与区域正确，未见文字交叠。网页最终数学渲染由发布阶段另验，本审查不冒称完成远端渲染验收。

## 实现与真实独立执行

读核全部Python源码、结果与Notebook执行方式。`verify`未调用`construct`，逐点逆解仿射坐标并绑定规范有序边界；非零等长垂直及内部参数先验后计算，面积不是筛选假设。参数格覆盖检查依赖已经核实的实际顶点绑定，固定格并非单独足以证明任意输入覆盖。面积使用Fraction；生产检查显式异常，不被优化模式删除。

独立新增[检查脚本](independent_check.py)，正例不调用作者构造器：从B、D、C等边端点与BD参数构造G，再得H/K/F，按平方长度及分段比例计算面积oracle。五方向、三尺度、双定向、两平移、四切点形成240构形。各模式分别实跑：

| 统计 | 每模式结果 |
| --- | ---: |
| 外部生成有效证书 | 240 |
| 五区域面积对照 | 1200 |
| 点位/区域边界/整体平移等篡改拒绝 | 6480 |
| 非法输入、坏类型、错切线及非规范边界拒绝 | 42 |

三命令`python independent_check.py`、`python -O independent_check.py`、`python -OO independent_check.py`均真实退出0；[summary](independent-run-summary.json)、[normal日志](logs/independent-normal.log)、[-O日志](logs/independent-O.log)、[-OO日志](logs/independent-OO.log)保存证据。6480+42=6522是每模式拒绝次数，不是定理数量；三模式复用同一测试族，不能冒称三倍独立数学覆盖。

另实际重跑作者18项unittest与Notebook回放，退出0；主运行保存的18项三模式、64网格构形、七命令及四算例与正文一致。Notebook五代码格为标准库compile/exec及新命名空间输出对照，未启动Jupyter kernel；保留null执行编号，不宣称内核/前端模式验证。

## 边界

这是普通整数/Fraction输入的有限审查，不证明不可通约长度或全部古代公理，不防任意恶意Python对象/无限资源消耗。规范边界要求固定顶点顺序，循环换名虽同几何区域仍按合同拒绝；并非宣称几何上不等价。类型验证与篡改族不穷尽所有程序缺陷。来源归属另见独立来源审查。

## 已核源码 SHA256

- `create_notebook.py`：`01b73ec88659f80574e119f8a62729c1c50b39d23ed0a46231a4a67f58cb2424`
- `draw_figure.py`：`6f621aaeff2a9dc74d85a1f80a0c72ae0b898a04c8a02ee2934d4878a81cbc02`
- `geometry.py`：`02043ebafc137d55f2b52e97871ae3855f9cf62335cf64820bcb3fb50caf8249`
- `independent_check.py`：`0f5a2c3bfc43eeef8cc578496d6d590c4eea177ca9134a06d3922616a1250ce3`
- `run_all.py`：`f72e762811292db30cc0c529d99a29a5cb57055479c02006ab0e41d738089a0b`
- `run_examples.py`：`9d69102860c691969046ba887910f3bf9c50eab9da0d1e6288be177d6ac7870e`
- `test_geometry.py`：`e3fccbf6f9f207aef670ad2ea95e1870f101f5269295a034b8d09f9b69889ae3`
- `verify_notebook.py`：`74eb42c0bd52ac77401c3c26dace5c0873927ec5912d65d36aa2cdbdf5a21a55`
