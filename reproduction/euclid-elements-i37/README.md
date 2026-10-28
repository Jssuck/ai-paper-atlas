# Euclid I.37 最小精确教学复现

这是原创有理坐标模型和可重算证书，不是古代尺规操作记录，也不是形式化证明器。原文先用I.31补图、I.35比较两平行四边形、I.34二分、最后取半；程序使用现代行列式作独立数值核对，不能反过来替代那条证明。

## 运行

仅Python标准库，在本目录运行 `python3 run_all.py`。依次运行 `python3 test_geometry.py`、`python3 -O test_geometry.py`、`python3 -OO test_geometry.py`、`python3 run_examples.py`、`python3 create_notebook.py`、`python3 verify_notebook.py`。真实命令、退出码、stdout/stderr见[运行摘要](run-summary.json)与[日志目录](logs/)，环境见[environment.json](environment.json)。无安装步骤、随机数或网络要求。

实际结果：27项单测三模式全部通过；672个精确正输入、9类非法几何直接拒绝；Notebook六个代码单元通过标准库compile/exec执行并回放输出匹配。不是Jupyter内核执行，不声称验证内核依赖。已读安装技能，但其脚手架脚本在执行环境缺失，采用可审查的标准库构建脚本，没有另装技能。

## 文件和接口

- [geometry.py](geometry.py)：输入解析、几何条件、证书生成/核验。
- [cases.py](cases.py)：确定性参数族，包含反射与非正交坐标基。
- [test_geometry.py](test_geometry.py)：单测和篡改测试，不依赖可被`-O`删除的assert。
- [results.json](results.json)：精确输入计数、分支及手算例证书。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)、[create_notebook.py](create_notebook.py)、[verify_notebook.py](verify_notebook.py)：六格教学与输出回放。
- [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：一般代数推导、手算及反例。

`make_certificate(data)`接收且仅接收A、B、C、D四点，点为长度2的list，坐标只允许精确int或规范Fraction字符串，例如`"1/2"`。拒绝bool、float、tuple、额外字段、非规范字符串。要求BC非零、A不在BC直线、D−A平行BC；这保证D也不在BC直线，且在同一上支持线上。允许A=D，此时使用由A与BC方向确定的上支持线而不是退化点对AD。

证书包含规范化全部输入、E/F、面积、平行叉积和两条对角线的两个半图面积。`verify_certificate`重新推导每项并比较严格JSON结构；只允许字符串/list/dict，无bool与int相等漏洞。等价坐标写法可规范化，几何平移虽然保面积，也不得复用旧证书。

有限样例只核查实现与特定输入族。证书没有证明每条古代公设、构造过程、区域有限可加性，也不能从等积推断全等或原条件必要。公开不附原文PDF、扫描或全文翻译。
