# Euclid I.28 最小教学复现

本附件以二维有理坐标核验两个角判据。它不是原文算法、完整中性几何公理系统或证明助理；有限测试不证明一般定理。完整原证见[中文深读](../../papers/ancient/euclid-elements-i28.zh-CN.md)。

## 模型、输入及接口

只需 Python 3 标准库，不安装依赖。`geometry.py` 的 `make_certificate(data)` 只接受恰有 E、F、B、D、case 的字典。各点是含两个**规范有理数字符串**的列表，例如 `"-2/3"`；不接受整数、布尔值、浮点、非约分字符串。case 为 `corresponding` 或 `interior_sum`。隐式 A=2E−B、C=2F−D、G=2E−F，故所需反向射线和点序已固定。

EB 和 FD 必须严格位于横截线 EF 同一侧。两分支分别检查角 GEB=EFD，或角 BEF+EFD=两直角。非零叉积保证所有角严格位于0与π之间。证书含输入完整拷贝、哈希、有符号角指标、侧向行列式、正比例系数和结论。

`verify_certificate(expected_input, certificate)` 将调用者独立给出的输入重新计算并作严格递归类型比较。证书中自报的输入或哈希不能取代调用者输入；这不是签名或身份认证。拒绝布尔值冒充整数、缺字段、多字段、元组替换列表和改绑模式。

## 实跑

从本目录执行：

```sh
python3 run_all.py
```

该命令依次执行普通、`-O`、`-OO` 下的 `python3 -m unittest -v test_geometry`，随后执行 `run_examples.py`、`create_notebook.py`、`verify_notebook.py`。每步保存命令、退出码及实际stdout/stderr到 `logs/01.txt` 至 `logs/06.txt`。环境见 `environment.json`，退出码见 `run-summary.json`。

最终实跑：32项测试 × 3模式均通过；672个正输入、12个负输入（两分支各6类）直接由生成器拒绝。正样例枚举有限斜率、两侧反射、90度旋转、平移、正有理尺度，不穷尽有理配置。近似平行负例的扰动为1/1000000，不借浮点容差放过。

`teaching.zh-CN.ipynb` 六代码格确实按顺序通过标准库 compile/exec 执行并写入捕获输出；**不是 Jupyter kernel 执行**。已读安装的Notebook技能，未找到本地模板脚本，故使用附带的标准库脚手架，不安装第三方包。Notebook内单元测试耗时可能随重跑变化。

## 文件

- `geometry.py`：精确核验与证书。
- `cases.py`、`test_geometry.py`：样例与测试。
- `run_examples.py`、`results.json`：批例及手算证书。
- `WALKTHROUGH.zh-CN.md`：一般模型推导、反例和边界。
- `create_notebook.py`、`verify_notebook.py`：可复建及执行的Notebook。
- `SHA256SUMS.json`：附件内容哈希；独立审查新增文件后由发布者最终更新。

本目录没有原书PDF、全文翻译、账户数据或私人对话。代码只核查本地输入，不访问网络。
