# 原文—实现核对表

## 文献与定位

Charles S. Peirce, “On the Algebra of Logic,” *American Journal of Mathematics*, Vol. 3, No. 1 (1880), pp. 15–57。

本次阅读对象是含 JSTOR 封面的 44 页扫描 PDF；印刷页 p 对应 PDF 的第 p−13 页（从 1 开始），例如印刷 p.23 是 PDF 第 10 页，p.57 是 PDF 第 44 页。来源 PDF 的 SHA-256 见 `evidence/environment.json`。本目录不复制整份文献。已核验公开入口：[DOI](https://doi.org/10.2307/2369442)、[JSTOR 文献页](https://www.jstor.org/stable/2369442)、[Internet Archive 扫描 PDF](https://archive.org/download/jstor-2369442/2369442.pdf)、[UNAV 镜像](https://www.unav.es/gep/OnTheAlgebraOfLogicCSP1880.pdf)。

公式读取流程：先读全文 OCR 定位，再查看扫描页中的上划线、上下标和复合运算标记；OCR 不能用来决定否定位置。重点图像核对页为 23、33、36、38–42、47–48、52–53、55–57。

## 逐项对应

| 印刷页 | 核对内容 | 实现/实验 | 声称与限制 |
|---|---|---|---|
| 23 | A/E 不含存在承诺；I/O 有存在承诺；原图四区域 | `categorical`；教程第 1 节 | 精确有限集合语义，不把图改成传统存在承诺版本 |
| 33–37 | +、×、补集、分配与展开；p.36 式 (26) | `shannon`；类代数穷举 | 点值布尔重构；一般定理不靠有限测试证明 |
| 33 | 式 (8) 的局部推导声称 | `m3_meet`、`m3_join` | M₃ 说明单独的上下界规则不足；不是对全部历史前提的形式化结论 |
| 38 | 由所有完整取正/取负组合构造展开；“prime factors”例子 | `cnf_from_truth_function` | 原文术语不等于现代最小素蕴含式；不依赖原文通用计数公式 |
| 39 | 第四过程，对同一字母正/负出现配对消元 | `eliminate`；trace | 现代布尔 CNF 实现，穷举验证存在投影；不自动处理 I/O 存在证人 |
| 39 | Boole 算例原始三个前提 | `boole_original` | 直接依据图像转录；不是依据 p.40 有误的 OCR/中间展开 |
| 40–41 | 消去 v、去冗余，得到六前提；再消 x 后无 y,z,w 独立限制 | `boole_six_clauses`；全部 16 行核验 | p.39 对 v 的直接枚举与 p.41 六式相符 |
| 42 | 最后的摘要式 | `boole_printed_summary`；反例集合 | 只是一方向必要条件；和六前提不等价，保留原式揭示差异 |
| 42–44 | 理想个体、简单项、无限数组/相对宇宙 | 有限关系作为教学替身 | **不复现**连续性或极限；有限原子不冒充原文全部哲学解释 |
| 45–46 | converse 交换相对项/关联项 | `Relation.converse` | 只实现二元逆关系，不实现全部高元排列代数 |
| 47 与 57 注 | 对角/非对角分类及 0/top 例外 | `Relation.classify` | 严格按定义补上末页勘误；退化有限域额外说明 |
| 48 | 5 种三元相等模式；1,2,5,15,52,203 的计数列 | `equality_patterns`、`bell_numbers` | 现代解释为集合划分；独立 Stirling 递推核对，未照抄难辨长式 |
| 50–52 | 三标记、取补转换、四种运算及其输入包含方向 | `compose`、`regressive`、`progressive`、`transadd` | 明确定义后独立量词 oracle 与单调性测试 |
| 53 | lover/servant 例释，否定是方法 | 教程量词解释 | 不凭英文例句猜操作，先以 p.52 的符号规则确定 |
| 55 | 八个简单肯定分配式 | 4,105 个全部小域三元组 | 对各自的正确运算成立；普通复合不能对交集任意分配 |
| 56–57 | 简单结合与发展结合的区别 | 普通复合结合律 + 混合运算反例 | 此行为主模块范围，**不声称主模块已验证全页发展式**；另附40核心等式补充见下节 |

## 避免静默修复

### p.42 摘要漏掉一个方向

实现保留四个独立对象：

- p.39 原始前提 `boole_original`
- 从它重构的 CNF 消元结果
- p.41 六个前提 `boole_six_clauses`
- p.42 原样显示摘要 `boole_printed_summary`

前三者在当前有限布尔语义的全部 16 个剩余赋值上相符。正确投影也可现代化简为 x=F，其中 `F=z¬w ∪ ¬zw ∪ ¬y¬z¬w`。最后的原样摘要只等价于 F⊆x，丢失另一方向，额外接受 1011、1100、1111。这是有限反例，不需要把“未检出反例”等同一般证明。

### p.38 的“数量公式”不作为算法依据

原文给出 `2^m+n−mp−p` 的通用计数式。实现直接枚举真值行。比如 `(a∨b)∧(c∨d)` 有 m=4、n=4、p=2，该式给 10，实际满足赋值数为 9。不要把这个公式当作任意表达式展开的可靠项数，也不要把“prime”误译成现代最小项数。

### p.57 勘误优先于前面粗略互斥叙述

p.57 “NOTE TO PAGE 47” 明说 0 同时属于 concurrent 与 alio-relative，top 同时是两类的 negative。实现没有硬编码一张忽略 0/top 的互斥分类图。

## 标准与来源边界

- 所有代码为本项目原创；不声称作者在 1880 年提供过算法源码。
- “CNF”“resolvent”“Stirling recurrence”“Bell numbers”等是现代解释语言，不作为 Peirce 本文已经使用这些现代名称的证据。
- 当前扫描版本只覆盖 pp.15–57，末尾印有 “To be continued.”；不能由本目录的实现推论后续文本的全部范围。
- 见同目录 README 中的精确计算范围，以及独立审查文件（如随整套发布物提供）。

## 独立关系表补充

[公式附录](../../papers/1880/peirce-relative-formulae.zh-CN.md)完整列出40条现代核心等式与条件；[补充脚本](supplemental_relation_checks.py)及[evidence日志](evidence/supplemental-relation-checks.log)在二元素论域检查其转写，不并入17个主测试方法。原印p55否定简单表右首行使用并而应为交，单独保留反例；没有声称原印全部否定变式逐字通过。p54坐标疑误与最终正确结论同样分别报告。
