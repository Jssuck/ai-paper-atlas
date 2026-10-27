# Euclid I.29 最小教学复现

本附件以二维有理欧氏坐标检验平行直线被截时的三个角结论。它不是原文算法、完整公理系统或证明助理。有限测试既不证明一般定理，也不证明第五公设的独立性；坐标模型已经选定欧氏结构。原文的第五公设反证见[中文深读](../../papers/ancient/euclid-elements-i29.zh-CN.md)。

## 输入、角色与接口

Python 3 标准库，无第三方依赖。`geometry.py` 提供 `make_certificate(data)` 和 `verify_certificate(expected_input, certificate)`。输入恰含 G、H、B、D，每个点是两个规范有理数字符串的列表，例如 `['-2/3','1']`。不接受整数、布尔、浮点、未约分或含空白形式。隐式定义 A=2G−B、C=2H−D、E=2G−H、F=2H−G，使 A-G-B、C-H-D、E-G-H-F 的射线角色固定。

令 t=H−G、u=B−G、v=D−H。输入须满足 det(t,u)、det(t,v)非零且同号，及 det(u,v)=0。前两项确保截线、交点和各射线非退化，B、D严格在截线同侧；后项是模型中的平行假设。它们还保证两被截直线互异，且 v=λu 的比例 λ>0。交换或反向射线会改变角的身份，不被悄悄归一化。

输出包含完整输入、输入SHA256、两个侧向行列式、正比例、有符号角指标和三个结论。角指标使用 cos 的符号和 cos²的精确有理数；只比较平方会把锐角和钝角混淆。核验器以调用者独立提供的expected_input重新计算，严格递归检查JSON类型与字段，拒绝True冒充1及列表/元组替换。哈希不是签名或身份认证。

## 运行与真实证据

从本目录执行：

```sh
python3 run_all.py
```

依次运行普通、`-O`、`-OO`三个模式的32项单元测试，批例、Notebook生成与执行。`logs/01.txt`到`06.txt`保留真实命令、退出码、stdout/stderr；`run-summary.json`和`environment.json`记录本次运行及环境。

本次三模式全通过。有限族含336个正确输入、8个负输入；每个负输入直接调用生成器并要求抛ValueError，不以空证书失败代替前提检查。族覆盖7种斜率、3种正尺度、2侧方向、4次四分之一旋转和2种平移。近似平行扰动1/1000000被精确拒绝，不用容差。

`teaching.zh-CN.ipynb`六代码格按顺序通过标准库compile/exec真实执行并保存输出，**不是Jupyter kernel执行**。已读取安装的Notebook技能，检查其本地helper路径及工作区未找到脚手架，因此采用自有标准库`create_notebook.py`，不安装依赖。Notebook重跑仅测试耗时等可变输出可能不同。

## 附件

- `geometry.py`：输入验证、精确角指标、证书及核验器。
- `cases.py`、`test_geometry.py`：有限样例及32项测试。
- `run_examples.py`、`results.json`：真实批例与手算样例证书。
- `WALKTHROUGH.zh-CN.md`：一般模型推导和负例解释。
- `create_notebook.py`、`verify_notebook.py`：可重建及执行Notebook。
- `SHA256SUMS.json`：文件内容哈希；独立审查追加后由发布者最终更新。

只含原创教学代码与解释；不包含原书PDF、全文翻译、账户资料或私人对话。代码不访问网络。
