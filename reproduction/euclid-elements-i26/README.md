# Euclid I.26：两角一边的精确有限核验

本目录是[中文精读](../../papers/ancient/euclid-elements-i26.zh-CN.md)的原创教学附件。它**直接计算给定有理坐标的前提与结论，不是 I.4/I.16 原始反证的形式化证明内核，不是完整复现《几何原本》**。它不产生关于所有三角形的实验性证明。

## 输入与范围

`triangle_1` 依次是 A、B、C；`triangle_2` 依次是 D、E、F。每个顶点为两项列表，坐标必须是 `"0"`、`"-2"`、`"3/5"` 等规范有理数字符串。整数、浮点、布尔值以及 `"2/2"` 均拒绝，避免混合类型及非规范表示。

两案都要求 B 与 E、C 与 F 内角相等。`side_case="included"` 另外要求 BC=EF；`side_case="opposite"` 另外要求 AB=DE（对 C、F）。对于给定 AC=DF 的对边情形可交换 B、C 及 E、F 化归，程序接口不另设第三分支。共线或重复点不属于输入域。

[geometry.py](geometry.py) 使用标准库 `Fraction`，以边长平方避免开平方；角键为两个顶点射线向量的内积除以行列式绝对值，因而保留锐角、直角、钝角符号。见[推导与手算](WALKTHROUGH.zh-CN.md)。代码不计算浮点角度、不用近似容限、不调用正弦定理。

## 实际执行及复跑

在此目录运行：

```sh
python3 run_all.py
```

该命令实际依次执行普通、`-O`、`-OO` 三种模式的单元测试，运行例子，生成并顺序执行 Notebook。具体命令、退出码和 stdout/stderr 在 [run-summary.json](run-summary.json)、[logs](logs/)；环境在 [environment.json](environment.json)。仅需 Python 标准库，无额外安装。

- [test_geometry.py](test_geometry.py)：29 项测试，每种模式均通过；包括两案、镜像、钝角、异常格式、严格布尔类型、输入绑定及真正的 SSA 反例。
- [results.json](results.json)：216 个正例全部验收，4 类不满足前提输入拒绝；保存两份完整示例证书及负例输入。216=36 种形状 × 3 种有理等距变换 × 2 个分支，不是 216 个独立随机实验。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)：六个代码单元，真实标准输出已嵌入。
- [notebook-check.json](notebook-check.json)：在新 Python 进程的共享命名空间中依次 `compile/exec` 六个单元。**不是 Jupyter kernel 执行，不声明 nbformat 完整模式验证或浏览器 Notebook 渲染。** Notebook 由随附标准库脚本生成，未安装任何依赖。

## 证书契约

`make_certificate(input)` 重新计算前提及三边/剩余角结论。`verify_certificate(expected_input, certificate)` 必须接收调用者独立持有的预期输入，重新计算整份证书并逐字段、逐类型比对，不能只相信证书内的输入或摘要。`True` 不能代替 `1`；额外字段、丢失字段、另一合法输入的证书均拒绝。

SHA-256 只用于识别输入内容，不提供认证签名。全部判断依赖此坐标实现及 Python 算术的可信性；不覆盖实数坐标全部情况、解析器拒绝服务安全性、形式证明可靠性或第三方 Notebook 内核兼容性。修改代码或数据后应重跑并重新生成日志，不能沿用旧证据。
