# Euclid I.35 最小精确复现

原创有理坐标教学模型：同底BC、上支持线相同的两个平行四边形A-B-C-D与E-B-C-F。完整原证解释见正文，现代模型与全部移位切拼分支见[数学说明](WALKTHROUGH.zh-CN.md)。不把行列式面积当作Euclid的原始证明。

## 真实执行

在本目录运行 `python3 run_all.py`。仅Python标准库；[环境](environment.json)、[运行摘要](run-summary.json)记录解释器、实际时间、命令及退出码。

- 27测试在普通、`-O`、`-OO`模式通过。
- 396精确正输入、9类非法几何直接拒绝；同一、重叠、端点相接、分离、负移位均覆盖。
- Notebook六代码格标准库compile/exec真实执行并回放输出一致，非Jupyter内核复现。
- [结果](results.json)、[Notebook回放](notebook-check.json)及日志保留实跑证据；有限运行不证明一般定理。

日志：[普通](logs/01.txt)、[优化](logs/02.txt)、[双优化](logs/03.txt)、[枚举](logs/04.txt)、[Notebook执行](logs/05.txt)、[Notebook回放](logs/06.txt)。

## 文件

[geometry.py](geometry.py)提供make_certificate(data)及verify_certificate(data,cert)。严格解析坐标并检查几何输入；证书完整绑定输入与分支。输入类型与精确数学范围见数学说明。

[cases.py](cases.py)提供确定性输入族；[test_geometry.py](test_geometry.py)含类型、移绑及篡改测试；[run_examples.py](run_examples.py)生成实跑结果。[create_notebook.py](create_notebook.py)构建并执行[教学Notebook](teaching.zh-CN.ipynb)，[verify_notebook.py](verify_notebook.py)回放。已读已安装Notebook技能，但其指定scaffold脚本不存在，故使用可审查的标准库构建器，不安装额外包。

[SHA256SUMS.json](SHA256SUMS.json)记录文件摘要，排除自身与缓存。独立技术审查由另行探针完成，不把本实现的自检冒充独立数学形式化。
