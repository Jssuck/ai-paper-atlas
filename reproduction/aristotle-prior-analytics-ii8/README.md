# II.8：结论替换与反驳目标——最小教学复现

这是原创 Python 标准库教学程序，不是古代作者的程序，不是全文翻译，也不是完整三段论或自然语言证明器。正文的逐步一般证明与程序角色分开：小实验核对规则、反模型和存在条件，不能单凭枚举证明任意论域的定理。

## 语义与输入

`('U', P, S)` 表示 S 包含于 P；`E` 表示二者不交；`I` 表示交非空；`O` 表示 S 中有元素不属 P。顺序始终为**谓项、主项**。`opposite` 的 `contradictory` 映射 U↔O、E↔I，为该现代语义的布尔否定；`contrary` 沿本章用语映射 U↔E、I↔O，不宣称所有配对互斥。

非空论域内，每个对象有 A、B、C 三个真值，编号 bit0=A、bit1=B、bit2=C。`frozenset` 给出实际出现的类型；类型0是三项都不属的对象，不是空论域。只保留每种出现类型一个代表，得到255种非空类型集合；过滤 C 非空有240种，三项均非空有218种。对本程序一元四类命题，重复同类型对象不改变真假；这说明代表缩减的根据，而不是把枚举本身当成一般证明。模型不处理关系、数量词“恰好两个”、模态或命题态度。

模型必须是非空 `frozenset`、元素为0–7的整数（拒绝bool），命题须为合法三元tuple。验证先于短路求值，生成器会先物化，避免尾部非法命题被短路隐藏。校验使用显式异常而非会被 `-O` 删除的assert。

## 运行

在本目录执行；无需安装依赖：

```sh
python model.py
python -m unittest -v test_model
python -O -m unittest -v test_model
python -OO -m unittest -v test_model
```

[环境](environment.txt) · [完整命令](logs/commands.txt) · [normal测试](logs/test-normal.txt) · [-O测试](logs/test-O.txt) · [-OO测试](logs/test-OO.txt) · [normal矩阵与反模型](logs/run-normal.json) · [-O矩阵](logs/run-O.json) · [-OO矩阵](logs/run-OO.json)

## 实际结果与解释边界

实际运行10个测试在normal、`-O`、`-OO`分别通过；三份矩阵逐字一致。每种存在政策含四个第一格式×两种替换×保留前提位置的16行，共48行。输出同时列：替换后假设、被移除的原前提、其严格矛盾目标、该章重构的结果、可满足模型数、结果反模型数、反驳反模型数以及首个见证。所有48行假设均有模型，不把空前提集合上的真空有效性冒充证据。

- 8种矛盾替换均在允许空项的政策下反驳被移除前提。
- 4种全称结论相反替换在 C 非空时均可反驳。若允许 C 空，这4种反驳均有反模型；其中保留大前提的2种仍能推出 E(B,C)，但 E(B,C) 与 U(B,C) 在 C 空时可同真。保留小前提的2种特称结果自身也需要 C 非空。
- 4种特称结论相反替换都不能反驳被移除前提，即使三项非空，每行仍有16个反模型。保留大前提时能推出 O(B,C)，但不能据此否定 I(B,C)；保留小前提时，被移除大前提的有序项对 A,B 上四类命题均不被蕴涵。

“无有序项对四类后果”只限定这个候选语言，不表示没有任何逻辑后果；`entailed_ordered_pair_results`也不是完整证明搜索。语义模型不把被移除的原前提继续当假设，否则会把“寻找反驳”误变为直接矛盾。

## 阅读来源与核查责任

程序设计实读[Jenkinson英译第8章电子转录](https://en.wikisource.org/wiki/The_Works_of_Aristotle/Prior_Analytics/Book_II)及[Owen1853卷I](https://archive.org/details/Aristotles_Organon_vol_01_1853)印199–201扫描。此处只给原创抽象及必要链接，不重发扫描与译文。来源校勘、一般证明和独立审查见[深读正文](../../papers/ancient/aristotle-prior-analytics-ii8.zh-CN.md)。

## 独立技术复核

独立审查使用[不同实现的量词oracle](independent_check.py)，不调用作者`holds`来计算真值；核对48行计数、候选后果和反模型，并重跑三种模式测试。[normal独立结果](logs/independent-normal.json) · [-O独立结果](logs/independent-O.json) · [-OO独立结果](logs/independent-OO.json) · [normal复核测试](logs/reviewer-test-normal.txt) · [-O复核测试](logs/reviewer-test-O.txt) · [-OO复核测试](logs/reviewer-test-OO.txt) · [审查结论及SHA256绑定](../../papers/ancient/aristotle-prior-analytics-ii8.technical-review.zh-CN.md)。

独立检查命令：`python independent_check.py`、`python -O independent_check.py`、`python -OO independent_check.py`；复核测试命令与上列三个unittest命令相同。日志均来自实际执行，不是预期输出模板。
