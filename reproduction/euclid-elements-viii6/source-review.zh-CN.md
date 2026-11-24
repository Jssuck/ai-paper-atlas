# VIII.6 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.8.6.html)、Heath 1908 卷 II 印刷页 355–356（扫描物理页 368–369，图在 355，收尾及评注在 356）、[Fitzpatrick 希英本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=234) 印刷页 234，以及 [Joyce VIII.6](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII6.html)。

原列以 A、B、C、D、E 示范；为检验 A 是否量尽位置在后的 C，按 VII.33 取 A 至 C 之间含端点的子列的最小同比形式 F、G、H（希文 Ζ、Η、Θ）。VII.14 由对应邻比相合得两列的端点比 A:C=F:H。因 A:B=F:G，按数比例定义 20，A 不量尽 B 蕴含 F 不量尽 G；单位可以量尽任何数，所以 F 不是单位。再按 VIII.3 得 F、H 互素；结合 F 不是单位，F 不量尽 H，遂由端点同比得 A 不量尽 C。互素本身不能排除单位量尽对方，这解释了原证为何保留排除单位的一步。

Clay 和 Fitzpatrick 希栏用括号保留“所以 F 也不量尽 H”的短语，Fitzpatrick 英栏也加括号；Heath、Joyce 与 Clay 英栏不用这句，但仍以互素和排除单位推出后续结论。Clay 英栏止于 A 不量尽 C；其他见证继续说明其余位置同理。各命题编号属于版本提供的定位，希文以其推理内容援用。

结论只否定较早位置量尽较晚位置，不要求数列递增。Joyce 题述的 [later] 是编辑性澄清，希文没有另写这个词；Heath 356 页评注也明确按较早项至较晚项解读。Joyce 的反例 24、12、6、3 具有共同邻比，24 不量尽 12，但位置在后的 3 量尽 6，因此不能把结论扩展到反向位置。推广到任意两个位置只需取以这两处为端点的连续子列，因共同邻比而继承首邻比不整除的条件。[VIII.7](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII7.html) 直接用本命题，由首项量尽末项推出首项量尽第二项，是针对首末项的逆否用法。
