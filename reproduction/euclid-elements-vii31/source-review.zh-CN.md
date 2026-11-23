# VII.31 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.31.html)、Heath 1908 卷 II 印刷页 332–333（扫描物理页 345–346，图与完整证明在 332、评注在 333）、[Fitzpatrick 希英本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=218) 印刷 218–219（图在 219），以及 [Joyce VII.31](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII31.html)。

希文 Α、Β、Γ 对应英语 A、B、C。先从合数 A 取一非单位真因数 B。B 若是素数就结束；否则取 B 的非单位真因数 C。C 量尽 B，且 B 量尽 A，因此 C 也量尽 A。继续时，每步维持两点：新数仍量尽原数 A，且严格小于前一步。第 VII 卷定义 13 中“由某个数测量”须联系定义 11 的素数及定义 2 的单位区分来读；这里所取不仅不是单位，也不是合数自身，否则严格下降不成立。用重复加法或现代整数等式可说明整除传递，原文没有点名定义 15 或 VII.30。不能无限严格下降是终止理由；联系 VII.1–2 只能作证明方法比较，不是本命题给出的引用。

Heath 333 页把正文所说“满足所要求的事”解释为隐含找出一素数来量尽 A。该页另指出，332 页第 18 行的希文第一次说找到一个素数时，在“量尽”处停住；英文补入后文明确给出的前一项与 A 的关系，Heath 转述 Heiberg 关于抄本 P 可能因行尾相似而漏抄的推测。Fitzpatrick 对应第一次出现处将补充文字置于括号。Clay 英栏保留下降链和素数存在结论，但不另重复一般命题和证毕标记；希栏及两印本有这一步。Joyce 网页把一般命题紧邻重复，不表示第二个推理步骤。

Heath 同页还介绍 Heiberg 移至附录的另一证明：取量尽 A 的最小非单位数 B；若它仍为合数，取其较小真因数 C；C 同样量尽 A，违反 B 最小。这是附录记载的异证，不等同于主证明每一步都选择最小因子，也不同于现代程序中为便于复跑而规定某种因子选择顺序。VII.31 只保证至少一个素因子，不证明全部分解或分解唯一。

[VII.32](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII32.html) 直接在合数分支援用 VII.31；[IX.13](https://mathcs.clarku.edu/~djoyce/elements/bookIX/propIX13.html) 分别为反证中的合数因子 E、F 取得素因数；[IX.20](https://mathcs.clarku.edu/~djoyce/elements/bookIX/propIX20.html) 在共同倍数加一不是素数时用 VII.31 取得一个素因数，再论证它不在原清单。IX.14 用的是 VII.30，并非 VII.31；VII.34 也未在其证明中调用 VII.31。
