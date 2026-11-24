# VIII.4 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.8.4.html)、Heath 1908 卷 II 印刷页 350–353（扫描物理页 363–366，结论和评注在 353）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=231) 印刷页 231–233，以及 [Joyce VIII.4](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII4.html)。

给定三个最简邻比 A:B、C:D、E:F；它们不必相同。这是 Heath 353 页所强调的用语区别。先由 VII.34 取 G 为 B、C 的最小公倍数，使 H、G、K 相继具有前两种比。英语 G、H、K、L 对应希文 Η、Θ、Κ、Λ；第二分支的 N、O、M、P 对应 Ν、Ξ、Μ、Ο，不要按形似把中间两字认反。若 E 量尽 K，令 **F 量尽 L** 的次数等于 E 量尽 K 的次数，得到 H、G、K、L。若假想存在逐项更小的同邻比列 N、O、M、P，则前两种最简比和 VII.20 使 B、C 都量尽 O，由 VII.35 得 G 量尽 O，矛盾。

若 E 不量尽 K，则由 VII.34 取 M 为 E、K 的最小公倍数，把原前三项按 M/K 倍伸展，将 E:F 按 M/E 倍伸展，共用 M，得到 N、O、M、P。若有更小的 Q、R、S、T，同理 B、C 都量尽 R，所以 G 量尽 R。由 G:R=K:S，把整除关系移给 K 与 S；E 也量尽 S，故 VII.35 给出 M 量尽 S，反证完成。两支最小性分别使用一次、两次 VII.35。各版的定义 20、VII.13 等编号是编辑定位；其中 Clay、Joyce、Heath 在 G:R=K:S 邻近处提示交替，Fitzpatrick 则在其后的整除转移处标定义 20，两步作用不同。逐处相同的邻比条件也使两个正数候选列只能相差统一的正倍数，因而比较一个坐标足以检验能否全列较小。

Fitzpatrick 231 页英栏在题目的复述处误将 C:D 写成 C:B；同页希栏、各版本证明及后续写法均是 C:D。Joyce 第一分支误写成 K 量尽 L，而希文、Clay、Heath、Fitzpatrick 都是 F 量尽 L，正确末段比因此为 K:L=E:F。Joyce 导读另有两处疏漏：末段 m:p 应等于 e:f，不是 c:d；四项与三项共用一个连接项，拼接示例所得是六项而非七项。Clay 英栏止于第二支 M 量尽较小的 S 所引起的矛盾；希栏与其他版本仍明确回结 N、O、M、P 最小。
