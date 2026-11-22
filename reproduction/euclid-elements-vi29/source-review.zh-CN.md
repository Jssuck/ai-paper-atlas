# VI.29 原典与证明核对

核对 [Clay 希腊文与 Heath 英译](https://www.claymath.org/library/historical/euclid/files/elem.6.29.html)、Heath 1908 卷 II 印刷页 265–267、[Fitzpatrick 2008 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=187) 印刷页 187–188（图在 187 页）、[Joyce VI.29](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI29.html)。这些材料的主要证明一致。英文图号以下依 Heath／Fitzpatrick。

## 原图与面积链

1. 将 AB 二等分于 E（I.10）。在 EB 上作同模板 D 相似且同样布置的小平行四边形 BF（VI.18）；应用 VI.25 作 GH，使其也同 D 相似且面积等于 BF 加目标面积 C；这里是**加**，不是 VI.28 的减。GH 面积大于 BF，所以对应边 KH>FL、KG>FE；由 VI.20 的相似面积平方比可以补明此步。沿 FL 和 FE 原方向延长至 M、N，得 FLM=KH、FEN=KG，再补出 MN；MN 与 GH 同面积且同形。
2. BF、FB、EL 是同一原小图，因为 B、F 和 E、L 各是两对对角点。MN 与 EL 都同 D 相似（VI.21），且 EL 内含于 MN，公共角在 F、同样布置；VI.26 使 F、B、O 共线。由 MN=EL+C，曲尺形 XWV=MN−EL 的面积为 C，XWV 不是三角形的三个顶点。
3. 图中 NB、LP 是大平行四边形内关于共同对角线的两块互补图，面积由 I.43 相等。AN 与 NB 沿 AB 的底边 AE、EB 相等且同高，故 AN=NB（Heath 标 I.36，Fitzpatrick 标 VI.1，两条路线可得同一结果）。于是 AO=AN+EO=LP+EO=曲尺形 XWV=C。
4. AO 超过 AB 的块是 QP，而不是面积辅助块 MN 或 GH。QP 与 EL 都在 MN 的共同对角线 FO 上，由 VI.24 相似，故 QP 与输入模板 D 相似。

## 斜坐标检查

取 F 为原点，第一轴沿 FL，第二轴沿 FE，以固定模板的边比和夹角吸收进坐标基底；令 m=AB/2，t>0 为超出 AB 的底边。于是 F=(0,0)、L=(m,0)、E=(0,m)、B=(m,m)、M=(m+t,0)、N=(0,m+t)、O=(m+t,m+t)、P=(m+t,m)、Q=(m,m+t)、A=(−m,m)。面积为坐标面积乘同一正因子 k。由此核对：

- NB 与 LP 面积同为 kmt，EO 面积为 kt(m+t)；
- AO 面积为 kt(2m+t)=k[(m+t)²−m²]，QP 面积为 kt²，且 k 是模板的面积除以对应底边长度平方；
- 目标面积 S>0 时，t=√(m²+S/k)−m>0，另一代数根小于零，不代表超出长度。这里没有 VI.28 的面积上界；若 S=0，得到退化 t=0，不在正图形设定内。

## 文本和历史边界

- Clay 在线英译止于 AO=C，最后对超出块 QP 的相似性核验在同页希腊文仍可读，也见 Heath 印本、Fitzpatrick 第 188 页及 Joyce。希腊图第 187 页用 Ξ 对应英文 O、Π 对应英文 Q、Ο 对应英文 P；不能机械按字形对应。
- Fitzpatrick 第 188 页脚注的二次式使用无量纲变量，与正文尺规叙述区分。Heath 第 266–267 页以矩形为例作现代代数解释，并指向《已知量》59；第 267 页还提到已知夹角时的菱形特例与《已知量》84，以及正方形超出情形与 II.6 的联系。VI.30 紧接着把 VI.29 用于超出部分为正方形的情形；这是原文依赖，不是把现代代数记号投回古代。
