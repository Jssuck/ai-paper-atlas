# 《后分析篇》I.19：独立数学与代码审查

## 结论与范围

**通过（2026-10-25）。** 审查者与正文和复现作者分开，独立阅读正文、源码、测试、复现说明、Notebook、结果及日志，并实际重跑。结论绑定下表最终文件SHA-256，任何正文、代码或公式格式修改后应重新核验；来源与版本解释另由来源审查负责。此项审查不是古代自然谓述或全部证明论的形式认证。

## 数学与范围核验

1. 肯定包含传递和负排斥桥接的逐元素证明正确。否定前提必须在所选较大中项上成立；结论真实不能反向认证任意中项。程序对不满足前提的输入抛出异常，不当作结论反例。
2. N对象有限域的严格包含链每步至少增加一个对象，故边数不超过N减起项基数；q种不同外延亦给出q减1的界。正文明确有限域、严格包含和同外延去重，并未用有限界证明无限自然谓述终止。
3. 给定词表没有严格中项，仅是相对于候选范围的结果。增加候选会改变相邻性，不改变原包含真值。外延相同的名字不能形成严格一步；商类去重不等于识别概念、本质、因果或自然/偶然方向。
4. 有理平均数严格位于两不同端点之间；重复细分的闭式和正余隙正确。一般构造允许任意有限次数，实际API仅允许0至256次；审查提出这一范围措辞修正，正文已采纳。有限运行并不证明无限性；一般构造才提供任意继续的论证。
5. 正文手算使用1起对象编号，程序用0起；已明确它们不是同一次实跑。主文新增3375/175/110与8次中点、10项测试和4单元Notebook计数均与真实附件一致。
6. 已核主README的顶部最新条目、年代目录行和本篇附件链接路径；发布后的远端内容和实际公式显示仍由发布验证另行完成，不冒称此本地审查已经检查远端渲染。

## 独立执行与交叉验证

- 独立运行 `python test_chains.py`、`python -O test_chains.py`、`python -OO test_chains.py`：各10项测试通过、退出码0；未覆盖作者原日志。
- 独立运行 `python chains.py`，输出与保存的 `results.json` 逐字节一致。
- 另写位掩码oracle，不复用作者集合包含判据。对1至5对象的全部非空三元组检查有效与无效前提的接受/拒绝，以及所有严格端点的候选中项；肯定前提数依次1、7、37、175、781，否定前提数0、2、18、110、570，与独立容斥公式一致。5对象扩展核查29791组，并未扩大公开实验的自称范围。
- 枚举4对象15个非空子集的全部149条非空严格上升链（包括单项链），每条实际调用链验证器并核对秩界；最大3条边。
- 对深度0至256逐一比较有理前缀与闭式，257种深度全部一致。
- 独立在单一私有Python命名空间顺序执行Notebook的4个代码单元，stdout与保存输出一致；未运行会重写Notebook的作者执行器，未声称启动Jupyter内核或检验前端。
- 关键前置检查使用显式异常，测试用unittest，不依赖优化模式会删除的裸断言。非法空外延、逆向、重复严格步、无效深度等边界已检查。

没有发现其他阻断性技术错误。合成数据与有限穷举不认证真实科学分类、自然谓述、科学直接性或所有证明终止；无证明助理认证。发布包不应包含运行生成的缓存文件。

## 显示格式修订复核

正文中点公式改用LaTeX `\lt` 表示两个严格小于关系，中项集合构造用 `\lbrace` / `\rbrace` 保留定界花括号，并为三处粗体标签补空格；已复核数学含义不变，最终散列已重新绑定。复现源码、结果与日志未作修改。本条只确认修订源码，修订后的实际GitHub显示由发布者另行截图验证。

## 最终文件SHA-256

| 文件 | SHA-256 |
|---|---|
| `papers/ancient/aristotle-posterior-analytics-i19.zh-CN.md` | `b542930dd59f215854308ab4911c30e9e36f7520ce480e4bfc9326e6c3a342c0` |
| `reproduction/aristotle-posterior-analytics-i19/README.md` | `2ea47b16fe07080607bd13deb0f9e35b0f4ef201f9c8e9126687599693e33841` |
| `reproduction/aristotle-posterior-analytics-i19/chains.py` | `1ba84bb7ce84278a6296da4558d8e69307c620f93cdb4855da35000fab82b8fd` |
| `reproduction/aristotle-posterior-analytics-i19/logs/environment.json` | `09e2af12c875ae458046298e939ef9936cfa303b1bff1679a57bed6bc48efb66` |
| `reproduction/aristotle-posterior-analytics-i19/logs/notebook.log` | `a4b0818ab657470318a324dbfb14acf619e7ff73b48fc7685a9b8ab7cb1e4074` |
| `reproduction/aristotle-posterior-analytics-i19/logs/tests-O.log` | `99416b5265655f7b50c19b6eb1994fdab4fb7152486c7b532a13f9efe8c98bbe` |
| `reproduction/aristotle-posterior-analytics-i19/logs/tests-OO.log` | `3b52daa519c3df249f534ff0e15cea075c269249794eef8a5eb593f40ff9d098` |
| `reproduction/aristotle-posterior-analytics-i19/logs/tests-normal.log` | `3b52daa519c3df249f534ff0e15cea075c269249794eef8a5eb593f40ff9d098` |
| `reproduction/aristotle-posterior-analytics-i19/results.json` | `259f9fe602ce53f6473253af67db4fa5df0976035d8f5e64b9ce6c7fb3fbf1c6` |
| `reproduction/aristotle-posterior-analytics-i19/run_notebook.py` | `4634704766dbc1bbadb5068c691fbae956aad39cb24c7ebb23d20f57efd02638` |
| `reproduction/aristotle-posterior-analytics-i19/test_chains.py` | `03cc687ff4ecf0d3053861b9a4619ce5ae0d95ae6a09516af530a423fb2d3ca7` |
| `reproduction/aristotle-posterior-analytics-i19/tutorial.ipynb` | `2f63424b85b7aafbac16b31e319bbb8cd9ca422d86639c8dee075f7847dc8b9c` |
