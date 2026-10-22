# I.20 最小教学复现：见证是否真的进入结论主项

本目录是原创现代教学代码，不是 Aristotle 的算法、古代文本的唯一语义，也不是一般定理的实验证明。只使用 Python 标准库。

## 1 模型和 API

`Model(n, worlds)` 的对象为 `0,...,n-1`；世界是非空元组，第一个世界为实际世界0，每个世界是 `(A,B,C)` 三个位掩码。`n` 必须是正整数，掩码必须在论域内；布尔值不当整数接受。模型不可变，不暗设每个词项非空。模型容许同样外延的两个世界；这不是两世界必定不同的框架。

`holds(mode, quantity, predicate, subject)` 始终是“谓项对主项”，不要把 A 对 B 读反。数量 `a/e/i/o` 分别为全肯/全否/特肯/特否。

- D：只在实际世界计算。
- P：对实际主项对象逐个找某个世界，使谓项有指定极性。不同对象可用不同世界。
- N：实际主项对象在所有世界都具有指定极性；主项范围不随世界改变。
- C：实际主项对象的谓项属性在世界间至少真一次、假一次。因而 C_a=C_e、C_i=C_o。否定这里不是“非C”。
- BOX：每个世界分别量化该世界的主项，然后要求相应实然命题在每个世界成立。BOX_i 的见证可以随世界变化，N_i 的见证不可变。

`varying(X)` 返回 X 曾真且曾假的对象集合。全称对空主项为真，特称为假；任何需要存在的测试显式加条件。对象论域非空，词项可空。

## 2 核验的命题和故意保留的失配

一般数学证明见主稿；以下程序仅检查有限边界。

1. 换质：C_a(X,Y)=C_e(X,Y)，C_i(X,Y)=C_o(X,Y)。这是我们定义中双向偶然性的性质，不是普通实然A/E等价。
2. 全称见证桥：C_a(A,C)且实际 C 与实际 B 有交集，推出 C_i(A,B)。B的模态前提不是这条充分条件所必需。
3. 特称见证桥：C_i(A,C)且实际 C 包含于实际 B，推出 C_i(A,B)。更精确的充分条件是实际 C、实际 B、A的变化对象三者有交集。
4. 不加桥时，第三格原文归约链并非在这个现代模型中普遍有效。程序分别保存“全称偶然转置到特称”“第一格形式”“第三格双全称”“双特称”失败的首个见证，不把失配删除或改称成功。

这些桥接是教学补充的充分条件，不冒充原典公设或原文已承认缺少的前提。它们不是 C_i(A,B) 的必要条件；见证可能来自实际 C 之外。

## 3 九个具名实例

`examples()` 的实例及每项实际真假见各 `results-*.json`。

- `all_actual_terms_nonempty_universal_failure`：U={c,b}对应位0、1。实际 C={c}，B={b}，A={c,b}；另世界 C={c}，B={c,b}，A={b}。两条C_a前提真，但实际B对象b始终是A，故C_i(A,B)假。实际三项均非空，不把失败推给空名词。
- `bridge_success`：共同实际对象落C及B，A有真有假，结论成功。
- `separate_particular_witnesses`：A偶然对象为0，B偶然对象为1，两个“某个”不能自动合并为一个见证。
- `necessary_inclusion_background` / `necessary_exclusion_background`：双C_i前提均真，实际B对象分别对A恒真/恒假，故N_a或N_e成立而目标C_i失败。这是Owen两组自然词例结构的集合重构，不是自然科学经验验证。
- `worldwise_inclusion_not_anchored_necessity`：A与B在每世界同延，但实际B对象可以以后不再是B，故BOX_a真而N_a假。不能用BOX_a背景自动反驳锚定C_i。
- `no_joint_positive_world`：同一对象分别可A、可B，却没有任何世界同时A且B。不能合并不同世界的可能性见证。
- `empty_middle`：显露存在条件。
- `actual_membership_not_modal_conversion`：实际桥足以使结论成立，但C是稳定谓项，故C_i(C,B)假。教学桥不等于偷偷接受原文模态换位。

## 4 命令与真实环境

实际运行环境见 `environment.json`。在本目录执行：

```sh
python3 -m unittest -v test_model
python3 enumerate_models.py
python3 -O -m unittest -v test_model
python3 -O enumerate_models.py
python3 -OO -m unittest -v test_model
python3 -OO enumerate_models.py
```

没有安装新包，也不要求Notebook。校验用显式异常及unittest，不依赖优化模式会删除的assert语句。

## 5 本次实跑

正常、`-O`、`-OO` 每模式均通过16项单测。枚举 `(对象数,世界数)` 为 `(1,1),(1,2),(1,3),(2,1),(2,2)`，共4744配置；每模式查询853920次，换质等价检查85392次。三模式JSON报告逐字一致。

- 全称桥808次前提满足，特称桥808次，精确见证桥1064次，均无失败。
- 换位1488候选、852失败。
- 第三格双全称及非空中项728候选、284失败。
- 第一格形式1188候选、268失败。
- 双特称1240候选、508失败。

这里“候选”是相应前提在一个配置中为真，“失败”是目标C_i为假。并非论文或古代逻辑的错误率，不把不同世界数配置当统计样本，也不声称只有这些配置可能失败。单测同时检查输入拒绝、空项、单世界、量词次序和原文例结构。

`logs/tests-*.txt` 是真实标准输出/错误日志；`logs/enumeration-*.txt` 记命令；`logs/results-*.json` 是各次实际程序输出。`author-manifest.json` 绑定作者附件，独立审查另存并不在作者manifest范围。
