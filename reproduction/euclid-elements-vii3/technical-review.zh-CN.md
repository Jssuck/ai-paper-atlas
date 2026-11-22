# VII.3 独立技术核对

**结论：通过。** 核查中文精读、原典核对、标准库代码、测试、Notebook 和四份冻结日志。

- 实读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.3.html)、Fitzpatrick 页 197–198 和 Heath 卷 II 页 300–302，目检两印本实际页影。Fitzpatrick 希、英栏及 Heath 图各有六段；希文的 Ζ 对应英图 F。原证明第一支的 E 是反设量尺，第二支的 E 是构造结果，不能把同一图上的长度当成两个分支的数值实例。Fitzpatrick 两处否定的英语句法易误解，须按希文读成「不存在比候选更大的共同量尺」；Clay 英栏较希文少末尾结论。
- 证明中的「三数不互素」确指有同一非单位量尺，不是两两各有共同量尺；据此才可对 A、B 使用 VII.2。第一支用 VII.2 附论否定较大公度。第二支先用附论建立 D、C 的非互素前提，再用 VII.2 得 E，最后反设任意较大公度，经两次附论递推到 F 整除 E。现代公因子集合恒等式的两个方向均成立，从此导出折叠、换序与分块，而不预设结合律。正文算例、两个反例和五道练习已重算。
- [VII.33](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII33.html) 非互素分支确实用最大共同量尺构造同比的最小数组；[X.4](https://mathcs.clarku.edu/~djoyce/elements/bookX/propX4.html) 讨论三个可通约的量，并不是 VII.3 的前置依赖。Heath 页 302 所记 Heron 的推广与正文的三数题目分开。
- 独立执行 `python -B -m unittest -v` 及 `-O`、`-OO` 两种优化模式，各通过 6 项。另以标准库 `math.gcd` 独立核对 1–24 的 13,824 个有序三元组的中间值、最终值及分支；10,356 个直接返回，3,468 个再次化简，与正文及测试一致。日志的单元测试行未单列分支计数；计数由测试内的断言核对。
- 标准库 Notebook 回放的三个代码单元输出与冻结日志正文逐行一致；未调用 Jupyter 内核或验证前端渲染。测试限于正整数教学模型和有限输入，不是任意输入的证明。
