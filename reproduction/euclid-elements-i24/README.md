# Euclid Elements I.24：精确最小复现

这是**现代有理坐标教学重构**，不是欧几里得原证明的机器形式化，也不是全套直尺圆规模拟。两边固定且夹角严格增大时，比较第三边平方；同时覆盖 Heath 指出的图形外型、共线和内型。有限测试不证明一般定理。

## 运行

```sh
python run_all.py
```

仅 Python 标准库，无下载、安装、网络或额外依赖。`run_all.py` 实际执行普通、`-O`、`-OO` 三模式的测试和示例，然后创建及顺序执行六格 Notebook。确切命令、UTC 时间、退出码见 `run-summary.json`，完整输出见 `logs/`。`environment.json` 是实跑环境，不代表任意 Python 版本均已测试。

本轮每模式 **33 个测试方法**（其中有网格子测试）、**300 个正证书**、**21 个非法输入**。另外具名样例不计入 300。三模式结果相同。Notebook 由 `compile/exec` 执行；**不是 Jupyter kernel、nbclient 或浏览器运行**，execution_count 保留 null，用 metadata.compile_exec_index 标记顺序。已安装 notebook 技能要求的脚手架脚本在本环境预期路径不存在，故使用随包标准库生成器，未安装替代软件。

## 接口

`case(a,b,s,t,reflection)` 是面向可信教学参数的便利构造器，经 `Fraction` 归一化，可能将 True 归一化为 1；它不是不可信 JSON 的验证入口。严格类型拒绝保证针对 `certify` / `verify` 接收的原始 JSON 数据。`case(a,b,s,t,reflection)` 产生规范输入；`certify(data)` 生成证书；`verify(data,certificate)` 从绑定输入重算并进行递归严格类型比较。`load_json(text)` 拒绝重复键和 NaN/Infinity。有理数均为互素整数 `[分子, 正分母]`；拒绝 bool、float、非约分表示和额外字段。要求 `a,b>0`、`0<s<t`，reflection 为整数 ±1。API 不接受相等/反向角作为 I.24 正例。

证书保存输入、点坐标、两条底边平方、精确差、恒等式差值、余弦值、EFG 有向行列式及配置。`True == 1` 不会使篡改证书通过。证书机制只是小型可信重算器，不是独立形式化逻辑内核；其正确性仍依赖源码审查和 Python 有理数实现。

## 文件

- `geometry.py` 精确模型及验证器；`cases.py` 有限样例和非法输入。
- `test_geometry.py` 回归、输入边界、反射/缩放、证书篡改、面积反例。
- `run_examples.py` 输出配置计数及逐项有理证书；`results-*.json` 三模式实跑结果。
- `teaching.zh-CN.ipynb`、生成器及执行器；`notebook-check.json` 六格执行状态。
- `WALKTHROUGH.zh-CN.md` 数学推导、配置依据和练习。
- `SHA256SUMS.json` 除自身、缓存外的文件 SHA-256；重新运行后会更新证据与清单。

## 原文依据与范围

- [Euclid I.24，TCD 所载 Heath 1908 英译](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp24_Heath1908.php)：原命题和 I.4、I.5、I.19 依赖。
- T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I (1908), pp. 297–298，I.24 评注；外型原证、共线直接比较、内型可用 I.21。本包仅作配置检查，原文证据与译本细节见仓库正文。

本包不收录原书扫描、全文翻译或第三方代码。

## 独立技术核验

`technical_probe.py` 及 `technical-probe.json` 保存独立审查的 9750 个交点分类、72 个严格类型攻击和 3 个 JSON 攻击实跑证据。可用 `python technical_probe.py` 单独重跑；`run_all.py` 不自动运行此独立审查脚本。
