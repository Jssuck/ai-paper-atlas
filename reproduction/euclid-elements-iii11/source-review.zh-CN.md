# III.11 独立来源审查

## 核验对象与边界

本审查由未执笔正文的独立来源审查代理完成；它不是人类专家署名，也不是证明助理认证。核验对象为本仓库原创中文深读 `papers/ancient/euclid-elements-iii11.zh-CN.md`。最终正文 SHA256：`9ec27d7c93e3fc463f251e1a8ba5a5711df17f747bb0274ecd354a90c9ded8a3`。已读取并复核该版本。

本次实际阅读：

- [Heath 1908 卷II扫描](https://www.wilbourhall.org/pdfs/Heath_Euclid_II.pdf)，印刷页24–26，逐页目视正文及评注。
- [Fitzpatrick 2008修订版希英对照](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)，印刷页81–82，逐页目视完整III.11及图；并读介绍页4所说明的方括号文本标记。
- [Joyce III.11](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII11.html)，正文和Guide；[卷III定义2–3](https://mathcs.clarku.edu/~djoyce/elements/bookIII/defIII2.html)，核对接触与不穿越的用语。
- [I.20正文](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI20.html)、[III.6](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII6.html)、[III.13依赖](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII13.html)，区分原证引用、教学补足和后继用途。
- Heath所附勘误表已目视：未见针对卷II第24–26页的条目。只报告所查表，不声称不存在其他勘误。Fitzpatrick这两页没有本命题专属校正脚注。

## 逐项核对

| 项目 | 核验结果 |
|---|---|
| 书目及页码 | III.11始于Heath p24下部、正文止于p25上部；其后至p26是编辑评注。Fitz版本位于pp81–82。 |
| 延长方向 | 正文措辞出现G到F的描述，但证明与图使用F朝G并越过G。Heath p25明确补出朝内圆心方向；文章明确分辨线段与射线。 |
| 原证算式 | I.20给AG+GF>FA=FH，减去FG得AG>GH，AG=GD形成矛盾。文章把F—G—H及非共线资格显式列出，没有把图示次序当作I.20结论。 |
| D与H重合 | Heath p26允许相等，故只需GD≤GH。正文不预借唯一接点排除这一分支。 |
| Camerer与Heath | 前者的分步修补经Heath转述，后者的缩短方案另列；没有声称独立读过Camerer、August或Heiberg原著。 |
| 连续性与内含 | 古典接触的局部描述不被无说明替换成现代闭圆盘内含；文章明确模型桥接及连续性、公理化边界。 |
| 共线反向情形 | A—F—G不能套用非退化三角形的严格不等式。文章另写长度次序反证；现代补证亦统一排除该情形。 |
| 依赖关系 | III.1和I.20属于原证明结构；III.6可作教学补足；III.10、III.7–8在编辑修补中使用。III.13调用III.11，未被倒用作前提。 |
| 现代重构 | d=R−r从内含与公共点推得，再证明等价及方向；向量、闭圆盘、精确坐标都明确标为教学重构，而非古典符号。 |
| 历史范围 | 古代书籍章节定位于数学推理前史，没有称现代AI论文；没有无证据指派III.11的独立发现者，没有称图灵样稿为第一篇AI论文。 |
| 图与运行证据 | 不可能的离轴内切原图仅作反证假设图；不把它当成可同时实现的数值例。运行证据属于实现与有限输入范围，不替代一般证明。 |

## 修订记录与结论

初审要求把III.6明确标为教学补足而非原文引用，并建议改善“平方范数”措辞；最终版本已修正。定义3直链在本审查中提供，作为本审查代理的独立实际阅读记录，不声称主作者另外打开过该页面。最终绑定时已复核修改及正文来源定位。来源阅读范围足以支持本文所列主张；未复制许可不明的扫描件或全文翻译至公开附件。

来源审查结论：通过，绑定上述最终正文。新增运行统计由独立技术审查负责核实，本来源审查不把其当作原文证据。

### 显示修订复核

发布显示检查后，第三条展示公式删去冗余的点序排版尾项，公式以句点结束；点序及其严格性仍由相邻正文和第2.3节明确说明。将这一处逆向还原所得正文哈希与初审绑定版本完全一致，确认只有排版修改，数学内容及来源判断不变。此处仅重绑正文，不声称重新运行代码、测试或Notebook。
