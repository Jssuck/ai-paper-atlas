# Euclid I.34 最小精确复现

本附件是原创欧氏有理坐标教学核验，不是完整古代几何形式化，也不是机器学习实验。原图边界A-C-D-B，对角线BC。输入条件、对应边角、三角形分割与面积使用精确分数核验；原证与现代解释见[数学说明](WALKTHROUGH.zh-CN.md)。

## 真实执行

执行命令：在本目录运行 `python3 run_all.py`。仅Python标准库；具体解释器/系统见[环境](environment.json)。[运行摘要](run-summary.json)保存真实开始结束时间、命令、退出码和日志路径。

- 27项单元测试分别普通、`-O`、`-OO`通过，禁用assert优化不影响测试结论。
- 576个精确正输入、9类非法几何输入；负例直接调用make_certificate要求抛出ValueError，不靠传空证书制造拒绝。
- Notebook六代码格真实标准库compile/exec执行，再回放比较输出一致；不是Jupyter内核执行，也不声称内核环境复现。
- 实跑结果见[results.json](results.json)；Notebook回放见[notebook-check.json](notebook-check.json)。这些有限运行不证明一般定理。

日志：[普通测试](logs/01.txt)、[优化测试](logs/02.txt)、[双优化测试](logs/03.txt)、[枚举](logs/04.txt)、[Notebook生成执行](logs/05.txt)、[Notebook回放](logs/06.txt)。

## 文件与接口

- [geometry.py](geometry.py)：make_certificate(data)、verify_certificate(data,certificate)。输入恰好A/B/C/D四个键，点为两个坐标的list，坐标是整数或规范分数字符串（如"1/3"）。拒绝bool、float、Fraction对象、非规范字符串与额外键。所有输出数值为字符串。
- [cases.py](cases.py)：576例生成族与9类几何反例；不声称均匀抽样或穷尽。
- [test_geometry.py](test_geometry.py)：27项测试，含关系、面积、类型和攻击。
- [run_examples.py](run_examples.py)：精确枚举和结果生成。
- [create_notebook.py](create_notebook.py)、[verify_notebook.py](verify_notebook.py)：生成六格并执行、独立重放。
- [教学Notebook](teaching.zh-CN.ipynb)：包括真实输出。已读安装Notebook技能；环境未找到配套new_notebook.py，故使用本附件标准库构建器，不安装额外包。
- [SHA256SUMS.json](SHA256SUMS.json)：文件字节摘要，清单不含自身。

## 核验边界

程序以两对方向平行及非退化性推出合法平行四边形，而非把待证等长预设为输入。证书绑定完整规范化输入和全部派生量，严格JSON叶类型比较。现代行列式面积不冒充Euclid原面积演算；有限例不证明平行公设可以删除。对角相等、等长、等面积是不同结论，不能互相无条件替换。独立技术审查及其额外探针在正文配套审查文件说明，不把这些测试当人类专家或证明助理认证。
