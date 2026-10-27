# Euclid《几何原本》I.20：来源、版本与论证位置

对应[中文深读](euclid-elements-i20.zh-CN.md)。约公元前300年是作品的传统年代估计，不是本命题单独发表或发现的日期；本单元属于几何与推理前史补读，不是现代AI论文。书内依赖次序也不等于发现年代次序。

## 实际核读范围

| 来源 | 实读位置 | 边界 |
|---|---|---|
| [Heath1908第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908；印286下–288，PDF307–309，逐页目视 | I.20题面、图与原证在286下–287上；287–288是Heath评论及三种历史替代证。286上仍属I.19，289已属I.21。档案标识02不是卷号。 |
| [Fitzpatrick2008希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick, *Euclid’s Elements of Geometry*, 2008修订纠正本，印/PDF23下–24上；实际文本提取及排印目视 | 23下为题面、图与设定，24上为完整证明及结论。此为现代翻译排印，不是直接核读古代手稿；不含Heath长篇史注。 |
| [TCD Heath I.20转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp20_Heath1908.php) | 完整题面、证明及I.5、CN5、I.19引据，在线读取 | 与扫描核对的便利转录，不是独立古代见证；不含Heath评论。 |

**勘误检查。** 已目视Heath扫描PDF16的ERRATA，未见印286–288条目。这只限定于读到的勘误表，不是对所有版次无误的保证。Fitzpatrick标明修订纠正，也不意味着可以跳过实际核对。

## 主张—证据对应

| 主张 | 原文或评论位置 | 使用方式 |
|---|---|---|
| 任意两边合起来大于剩余一边 | Heath286题面；Fitzpatrick23下 | 是非退化三角形中的严格结论，须覆盖三种配对，不是只比较某两边。 |
| 延长BA到D，并使AD=AC，连接DC | Heath286构造段；Fitzpatrick24上 | B、A、D按此顺序共线，A在线段BD内部。Fitzpatrick在等长设置处标I.3；Heath此句未另标命题。延长后有足够长度及截取的存在属于构造所需条件。 |
| 等腰三角形ADC给出角ADC=ACD | Heath286，标I.5；Fitzpatrick24上 | 这是原证明的等量桥梁，不依赖待证的三角不等式。 |
| 角BCD严格大于角ADC | Heath286，标共同概念5；Fitzpatrick24上 | 先用ACD是BCD的真部分，再替换为等角ADC；角内部位置不能仅凭图像宣布。 |
| D处射线DA与DB相同；I.19给DB>BC | Heath286末段；Fitzpatrick24上 | 因B-A-D顺序，ADC与BDC是同一普通角；要在三角形DCB中配对正确的对边。 |
| 将DB换成BA+AC，再交换标签得其他两式 | Heath287上；Fitzpatrick24上 | 使用线段拼接与AD=AC。其余两式是同一证明重标号，不是把一式作任意代数倒置。 |
| 驴子故事及“感知”与“证明”之别 | Heath287首段，转引Proclus p.322 | 只是Heath报告Proclus关于伊壁鸠鲁派的说法，不能当作独立核实的事件、首创权或现代心理实验。 |
| 不延长原三角形边的三种替代证 | Heath287–288，转述Proclus pp.323–326，提及Heron与Porphyry | 是后世评论中的历史方案，不是欧几里得本命题原证。Heath以整体归属叙述，不宜凭此把每一种方案分别断言归某一作者。 |

## 历史替代证明的实读内容

第一种是直接证明：以AD平分顶角A且D落在BC内。在ABD中，角ADC作为外角大于BAD；由BAD=DAC，I.19给AC>CD。同理AB>BD，将两不等式相加得AB+AC>BD+DC=BC。角平分线与对边相交且落在内部是位置条件；这条路线不等于可以调用后来角平分线比例定理。

第二种仍是直接证明，分等边、等腰、不等边情形。关键难例是底边为最大边：在BC上截BD=AB，连AD，以两处I.16外角比较及角量相减得到角ADC>CAD，再由I.19得AC>CD，加上AB=BD收束。Heath随后说明不等边可按长短排序，把难比较化到同样的截取路线；不能把“不难的两式”误当成第三式也已证明。

第三种是反证。设BC为最大边，对AB+AC=BC和AB+AC<BC分别排除。等号情形在BC上截BD=AB，余段DC=AC；两个等腰角关系会使A角等于两直角，与I.17（及另一内角为正）不容。小于情形分别从B、C截取BA、CA等长段，在B-D-E-C的顺序下，用等腰关系与I.16得到同一角和既相等又严格更大的矛盾。这里的点序与严格性仍须论证，不能把有限坐标样例当作此历史方案的完整形式化。

## 公开与推论边界

- 现代向量、单二次域、根式符号判定、严格JSON证书和有限枚举属于教学重构，不倒写进古代正文。
- 距离或范数的三角不等式、折线路径、逆三角不等式可以作为后续分析；不能先把它们当公理，再声称重建了I.20原证。
- 原证明及历史替代证不使用余弦定理或三角形内角和等于两直角；本单元不会以这些后来结果替代原典依赖链。
- 扫描与PDF仅用于内部阅读；公开只留原创解析及必要书目链接，不附原件或全文翻译。收录不代表I.21、全书或AI前史已完成。

最终正文哈希见[独立来源审查](euclid-elements-i20.source-audit.zh-CN.md)。
