# Euclid I.38：等底三角形的精确教学核验

这是原创的现代有理坐标小模型，不是对古希腊文本的形式化认证，不以有限实验代替一般证明。正文见[中文深读](../../papers/ancient/euclid-elements-i38.zh-CN.md)。

## 原证明与代码的边界

原文先用 I.31 作平行线，补成 GBCA、DEFH 两个平行四边形，再以 I.36 得到整体等积，以 I.34 得到对角线 AB、DF 两侧各半，最后比较两半。本程序没有证明 I.31、I.34、I.36；它在已经选择的现代有理平面模型中，用精确行列式检查构图与面积等式。绝不能把通过几个算例说成完成欧几里得一般定理复现。

- [geometry.py](geometry.py)：严格输入、非退化与共同支持线前提、构图、证书与完整输入重新绑定。
- [cases.py](cases.py)：5个坐标框架 × 6个底偏移 × 6组顶点参数 × 2种底方向 = 360个正例；另有8个非法几何输入。
- [test_geometry.py](test_geometry.py)：32个测试方法，包含360正例族、全部证书叶字段篡改、同面积异输入移绑、类型/schema错误和重合边界。
- [results.json](results.json)：汇总、一个基础算例、6种边界算例及8个拒绝原因；不保存360条大而重复的证书。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)：5个代码格的教学Notebook。
- [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：构图与接口逐步解释。

## 输入契约

`make_certificate(data)` 接受且只接受 `A,B,C,D,E,F` 六个键。每个点为长度2的 `list`，坐标是 Python 真正的 `int`（不包括 `bool`）或规范有理数字符串，如 `"-2/3"`、`"0"`。不接受浮点、Fraction对象、None、元组点、`"2/4"`、`"0.5"`、带空白字符串或额外字段。规范整数 `0` 和字符串 `"0"` 有意视为同一数学输入。

拒绝零底；拒绝 BC、EF 不在同一支持线；拒绝底长不同；拒绝 A 在底线上；拒绝 D 不在通过 A 且平行于底的同一条支持线上。最后两项共同保证两个三角形非退化、两顶点同侧且同高。异侧等高的等积实例仍不符合本命题前提，直接拒绝而非悄悄“修复”。

**允许**等底反向、同底、底交叠、顶点沿支持线任意平移，以及 A=D、B=F、G=H 等跨标签重合。标签重合不等于面积退化，但原图的 AD、BF、GH 线名可能失效；代码用非零底向量及其平行支持线表示几何对象，而不是把同一点的两标签当作一条线。

证书中所有数值统一输出规范有理数字符串。`verify_certificate(data, cert)` 重新校验输入并计算**全部**证书，严格检查证书值类型，作完整序列化比较。它会拒绝同面积但顶点/底位置不同的移绑，也拒绝 `True` 冒充 `1`。字典键顺序无关。该方法是可重算的教学证书，不是数字签名、防恶意资源耗尽沙箱或不可信超大输入服务。

## 环境、运行与真实证据

仅用 Python 3 标准库，没有安装第三方包。具体本轮版本与UTC时间见 [environment.json](environment.json)。从本目录执行：

```sh
python run_all.py
```

实际依次执行的六条命令及退出码见 [run-summary.json](run-summary.json)：

```sh
python test_geometry.py
python -O test_geometry.py
python -OO test_geometry.py
python run_examples.py
python create_notebook.py
python verify_notebook.py
```

本轮32测试在三种模式各通过一次；正常与优化模式都直接拒绝不合法几何，因为输入检查不是会被优化移除的 `assert`。真实标准输出/错误保存在 [normal](logs/tests.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)、[算例](logs/examples.log)、[Notebook生成](logs/notebook-build.log)、[Notebook重放](logs/notebook-replay.log)。测试方法数不等于独立定理数，三种模式重复也不扩大数学覆盖。

已读取安装的 Notebook 技能；其本地 `new_notebook.py` 不存在，资源读取也未成功，因此使用随附原创 [create_notebook.py](create_notebook.py) 生成标准 Notebook JSON。**真实执行是标准库 `compile/exec`，不是 Jupyter kernel**。生成器顺序执行5格并保存stdout；[verify_notebook.py](verify_notebook.py) 在新的命名空间从头重放并逐格比对stdout，[notebook-check.json](notebook-check.json) 保存结果。它验证当前代码格可顺序执行和已存输出一致，不声称浏览器Notebook界面或kernel协议已测试。

[SHA256SUMS.json](SHA256SUMS.json) 是本目录文件的内容清单（不包含它自身及缓存目录）；重新运行会因环境时间和测试耗时变化而更新日志及摘要，这是预期行为。
