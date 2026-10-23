# II.9 独立数学与代码审查

## 结论与范围

审查最终正文、四式16格、全部逐步证明、反模型、12题答案以及作者程序、测试和结果。**在明示的经典一元三项外延语义及三种存在政策下通过；未发现待修数学或代码错误。** 来源和版本问题由[独立来源审查](aristotle-prior-analytics-ii9.source-audit.zh-CN.md)另行负责，本审查不以数学一致性替代原文核验。

正文用U标记全称肯定，代码用传统种类A；已明确映射，项A与命题种类A不同。第二格中项为A，大端B、小端C；`retain_major`保留AB而检查AC，`retain_minor`保留AC而检查AB，作者程序没有把目标前提偷偷加入背景。

## 手工证明核验

- 原四式Camestres、Cesare、Festino、Baroco的前提与结论排列正确；原式在允许空项的语义仍有效，特称两式的见证来自小前提。
- 全称反对替换保留AB时，包含传递或排斥传递得到新全称结果，即使C空也成立；但要排除原来相反全称前提必须C非空。保留AC时，特称结果本身就需要C见证。正文正确区分这两处存在承担。
- 全称矛盾替换的I(B,C)自己提供同一个见证；小前提反驳走第一格，大前提反驳走第三格。Darii、Ferison、Ferio、Datisi方向核对正确，没有将Datisi与Disamis倒置。
- 特称反对替换允许I/O同真。Festino与Baroco两点反模型同时满足原前提、原结论和替换命题；保留小前提的两种见证不能无根据合并。文本限定为无所需目标反驳，没有泛称不存在任何逻辑后果。
- 特称矛盾替换U(B,C)可运送保留小前提的见证，或者从保留大前提推出全称AC关系；两种方向均无需额外存在假设。
- 非全称加强的两个反模型正确；12题答案与正文相符。原文详论的Camestres、Festino和省略同理的Cesare、Baroco教学补全已区分。
- 三项八类型压缩的理由限定于当前四类命题，无对象计数、关系或模态；有限实跑不被写成一般一阶逻辑定理或古代唯一语义证明。

## 独立实现与真实执行

独立程序[源码](../../reproduction/aristotle-prior-analytics-ii9/independent_check.py)不导入作者`check.py`，使用布尔三元组、`itertools.combinations`枚举类型子集，以逐对象`all`/`any`量词计算真值；作者代码则采用位码与集合运算。独立输入表从正文四式16格重新列出。

对三种政策各16格，逐项核对作者`results.json`中的：背景模型数、表定结果反模型数、原目标未被反驳的模型数、目标有向项对上所有有效A/E/I/O形式。独立重放18个已存反模型，并检查正文两个不能全称加强的例子和两个特称反对失败例子。所有背景均可满足，未把不相容背景的空洞蕴涵当成功。

真实执行普通、`-O`、`-OO`三模式，均通过48格匹配、18个反模型重放和4个正文例子；并在各模式重跑作者10项unittest，均通过。独立脚本使用显式`require`异常，作者测试使用unittest，优化模式不会移除检查。

- [普通模式日志](../../reproduction/aristotle-prior-analytics-ii9/independent-normal.log)
- [-O模式日志](../../reproduction/aristotle-prior-analytics-ii9/independent-O.log)
- [-OO模式日志](../../reproduction/aristotle-prior-analytics-ii9/independent-OO.log)

复跑：进入附件目录后执行`python3 independent_check.py`，也可加入`-O`或`-OO`。日志记录真实运行时间与命令，退出码均为0；这是本地教学核验，不声称GitHub CI运行过。

核实统计：允许空项255模型，C非空240模型，全项非空218模型；矛盾替换8方向在三政策下均零反模型；全称反对4方向允许空C时各7个未反驳模型，限制C非空后为零；特称反对4方向在三政策均各16个未反驳模型。正文§11与结果文件一致。

## 最终版本绑定（SHA-256）

以下哈希绑定已读正文和已实跑代码/结果，不是公开进度字段，也不代表未来版本自动通过。

|文件|SHA-256|
|---|---|
|正文 `aristotle-prior-analytics-ii9.zh-CN.md`|`1af9ef1aa45652f2d74e57f39bd793c2d2ccd4110d15b5ce9cadba6478e3d2c2`|
|作者 `check.py`|`0ae6ae7cab7c341275bb4882c4d7b43c87ced45c8393489e9f98b4d5b2718430`|
|作者 `test_check.py`|`a7267856d4ee2184a5354ad5bb3304dcae50282091a2978f5563b7a4f387054c`|
|作者 `results.json`|`87a30ad3add6eb4699bd8b894dfa18049bbbe873afd759724ef0a7022c89f359`|
|独立 `independent_check.py`|`8fa738a6f1a862418118dc1c731f4691fd07356b77fc2b4bdcbf8754f0bf525f`|

实际公式浏览器显示、远端字节与链接完整性由发布步骤核验，不在本地数学审查中冒称已完成。
