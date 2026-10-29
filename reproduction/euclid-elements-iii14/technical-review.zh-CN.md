# III.14 独立技术审查

核验日期：2026年10月29日。结论：通过。此为与正文和实现编写分离的AI辅助技术检查，不是人类专家签署或证明助理认证。

正文 SHA256：`c26ccb567995a8f49ba172ef0eb6cf9b4ab785cb0ab7460739c687394486508c`。

## 一般推导核查

- 同圆正半径、两端点不同且在圆周是必要输入规格。非直径分支先用III.3取得半弦，再用I.47得到共同平方和；正向消去半弦平方，逆向消去垂距平方。非负长度使平方相等返回长度相等，未预设待证边相等。
- 现代中点证明由两端点到中心等距展开得到正交关系，不依赖图上位置。对于任意线上点的正交分解给出唯一最近点；中点在弦内部，所以点到支撑线与弦段距离相同。
- 直径分支不对退化三角形套I.47；双直径距离均零、长度均2R，单直径分支由非直径的正平方项得到严格短于2R。没有借用尚未重建的III.15来证明III.14。
- 不等半径两个手算反例正确；根号半径明确非当前有理半径接口实跑。同半径不同圆的推广具备共同平方和条件。
- 任意内线段反例、无向距离与有向坐标的区别、等长不决定方向与唯一位置均成立。有限实验不代替上述一般实数推导。

## 已闭环的文本澄清

初稿习题3说“有直角且相同斜边”可唯一确定另一条直角边，表述可能漏读已知对应直角边。建议明确还需“一条对应直角边相等”。最终正文已补足该条件，重新阅读通过。未发现需修改的被审源码错误。

## 实现核查

`chord` 校验圆周端点及非退化后，以通用投影参数计算垂足，不把中点或本条等式作为输入筛选条件。`compare` 分开计算长度平方、距离平方相等真值，等价真不等于两个相等真。`validate` 重新计算并严格检查字段集合与规范类型，不是通用证明器；未采用可在优化模式失效的assert作为有效性检查。bool、float、非二元点、非正半径和非法端点被拒绝。数据接口为Python精确对象，非JSON或任意实数接口。

原创SVG的比例对应半径5、半弦4、距离3；它只是平行两弦的特例，不承担普遍性证明。

## 独立实跑

已分别在普通、`-O`、`-OO`模式执行以下四项，12条命令全部返回0，记录于[independent-run-summary.json](independent-run-summary.json)：

1. 原28项单测，每模式324条弦、11664对有序比较。
2. 原算例，4个同圆比较、1个不同半径反例、2个非法输入拒绝。
3. 已存Notebook的五格只读重放，实际stdout逐格相同；不是Jupyter kernel执行。
4. 独立[oracle](independent_check.py)：手选10个精确单位圆点，包含原参数网格未含的(-1,0)，3个圆心、3个半径。使用中点及行列式点线距离，而不是复制实现的投影路径；每模式405弦、18225有序比较、405端点反序、2025最近点分解、4860篡改拒绝、15非法输入拒绝。另核两种不同半径反例。

独立oracle使用显式异常检查，不因`-O`删除关键断言。样本是有限回归，不能证明覆盖所有圆、所有坐标或一般定理。

## 日志与重跑

在复现目录执行 `python independent_check.py`，优化模式可加 `-O` 或 `-OO`。执行 `python -m unittest -v test_geometry`、`python run_examples.py`、`python verify_notebook.py`可重跑相应项目。

- [普通oracle](logs/independent-oracle-normal.log)、[-O oracle](logs/independent-oracle-O.log)、[-OO oracle](logs/independent-oracle-OO.log)
- [普通单测](logs/independent-tests-normal.log)、[-O单测](logs/independent-tests-O.log)、[-OO单测](logs/independent-tests-OO.log)
- [普通算例](logs/independent-examples-normal.log)、[-O算例](logs/independent-examples-O.log)、[-OO算例](logs/independent-examples-OO.log)
- [普通Notebook](logs/independent-notebook-normal.log)、[-O Notebook](logs/independent-notebook-O.log)、[-OO Notebook](logs/independent-notebook-OO.log)

未改被审源码、Notebook、正文或已暂缓目录，未执行公开写入。本报告只验技术内容和所列运行，远端内容、链接及公式实际显示由发布环节另验。
