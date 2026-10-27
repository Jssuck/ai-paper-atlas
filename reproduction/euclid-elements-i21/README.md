# I.21 精确教学复现

此包是原创现代坐标核验，不是原典的完整形式化或一般定理的机器证明。对应[中文深读](../../papers/ancient/euclid-elements-i21.zh-CN.md)。只使用 Python 标准库，不安装依赖、不访问网络。

## 输入、构造与结论

`construct(A,B,C,D)`接受二维整数或 `Fraction` 坐标，拒绝浮点、布尔、共线三角形及非严格内部D。重心系数α、β、γ均大于0且和为1；计算 E=(αA+γC)/(α+γ)，故A-E-C且B-D-E。证书含原输入、E、重心系数、延长倍数、各平方长度和14项检查。

长度链：AB+AE>BE，CE+ED>CD；分别拼接EC、DB后得到 AB+AC>BE+EC>BD+DC。角链：BDC>CED=CEB>BAC。原文依赖I.20及I.16；本程序以根式和点积检验给定实例，不能替代那些命题及保序/传递性的证明。

`sum_compare(a,b,c,d)`比较√a+√b与√c+√d：先用两次平方的精确等式判零，非等值用整数平方根生成有理包围区间并不断加精至区间分离。无浮点容差；相等先判避免永不终止。非等值终止依赖实数平方根界收敛，不宣称固定时间上界。`angle_compare`比较[0,π]普通角，先判点积符号，再比较平方比例；不得先平方而丢失符号。

`accepted`从外部输入重新生成期望证书，以严格JSON结构比较，拒绝bool/int混同、浮点NaN、元组替代列表、额外字段、篡改和输入不匹配。它验证的是本实现的坐标证书，不是独立证明助理。

## 执行

在此目录运行 `python run_all.py`。真实执行三模式 `python`、`python -O`、`python -OO` 下测试与例集，另生成并执行Notebook。完整argv、时间、退出码见 `run-summary.json` 和 `logs/`，环境见 `environment.json`。Notebook六个代码单元由标准库逐格compile/exec，共享命名空间；未使用Jupyter kernel、未声称浏览器验证Notebook。Notebook文件由自有小型JSON生成器建立。

当前主测试每模式34项，例集每模式120正证书与12非法输入。优化模式输出需完全一致。`SHA256SUMS.json`覆盖公开附件（自身除外、缓存除外）；独立审查加入后应刷新清单。

## 文件

- `geometry.py`：精确运算、构造、证书及接受器。
- `cases.py`、`test_geometry.py`：变形、边界、类型与篡改测试。
- `run_examples.py`、`run_all.py`：可重跑命令入口和真实日志。
- `teaching.zh-CN.ipynb`、`create_notebook.py`、`verify_notebook.py`：六格教学及真实执行器。
- `WALKTHROUGH.md`：手算与证据分层。

来源定位：[Euclid I.21 原证转录](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI21.html)。本包不收录原文全文、PDF或全文翻译。
