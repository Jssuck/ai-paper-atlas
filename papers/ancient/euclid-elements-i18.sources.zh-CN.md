# Euclid《几何原本》I.18：来源、版本与论证位置

对应[中文深读](euclid-elements-i18.zh-CN.md)。约公元前300年是作品传统年代估计，不是本命题独立发现时间。本单元属于几何与推理前史补读，并非现代AI论文，收录不声称穷尽。书内依赖顺序也不等于历史发现顺序。

## 实际核读

| 来源 | 位置与方式 | 使用范围 |
|---|---|---|
| [Heath1908第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908，印283–284上，PDF304–305；目视扫描 | I.18正文全部位于印283；该页下方及284页最上方是语词、历史和替代证明评论。284页主体已属I.19，不计为I.18正文。档案标识中的02不是卷号。 |
| [Fitzpatrick希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick, *Euclid’s Elements of Geometry*, 2008修订纠正本，印/PDF22中段；目视排印及文本提取 | I.18题面、图和完整证明。页上是I.17续文，页下开始I.19。现代编译排印不是古代手稿。 |
| [TCD Heath I.18转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp18_Heath1908.php) | 完整命题与引据 | 交叉核对扫描，不视为独立古代见证；转录不包含Heath全部评论。 |
| [Joyce I.18导读](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI18.html) | 命题、证明及语序导读 | 核对I.18与I.19的条件方向及现代英语说明；导读不是欧几里得原文。 |

**勘误范围。** 已目视Heath扫描PDF16的ERRATA，未见印283–284条目。这个结论只针对所查勘误表，不保证全部版本没有其他错误。Fitzpatrick的“修订纠正”标签也不等于所有细节绝对无误。

## 主张与证据定位

| 主张 | 证据 | 边界 |
|---|---|---|
| 已知AC大于AB，欲证ABC大于BCA | Heath283题面与设定；Fitzpatrick22 | 条件由边序到对角序；不能颠倒为后篇I.19的证明，也不以“看起来同义”省略方向。 |
| 在长边上截出AD=AB并连接BD | Heath283证明首句、I.3引据；Fitzpatrick22 | 截取的是从A起的部分；A-D-C的严格中间关系使后续外角与内部分角成立。 |
| ADB是三角形BCD的外角，严格大于DCB | Heath283中段、I.16引据；Fitzpatrick22 | DA与DC为相反射线，BCD非退化；不需要后续外角等于两内角和定理。 |
| AB=AD使ADB=ABD | Heath283中段；Fitzpatrick22明确I.5引据 | 等腰三角形ABD的底角相等；不是把所欲证明的大边大角关系先当作角比较规则。 |
| DCB与ACB为同一普通角 | 原证由DCB转写ACB处 | 因D在AC内部，CD与CA为同向射线；不能只凭共线就认定角相同。 |
| ABC严格包含ABD，由此结束不等式链 | Heath283末两步；Fitzpatrick22末段 | “更大”是严格序传递，不提供固定倍数或数值差额。BD在ABC严格内部的点序依据须在教学展开中说明。 |
| I.18、I.19的题面语序标记已知量与待求量 | Heath283第一段评论；Joyce Guide | Heath将先给数据后给目标作为区分重点；英语主动/被动的表面近似不能抹掉互逆方向。 |
| Aristotle引文 | Heath283语词评论，转述 *Meteorologica* III.5, 376a12 | Heath说引的是I.19的结果及措辞；此处未独立通读该部原典，不能据此声称Aristotle证明I.18或确定其首创者。 |
| Porphyry替代证明 | Heath283末–284首，转述Proclus315.11–316.13 | 改从C端截CD=AB，再延AB至E使BE=AD，得AE=AC；用等腰与外角链结束。属于Heath转述的历史替代方案，不归为欧几里得本命题原证。 |

## 历史替代方案的范围

Heath报告的方案先令CD=AB，然后从B向外延长AB到E，令BE=AD。因为AC=AD+DC而AE=AB+BE，故AE=AC，三角形ACE等腰。于是AEC=ACE；ABC是三角形BEC在B的外角，严格大于AEC；而ACE包含ACB，故再传递得到所需比较。该方案改变的是辅助对象的布置，不是删除等腰、外角或点序前提。

## 现代重构与公开范围

- 坐标、正平方根、二次扩域、行列式、角排序算法和机器证书均是现代教学核验，不归给原作者。
- 余弦公式或反三角函数可作另一路现代检验，但不能偷换原证、形成对I.18/I.19的循环论证。
- 本单元不完成I.19、全部《几何原本》或AI前史，也不声称恢复唯一古代形式系统。
- 阅读PDF和扫描页只作研究核验，不公开上传；此台账为原创概述及必要链接，不是全文翻译。

最终来源审查及正文哈希绑定见[独立来源审查](euclid-elements-i18.source-audit.zh-CN.md)。代码和实跑另由技术审查核验。
