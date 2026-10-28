# I.33 最小精确复现

本附件是原创的有理坐标教学模型，不是古代尺规操作记录，也不是完整公理化证明。只检查声明的欧氏有理平面输入及证书，不凭有限样例证明一般命题。

## 运行

仅需 Python 3 标准库；在本目录运行 `python3 run_all.py`。依次执行普通、`-O`、`-OO` 单元测试，批量算例、Notebook生成执行及输出回放。真实命令/退出码/stdout/stderr在 `logs/01.txt` 至 `06.txt`，环境在 `environment.json`，时间及命令清单在 `run-summary.json`。

本次27项测试在三模式分别全部通过；360个精确正输入、10类负输入。每类负输入直接调用 `make_certificate` 并要求抛出 ValueError，不用坏证书代替前提检查。输入族覆盖六个方向、五个切向位移、四个横向位移、三个比例；不是全部有理点穷举。

`teaching.zh-CN.ipynb` 六个代码格真实由标准库 `compile/exec` 顺序执行，保存stdout；`verify_notebook.py`再次执行并精确比对。没有启动Jupyter内核，也未验证前端交互。已读安装的Notebook技能；本地scaffold脚本未找到，使用最小nbformat4结构。

## 接口和边界

输入严格为四个键A/B/C/D，每点是两项list；坐标允许Python整数（拒绝bool）或规范Fraction字符串，如`"1/2"`。浮点、非规范`"0/1"`、额外键、tuple均拒绝。两个输入表达相同有理数视作同一几何输入，证书绑定规范化后的全部四点，而非原始字符串拼写。

前提检查：AB/CD非零、叉积为零、支撑直线相异、方向点积为正、平方长度相等。这实现同向端点配对，交叉配对会被拒绝。证书载明前提、SAS点积、中介BC和连接线结果；验证器从当前输入重新计算全部字段，并对JSON结构和叶子类型严格比对。整数或布尔值不能冒充字符串坐标或数值。它不是能接收任意证明步骤的形式证明核。

文件：`geometry.py`内核、`cases.py`输入、`test_geometry.py`测试、`run_examples.py`批量算例、`WALKTHROUGH.zh-CN.md`数学解释、`results.json`实跑结果。发布清单排除缓存；独立审查另列。
