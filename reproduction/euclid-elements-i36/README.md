# Euclid I.36 最小精确复现

原创有理坐标教学模型：平行四边形ABCD与EFGH同两平行线且等底，使用桥EBCH连接两次同底比较。参见[数学说明与答案](WALKTHROUGH.zh-CN.md)。行列式模型不冒充原文切拼证明。

## 真实执行

在本目录运行 `python3 run_all.py`。仅Python标准库；[环境](environment.json)、[摘要](run-summary.json)记录实际命令、时间、退出码。

- 27项测试分别通过普通、`-O`、`-OO`模式。
- 1176精确正输入、10类非法几何直接拒绝；两个位置参数的重合、重叠、相接、分离及负位移覆盖。
- Notebook六代码格经标准库compile/exec实际执行及回放输出一致，非Jupyter内核复现。
- 有限运行不证明一般定理；证书核验是重算实现，不是独立形式化证明。

日志：[普通](logs/01.txt)、[优化](logs/02.txt)、[双优化](logs/03.txt)、[输入族](logs/04.txt)、[Notebook执行](logs/05.txt)、[回放](logs/06.txt)。[结果](results.json)、[Notebook回放摘要](notebook-check.json)保留实跑输出。

## 文件与范围

[geometry.py](geometry.py)提供make_certificate与verify_certificate，严格检查八点输入及完整证书绑定。[cases.py](cases.py)是确定性输入族，[test_geometry.py](test_geometry.py)含类型、篡改和移绑测试，[run_examples.py](run_examples.py)输出结果。

[create_notebook.py](create_notebook.py)构建并执行[教学Notebook](teaching.zh-CN.ipynb)，[verify_notebook.py](verify_notebook.py)回放。已读取安装Notebook技能，指定scaffold脚本实际不存在，故使用可审查标准库构建器，不安装第三方包。[摘要清单](SHA256SUMS.json)排除自身与缓存；独立审查探针由另一审查者添加。
