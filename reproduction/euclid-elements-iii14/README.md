# III.14 最小教学复现：弦长与圆心距

配套[中文深读](../../papers/ancient/euclid-elements-iii14.zh-CN.md)。这是原创现代有理坐标核验，不是欧几里得原始算法、一般定理的机器证明，也不是浮点几何库。

## 输入与模型

`Circle(center, radius)` 接受整数或 `fractions.Fraction`；半径严格正。`chord(circle,A,B)` 验证端点不同且都位于圆周，再独立计算直线投影参数、垂足、全弦长平方、半弦长平方及无符号距离平方。不会把“等弦”或“等距”作为输入筛选条件。直径的垂足是圆心自身，距离为零，不构造零方向垂线。

同一圆中每弦满足“半弦平方＋垂距平方＝半径平方”，于是两弦长度平方相等恰当且仅当距离平方相等；一般证明见正文。程序检查有限实例，不以测试替代证明。不同圆的等半径推广可平移比较；删去等半径条件则有反例。

`compare` 只接受同一圆，分别计算两个等式的真值；`validate` 从证书端点重新计算并检查规范字段和类型，拒绝增删、篡改字段。接口使用Python对象而不是JSON证书；不声称通用证明器或任意实数求交器。排除bool、float和非二元点，算术不使用容差。

## 文件与命令

- [geometry.py](geometry.py)：数据验证、投影与证书。
- [test_geometry.py](test_geometry.py)：28项单测，含直径、镜像、平移、缩放、分数、端点交换与拒绝输入。
- [run_examples.py](run_examples.py)：4个同圆比较、1个不同半径反例、2个非法输入拒绝。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)：五格教学代码，已保存实际输出。
- [create_notebook.py](create_notebook.py)、[verify_notebook.py](verify_notebook.py)：生成并顺序compile/exec，以及只读回放对比stdout。**不是Jupyter kernel执行。** 已检查安装位置无Notebook模板helper，采用本地nbformat4结构，未安装依赖。
- [diagram.svg](diagram.svg)：原创示意图，不是原书复制。
- [run_all.py](run_all.py)、[environment.json](environment.json)、[run-summary.json](run-summary.json)：执行入口、环境与返回码。

在此目录执行 `python run_all.py`。仅需Python标准库；本次实际版本见环境文件。重复执行会覆盖生成的Notebook、日志和汇总。

真实运行：28单测在普通、`-O`、`-OO`三个模式通过。每模式网格使用3个半径、3个圆心，每圆9个不同参数圆周点，36条弦；总计324条弦、11664对有序弦比较。遍历是有限的有理子集，参数化漏掉一个方向，不声称覆盖全圆或连续域。4个合法比较、不同半径反例和2个拒绝例通过；五格Notebook实际顺序执行并只读回放一致。

日志：[普通测试](logs/tests.log)、[优化测试](logs/tests-O.log)、[双优化测试](logs/tests-OO.log)、[算例](logs/examples.log)、[Notebook运行](logs/notebook.log)、[Notebook回放](logs/notebook-replay.log)。日志捕获命令、真实stdout/stderr及返回码，不含账户或机器路径。

## 如何解读反例

半径5圆的弦端点(-4,3)、(4,3)，与半径4圆的直径(-4,0)、(4,0)都长8，垂距却为3和0。这不反驳III.14，而是说明同圆或等半径不可省略。反过来，不同半径两圆的直径都距圆心0，但长度未必相等。

本实验提供可复核实现和有限回归证据。独立技术审查另行检查一般推导、外部算例及篡改拒绝；审查报告与正文最终hash由发布任务绑定。
