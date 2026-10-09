# 一手来源与实现对照

## 文献

Henry Maurice Sheffer. “A Set of Five Independent Postulates for Boolean Algebras, with Application to Logical Constants.” *Transactions of the American Mathematical Society* 14, no. 4 (October 1913): 481–488.

- 本次实际阅读的公开扫描：[Internet Archive / JSTOR 扫描 PDF](https://archive.org/download/jstor-1988701/1988701.pdf)。PDF 第1页为 JSTOR 封面，第2–9页为印刷页481–488。
- [JSTOR 稳定记录](https://www.jstor.org/stable/1988701)；[JSTOR DOI 10.2307/1988701](https://doi.org/10.2307/1988701)。
- [AMS DOI 10.1090/S0002-9947-1913-1500960-1](https://doi.org/10.1090/S0002-9947-1913-1500960-1)。AMS 网页本次访问返回403；书目信息通过 Crossref 核对，内容依据上述实际取得的扫描，不把403页面当作已读正文。
- 阅读用 PDF 大小：189,381 bytes。
- 阅读用 PDF SHA-256：`7636eddef1ea4eefd03eb5b131d5455d148ca5d881bf7891ef24f3c0eeda6154`。

## 定位到页

| 印刷页 | 本次 PDF 页 | 复现内容 |
|---|---:|---|
| 481 | 2 | 脚注中的 rule、K-rule 与 K-closed 的区分 |
| 482 | 3 | 五条公设、prime 定义及 P3–P5 的 K 元素条件 |
| 483 | 4 | 一致性表、五个独立性解释及 P5 三元素表 |
| 487 | 8 | rejection 的 neither–nor 解释；NOT、OR 的定义 |
| 488 | 9 | 命题形成规则的约简；末条脚注中的对偶 NAND 解释 |

第482、483、487、488页均直接检查过页面图像，不只依靠 OCR。特别核对 P5 表的行顺序 l,m,n，三行为 `(l,m,n)`、`(n,n,l)`、`(m,l,m)`，以及 P5 右边 prime 的位置。

## 原文和现代重构的边界

- **原文数学内容**：五公设、一致性及独立性模型、有理数运算、NOR 主解释、NOT/OR 约简、NAND 对偶脚注。
- **本项目新增实现**：guarded AST evaluator、outside-K sentinel、精确线性系数类、完整小表枚举、递归语法翻译器、测试、JSON 结果及 Notebook。
- **本项目新增教学解释**：用类型假设解释 P2 容易被遗漏的原因；用结构归纳说明递归翻译器为何保持语义；用真值编码区分 NOR 与 NAND。
- **未复现的证明任务**：没有把原文 pp.483–486 的完整演绎证明编码成形式化证明对象，也没有用一般定理证明器重证其 Boolean algebra 表示结果。小型枚举不是替代证明。
- 这里的 independent 指原文逐条独立性：对每条公设给出满足其余四条的反模型。程序不声称检查所有公设真假组合都可实现的更强“完全独立性”。
