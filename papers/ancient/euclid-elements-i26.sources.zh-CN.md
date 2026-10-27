# Euclid I.26 来源台账

本台账区分欧几里得命题、近现代编辑注释和本文教学分析。核查日期：2026-10-27。公开内容为原创阅读记录，不附原书扫描或全文翻译。

## 1 主读文本与精确位置

| 文献 | 本次实读位置 | 核验用途 | 边界 |
|---|---|---|---|
| T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908 | 印页301末、302、303；相关注303末–306；前置ERRATA | 命题、两案完整证明、图、版本及历史评论；实际目视扫描 | 非古代手稿；未穷尽传本 |
| Richard Fitzpatrick, *Euclid’s Elements of Geometry*, revised and corrected 2008 | 印页28末至30上半，含30页脚注 | 希英并排核对命题、两案角名与边序 | 希腊底文依据Heiberg 1883–1885；未独立校勘手稿 |
| Trinity College Dublin的Heath I.26转录 | 本命题完整页面 | 对照字母与引用I.4、I.16 | 转录只作辅助，非扫描替代 |

- [Heath 1908 扫描本](https://archive.org/details/thirteenbookseu02heibgoog)。阅读位置：PDF页322–327对应印页301–306；PDF页16为ERRATA。页序是该扫描文件的页序，不是原刊页码。
- [Fitzpatrick 2008 修订版](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)。本命题印页28–30与PDF页序一致。
- [TCD I.26 转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp26_Heath1908.php)。

## 2 证明逐节点定位

| 节点 | Heath印页及边注行数附近 | 对读定位 | 本文解释 |
|---|---|---|---|
| 两角、一边，夹边或对边 | 301末第1–5行，302第6–15行 | Fitzpatrick 28末–29开头 | 固定A↔D、B↔E、C↔F |
| 第一案假AB较长、截BG、连GC | 302第16–19行附近 | Fitzpatrick 29 | 教学显写B-G-A严格介于；截取联系I.3 |
| GBC与DEF调用I.4 | 302第20–28行附近 | Fitzpatrick 29中段 | 匹配GB、BC和B处夹角 |
| 真子角等于全角的矛盾 | 302第29–32行附近 | Fitzpatrick 29中段 | 内部射线及大小规则是背景，不由图像直观替代 |
| AB相等后再次I.4 | 302第33–40行附近 | Fitzpatrick 29 | 得到AC及A处余角相等 |
| 第二案AB=DE，假BC较长、截BH、连AH | 303第41–50行附近 | Fitzpatrick 29下段 | B-H-C保证HB反向延长HC |
| ABH与DEF调用I.4 | 303第50–56行附近 | Fitzpatrick 29末–30上部 | 输出BHA=EFD |
| 外角等于内对角不可能，引用I.16 | 303第57–63行附近 | Fitzpatrick 30上部 | 三角形AHC；BCA与HCA同角 |
| BC相等后再次I.4 | 303第64–70行附近 | Fitzpatrick 30上部 | 不借用I.32求第三角 |

原文从不等选一边较大；本文把交换两个三角形处理另一方向写明，标作教学补全。原证图中的两个截取点服务于两个不同假设案，不表示不相容条件能同时作为真实模型存在。

## 3 版本校注

Fitzpatrick 30页的脚注对应29页第一案的边序：希腊文排为BG、BC，英译排列为GB、BC。按无向线段长度二者数值相同，本文说明其对应顶点的编辑意义，不把它当作定理错误。Heath本扫描所附ERRATA未列本命题所在页；仅报告所查表，不能据此断言所有版本无异文或勘误。

## 4 历史材料证据分层

- 书内先行工具：I.3截取、I.4两边夹角、I.16外角比较；I.8是相关全等判据，不是本证直接调用。
- Heath 303末谈及an-Nairizi记录的一种叠合法，并注明其作者不详；不能反推它就是欧几里得原证。
- Heath 304引Proclus（其定位p.352,13–18）转述Eudemus，把本命题联系Thales海船测距；同时明确资料不足以复原具体方法。本次实读的是Heath这条转述，不是Eudemus原稿或Proclus全书。
- Heath 304–305讨论Bretschneider、Cantor、Tannery及自己的测距重构，属于后世解释与猜想。它们不能充作Thales首创日期、确实仪器或欧几里得直接借鉴的证据。
- Heath 305–306整理后世全等分类；306强调相等边必须对应同类角色，不能夹边与对边混配。正文以原创缩放反例说明此点。

## 5 明确不归给原文的内容

ASA/AAS现代简称、坐标反例、带符号点积除绝对叉积的有理角指标、JSON证书、输入绑定攻击测试、AI验证联系均为现代教学或分析。没有以有限计算证明一般几何定理，没有以本单元宣称前史文献已经穷尽，也未将后出的I.32或正弦定理当作原证依赖。
