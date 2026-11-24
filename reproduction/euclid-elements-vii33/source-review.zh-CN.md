# VII.33 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.33.html)、Heath 1908 卷 II 印刷 333–335 页（物理 346–348；图在 333，收尾和评注在 335）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=219) 印刷 219–220 页（图在 220），以及 [Joyce VII.33](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII33.html)。

输入 A、B、C；D 是全组最大公量；希文 Ε、Ζ、Η 对应英语 E、F、G，为按位置构造的测量次数；Θ、Κ、Λ 对应英语 H、K、L，为反证中的较小同比列；Μ 对应 M，为该列测量原列的共同次数。Heath 指出，希文的“每一个量每一个”要按位置读，绝非要求 E、F、G 各自整除所有原数。第一分支的“互素”是**全组**无非单位公量；例如 6、10、15 全组最大公因数是 1，但任意两项都有大于 1 的公因数。现代写法允许输出 1；古文区别单位和数，不能从“数”字直接认定原文已经给出现代含单位输出的类型约定。

原列全组互素时，原证直接判原列最小。Heath、Clay、Joyce 标 VII.21，方向正确，但本命题把它用于多项；Fitzpatrick 第 219 页标 VII.22，该命题是反方向，不能为此行提供依据。否则用 VII.3 取 D，就 D 量每项的次数建 E、F、G，再交换计数和量者角色。两次交换在 Heath、Clay、Joyce 标 VII.16，Fitzpatrick 标 VII.15；后一命题也可用单位与计数说明同一角色交换。随后用数字比的定义 20 连接相同倍数与同比。

反证不能由任取较小同比列直接推出它逐项整除原列；例如 6:9 与 4:6 同比，后一组较小却不逐项整除前一组。Heath 335 页指出 H、K、L 必须另选作最小同比列，解释该步参照 VII.20；仍须区分 VII.20 的两项原述与多项推广。不能因全组互素就将任意两项当作最小数对。现代补证可另用最简分数倍率：将倍率写成互素分子、分母，分母必须整除同比列的起始端全部坐标；当该端全组互素时分母只能是 1。先以此证最小列的全组互素与整倍数性质，再拿它解释原证，勿反用尚待证明的最小性。

共同次数 M 经角色交换后量尽全部原项。第一坐标给出 E×D=H×M，故根据 VII.19 得 E:H=M:D；E>H 蕴含 M>D，和 D 为最大公量矛盾。Fitzpatrick 给后一行标 V.13；该条讨论借相等的比传递与第三个比的比较，并非此步直接所需。Heath 记 Heiberg 认为可用 VII.13 加 V.14，而自己更愿从数比例定义解释。Clay 英文停在排除较小同比列，没有再点明 E、F、G 最小。Joyce 导读有记号疏漏：按其单位记号，若 b=nd，则 f=nu，不是 nb；若 d=ku，正确读回是 a=ke、b=kf。

[VII.34](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII34.html) 在非互素分支直接用 VII.33 构造两项的最小同比对，再作最小公倍数的独立证明。[VIII.6](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII6.html) 则直接用它选取连比例中三项的最小同比列。
