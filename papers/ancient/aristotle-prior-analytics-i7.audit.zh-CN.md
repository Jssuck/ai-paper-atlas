# 《前分析篇》I.7：独立全文论证与数学核验

核验日期：2026-10-21 UTC。结论：**PASS，限本报告声明范围**。本审读独立检查主文全部16节、十四式表、二十题答案与来源解释；实际重新目验Owen1853印98–100和Bekker1831印29，不以搜索摘要替代原典。本报告不代替独立代码审计或发布后的真实GitHub显示验收。

## 1. 来源忠实性

完整I.7为29a19–29b28，Owen98章题至100顶部三行；没有把I.8模态内容算入。主文依次覆盖逆向结论、不定肯定替代、第一格完成、第一格全称归约、Darii/Ferio的归谬以及第三格与全章总结。Owen括入“and particular”及脚注2省略说明，与Bekker正文及装置差异被显式分开；未伪称唯一古代原文。

主文“原文主张—位置”表与账本逐项对应；最后总结定位细化为29b26–28。来源账本开头避免称所有以前章节均已完成；仅此前章节的有界背景引用，不解除I.2暂缓或计I.3完成。Owen三条编号脚注及术语/历史归属被归入译编层，不冒充作者论述。没有新增关于精确古代成书日期、全部手稿或直接AI传承的未经核实主张。

## 2. 全部主要推导的逐项检查

| 区域 | 检查内容 | 结论 |
|---|---|---|
| §4 | 主项优先记号、A/O及E/I矛盾、E/I换位、A与O换位反例 | 正确；A/E空主项兼容明确 |
| §5.1–5.3 | 原例I分支同一见证；A分支仅需B存在；空B反例；逆向O不可倒转 | 正确；没有把正反方向混淆 |
| §5.4 | “未产生原所求推论”前置限定；同质前提不被一概判无效；E条件不被误作必要条件 | 正确；第二格OA及第三格AO补例成立 |
| §6 | 不定肯定解释的语境限制；I不含O；代码不充当自然语言分析器 | 正确 |
| §7.1 | Barbara包含传递、Celarent包含与不交 | 任意集合成立，无须非空 |
| §7.2 | Darapti反设E(B,A)，Celarent得E(C,A)，用C见证冲突 | 正确，存在条件没有省略 |
| §8.1 | Darii反设E，经两次E换位和Celarent得到E(C,B)，与I(C,B)冲突 | 正确；未用Darii证明自身 |
| §8.2 | Ferio反设A，经E换位及Celarent与I冲突 | 正确；没有把I或E错当O的否定 |
| §8.3 | Festino展开Ferio；Baroco反设A后Barbara与O冲突 | 正确；无非法O换位 |
| §9 | 十四条模式方向和归约路线；Felapton、Bocardo见证来源 | 全部正确；只有Darapti/Felapton需额外中项非空 |
| §10 | 局部可靠性、证书行数归纳、反设闭合 | 正确；换位、反证和存在背景不被隐去 |
| §11 | 任意论域压缩到八种出现类型；反向可实现性；计数/关系/模态扩展限制 | 正确，一般论证与有限执行分开 |
| §12–14 | 实跑计数、原文位置、范围与延伸 | 与已存作者报告一致；不外推全逻辑完备或AI效能 |
| §15 | 全20道问题与答案 | 无方向、矛盾或存在条件错误 |

三条最容易混淆的边界特别复核：

1. “第一格全称归约”是证明路线的归约，不是删去特称前提或把特称结论改成全称。I见证在归谬末端仍必需。
2. 先以第二格解释Darii并不构成实质循环；将所用第二格全称路线展开后，只依赖Celarent和E换位。
3. “只需中项存在”的手工证明不等于程序all-nonempty策略精确只加中项存在；程序政策更强，但正文的更弱条件由一般证明单独成立。不能把程序政策与最弱充分条件混为一谈。

## 3. 独立执行证据

审计脚本[check_arguments.py](../../reproduction/aristotle-prior-analytics-i7/argument-review/check_arguments.py)不导入作者reduction实现。它以三布尔元组和Python集合重新建立模型，不调用作者语义oracle或证明搜索器。

每个模式实际完成 **9,403次显式检查**：

- 用独立集合解释复核全部768个定向后承结果，与classification.json逐项比较；59有效、709无效。
- 十四个标准模式在255个支持上做3,570次条件检查；Darapti和Felapton明确加中项非空，其余不加。
- 在三对象论域的所有三集合组合上逐行检查Darii/Ferio的局部归约、Barbara/Celarent、E/I换位及矛盾配对、原章逆向例子与Darapti的只需C存在条件。
- 另检查正文换位失败、空项兼容、I/O可以并真等具体反例。

普通、-O、-OO模式均实际运行成功，分别保存[普通结果](../../reproduction/aristotle-prior-analytics-i7/argument-review/normal.json)、[优化结果](../../reproduction/aristotle-prior-analytics-i7/argument-review/optimized.json)、[双优化结果](../../reproduction/aristotle-prior-analytics-i7/argument-review/double-optimized.json)。这些是审计自己的检查数，不与作者24个测试方法或独立代码审计数混加。

运行方式（在本实验的argument-review目录）：

```sh
python check_arguments.py
python -O check_arguments.py
python -OO check_arguments.py
```

脚本中的有限检查不替代一般规则可靠性及类型保持性证明；后者已经在主文与此处人工逐项核验。该脚本也不审计所有恶意证书、任意输入安全性或全部历史论证。具体证书核与代码故障检查见另行的[独立代码审计](../../reproduction/aristotle-prior-analytics-i7/independent-review/review.md)。

## 4. 冻结文件与限制

[绑定清单](../../reproduction/aristotle-prior-analytics-i7/argument-review/bindings.json)记录实际核验的主文、来源文件、README、走查、分类、报告和审计脚本/结果的SHA-256。内容如有变更，应重新核验相应部分再更新绑定，不把旧PASS默认为自动适用于新稿。

本次没有发现阻止发表的数学错误。页界精确化与来源完成范围措辞收紧不改变证明。实际GitHub公式、表格、链接显示，以及远端文件完整性，需要发布验收另行检查；本报告没有代替这些步骤。仅完成本章，不完成暂缓I.2、后续模态章节或整部《工具论》。
