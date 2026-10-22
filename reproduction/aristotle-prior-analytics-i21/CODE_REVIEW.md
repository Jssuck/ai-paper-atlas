# I.21 独立代码审查

结论：在下述有限检查范围通过，无阻断错误；未修改作者源码、测试或原始日志。该结论不是一般数学证明或古代唯一语义认证。

## 方法与结果

逐对象 oracle 独立实现 D/P/N/C/BOX，不调用作者 `holds` 或 `_quantify` 作为真值来源。对象成员虽从输入位掩码读取，量化及模态运算以 Python 布尔列表、all/any 逐对象重建，而不是复制作者集合并交算法。

正常、-O、-OO每模式均检查4744配置，覆盖(n,情形数)=(1,1),(1,2),(1,3),(2,1),(2,2)。每配置180个模式/数量/谓项/主项组合，共853920查询，与作者结果一致。包括相同主谓项、空项和不同情形外延。

58个非法输入分别检验构造、维度、项、模式、量词和情形索引，均按接口拒绝为ValueError。包括bool冒充int、负数、非整数、空情形、错误元组长度、越界位；不声称覆盖任意Python恶意对象或资源耗尽。

29700项变形比较检查对象重命名、重复情形、非实际情形顺序交换的保真性。9类明确语义变异分别找到区别见证：主谓交换、肯否翻转、全称/特称翻转、P当N、N当P、C当P、BOX当N、末情形误作实际、空主项特称误真。它们是对错误语义的独立比较，不是任意源代码变异全覆盖。

作者16项单测在三模式全部通过；重新执行枚举器后，完整JSON与各自保存的作者JSON逐字相同。作者manifest的11项SHA256全部吻合。时间相关的单测运行耗时不要求逐字相同，作者日志未被覆写。

独立补查正文6个配置、21条具体真假主张，包括第6节去掉非实际情形后的变化，第7.1/7.2的反模型与第8节不同见证。正文与附件使用不同数值配置的地方未强行等同；它们各自满足所列主张。

## 定义与实现

正文与README规定固定实际主项；N和P逐对象量化情形，C要求正负两向可能，BOX则逐情形重新量化主项。代码保持这些区别，C肯否对称不被偷换为项位对称。空主项全称真、特称假一致。模型核心复用自有I.20实现的来源已标明，I.21例子与日志重新执行。

主稿的一般见证证明及反证由独立数学审核负责；本代码审核不拿有限枚举替代证明，也不将原典规则同现代模型之间的失配删掉。

## 文件与复跑

- [独立oracle和变异比较](independent-review/check.py)
- [正文配置核查](independent-review/check_prose.py)
- [执行命令](independent-review/commands.txt) · [实际环境](independent-review/environment.json)
- [正常结果](independent-review/result-normal.json) · [-O结果](independent-review/result-O.json) · [-OO结果](independent-review/result-OO.json)
- [正常作者复跑](independent-review/author-tests-normal.txt) · [-O](independent-review/author-tests-O.txt) · [-OO](independent-review/author-tests-OO.txt)
- [正常正文核查](independent-review/prose-normal.txt) · [-O](independent-review/prose-O.txt) · [-OO](independent-review/prose-OO.txt)
- [版本绑定](independent-review/bindings.json)

任何修改模型、主稿相关定义或审查代码后，应重新核对受影响的结果和绑定。没有运行Jupyter或CI，不声称其通过。
