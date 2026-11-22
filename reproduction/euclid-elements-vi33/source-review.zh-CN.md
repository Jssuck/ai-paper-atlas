# VI.33 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.6.33.html)、Heath 1908 卷 II 印刷页 273–276（图与正文起于 273，正文止于 274，校注横跨 274–276）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=191) 印刷页 191–192，以及 [Joyce VI.33](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI33.html)。各本核心题旨相同；Clay 网页英栏推得比例后停止，印本及希腊栏有题旨复述。

## 原图及推导

- 两同半径圆的圆心为 G、H。第一圆初弧 BC 对圆心角 BGC、圆周角 BAC；第二圆初弧 EF 对圆心角 EHF、圆周角 EDF。取不含圆周角顶点 A 或 D 的截弧，不把 BC、EF 理解为弦。依次复制 CK、KL 与 FM、MN，使每组同原弧；图上各三段只是示意，不要求两个任意整数倍相等。希腊圆心 Η、Θ 对英文字母 G、H。
- III.27 使同圆或等圆等弧对应等角；在图示可直接比较的范围，从两弧起点作同向对齐，大弧越过小弧终点，多出的正角给严格次序。把 m 个 BC 与 n 个 EF 连续排列，所得弧 BL、EN 分别是两弧的倍量，角 BGL、EHN 分别是原圆心角的倍量。比较弧的三种结果大、小、等，须同角的比较一致，才能用 [V.定义 5](https://mathcs.clarku.edu/~djoyce/elements/bookV/defV5.html) 建立原弧比等于原圆心角比；任意 m、n 彼此独立。
- III.20 使同弧圆心角是圆周角的两倍，再用 V.15 同倍量的比不变，得到圆周角比。VI.1 的“倍量比较”结构类似，但只可列为对读，不是 VI.33 所引前提；古证没有调用数值弧度或预设弧长等于半径乘弧度。

## 倍量、角与传本的边界

Heath 页 275 专门指出普通角大于两个直角就超出早先的术语范围；无论大小角如何约定，把累加量压缩到一对终边更会在整周丢失信息。例如以直角为单位重复相同弧五次与一次，终边相同而累积相差一整周。不能据此删去超过半周的倍量、只验证有限个整数或说古人已定义反角。现代可把弧和角都视作各正量的累加序列，用半周数和剩余量先后比较；半周内比较由同半径弧对齐和 III.27 的严格次序承担。这是教学补明，非正文措辞。Heath 页 275–276 对古人可能如何重述给出推测，不是文本事实。

Heath 页 274–275 把扇形面积扩展与 Theon 的自述相联系：Campanus 未收该增补，P 中由后手写入。Fitzpatrick 和 Clay 此处主文本均不含扇形结论。亦不可把“同比”扩大为不同半径下的弧长比较：现代相同角在半径不同时对应不同弧长。

## 可直接追查的用例

[XIII.8](https://mathcs.clarku.edu/~djoyce/elements/bookXIII/propXIII8.html) 将正五边形的两段边弧与一段边弧之比转成圆周角二倍；[XIII.9](https://mathcs.clarku.edu/~djoyce/elements/bookXIII/propXIII9.html) 把 AC 弧对 CB 弧的四倍关系转成相应圆心角四倍。这里说的是这些证明位置实际采用的转换，不据此泛称 VI.33 奠定某一现代领域。
