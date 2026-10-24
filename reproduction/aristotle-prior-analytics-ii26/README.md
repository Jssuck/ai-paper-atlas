# II.26 最小教学复现：反对意见何时真正反驳前提？

配套[原创深读](../../papers/ancient/aristotle-prior-analytics-ii26.zh-CN.md)与[来源台账](../../papers/ancient/aristotle-prior-analytics-ii26.sources.zh-CN.md)。本目录为原创现代集合语义核验，不是古代程序、心理实验或完整历史复现。原文的共同科学、相反与相对分类只是论证材料；本程序不认证这些材料的事实真假，也不为版本异读裁决。

## 1. 模型和问题

论域是 $`D=\lbrace i\in\mathbb{Z}:0\le i<n\rbrace`$；允许空域和空项，是显式的现代边界测试政策，不冒称古代唯一解释。集合 $`A,B,C\subseteq D`$ 编码为整数位掩码。$`B`$ 始终为被反驳命题的主项，$`A`$ 为谓项；上位或下位关系由证书给出，不由名称猜测。

四种命题分别为：

$$
\mathrm A(B,A)\iff B\subseteq A,\quad
\mathrm E(B,A)\iff B\cap A=\varnothing,
$$

$$
\mathrm I(B,A)\iff B\cap A\ne\varnothing,\quad
\mathrm O(B,A)\iff B\setminus A\ne\varnothing.
$$

A/O与E/I是精确矛盾；A/E不是无条件矛盾。上位路线可以推出一个真的全称命题，却在空主项时没有反驳其全称反对命题。`certificate()`因此分别报告`accepted`（前提全真）、`conclusion_true`与`rejects_target`。结论碰巧真而前提不成立，不算有效证书。

## 2. 核验的六条路线

| 标识 | 显式前提 | 结论 | 要反驳的目标 |
|---|---|---|---|
| `upper_negative` | $`B\subseteq C`$ 且 $`C\cap A=\varnothing`$ | E(B,A) | A(B,A)，须B非空才真正反驳 |
| `lower_negative` | $`\varnothing\ne C\subseteq B`$ 且 $`C\cap A=\varnothing`$ | O(B,A) | A(B,A) |
| `upper_positive` | $`B\subseteq C\subseteq A`$ | A(B,A) | E(B,A)，须B非空才真正反驳 |
| `lower_positive` | $`\varnothing\ne C\subseteq A\cap B`$ | I(B,A) | E(B,A) |
| `second_negative` | $`A\subseteq C`$ 且 $`B\cap C=\varnothing`$ | E(B,A) | A(B,A)，须B非空才真正反驳 |
| `first_particular` | $`B\cap C\ne\varnothing`$ 且 $`C\subseteq A`$ | I(B,A) | E(B,A) |

前四条是本章上位/下位路线的教学重建；后两条检查解释边界：第二格能够有有效的否定推理，第一格能够得特称结论。不能把本章对“直接异议”的分类读成一般逻辑禁止这两件事。这里不模拟对话者觉得哪个新前提足够直接或可信。

### 一般推导为何成立

- 上位负路线：任取B中的对象，它在C；C与A无交，所以它不在A。B若非空，该对象也给出反A目标的见证。
- 下位负路线：从非空C选对象，它在B且不在A，故O成立。
- 上位正路线：任取B中的对象，先到C再到A。B非空时又给出I，排除E目标。
- 下位正路线：从C选对象，同在A和B，故I成立。
- 第二格负路线：若对象同时在B和A，则由A包含于C知它在B和C，矛盾。非空B才保证排除A目标。
- 第一格特称路线：取B与C共同见证；它由C包含于A而属于A，仍是同一对象，得I。

这些逐对象论证覆盖任意集合（取见证只用既给定非空集合），不依赖有限实验。有限枚举只能发现本次编码/界限内的反例。

## 3. 反模型与输入检查

`test_objections.py`包含16项测试，使用在优化模式仍生效的`unittest`断言方法与显式异常，不使用Python的裸`assert`作为验证条件。

- 空B：A/E都真，I/O都假；已得E不能当作已经反A。
- 空C：不能冒充下位路线的存在见证。
- $`A=\lbrace1\rbrace,B=\lbrace0,1\rbrace,C=\lbrace0\rbrace`$：下位负路线成立，O真但E假，不能把一个反例升级为“所有B都非A”。
- $`A=C=\lbrace0\rbrace,B=\lbrace0,1\rbrace`$：下位正路线成立，I真但A假。
- 错向包含、前提假而结论碰巧真均被拒为证书。
- 参数拒绝负数、超界集合、非法域大小、把布尔值冒充整数及不存在的路线名称。

`n`限制为0–8是低成本运行保护，不是数学限制。默认0–4足够展示本章的边界；超过默认范围不声称已跑。

## 4. 重跑命令、环境与真实记录

只需Python标准库和Bash，不安装依赖：

```bash
cd reproduction/aristotle-prior-analytics-ii26
bash run.sh
# 单项检查也可：
python3 -m unittest -v test_objections.py
python3 objections.py --max-n 4
```

`run.sh`依次运行普通、`-O`、`-OO`模式，将命令与测试输出保存到日志，再比较解码后的JSON结果。环境见[environment.json](environment.json)：本次CPython3.12.14、Linux x86_64；无随机性、无外部数据、无需网络。重新执行会覆盖本目录的运行日志，这是为了让读者核验自己的运行，不保证时间耗时字节一致。

- 测试：[normal](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)。每模式16测试通过。
- 枚举：[normal](logs/results-normal.json)、[-O](logs/results-O.json)、[-OO](logs/results-OO.json)。
- [模式比较](logs/comparison.log)。三模式语义结果完全相同，耗时不作为语义比较字段。
- 源码：[objections.py](objections.py)、[测试](test_objections.py)、[运行脚本](run.sh)。

## 5. 本次结果与计数口径

域大小0–4中，每个对象有A/B/C八种成员组合，因此总世界数为：

$$
\sum_{n=0}^{4}2^{3n}=1+8+64+512+4096=4681.
$$

这是带标签的有限世界数，包含同构重复；不是不同逻辑类型数。每个世界检查六路线，路线的计数允许重叠。

| 路线 | 前提全真 | 结论失败 | 真正反驳目标 | 空B而未反驳 |
|---|---:|---:|---:|---:|
| upper_negative | 341 | 0 | 220 | 121 |
| lower_negative | 440 | 0 | 440 | 0 |
| upper_positive | 341 | 0 | 220 | 121 |
| lower_positive | 440 | 0 | 440 | 0 |
| second_negative | 341 | 0 | 220 | 121 |
| first_particular | 774 | 0 | 774 | 0 |

A/O与E/I精确矛盾检查失败数为0。`empty_subject_nonrejections`不是程序错误；它展示现代空项政策下全称“反对”未必互斥。

## 6. 不支持的结论

没有实验数据集、学习算法、预测指标或现代基线可在本章忠实复现；本次适用的是证明重建、有限反模型与实现交叉核验。不声称覆盖古代完整认识论，不证明前提真实，不测量异议的说服力或对话成本，不证明无限域定理。独立审查与独立实现见[独立核验附件](audit/README.md)及配套技术审查，不能把作者的自测称为独审。
