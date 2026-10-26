# Euclid I.5 独立技术审查

结论：通过本次数学与实现审查。范围为最终正文的一般证明、现代有理模型、教学例与实际有限运行；不是人类专家认证、证明助理全形式化或古代公理体系的完备认证。来源年代和版本另见独立来源审查。

## 一般证明核对

- 第一次比较 AFC↔AGB，逐顶点 A↔A、F↔G、C↔B；AF=AG、AC=AB 及共同顶角提供两边夹角。输出 FC=GB、大角 ACF=ABG、AFC=AGB，未预先使用底角定理。
- 点序 A—B—F、A—C—G 使 AF−AB=AG−AC 得 BF=CG，并使 FA/FB、GA/GC 同向。这些条件不能从等长单独推出。
- 第二次 BFC↔CGB 的夹角在 F/G，来自前一次及同向射线；两个边输入 BF=CG、FC=GB 已有。取得外角 FBC=GCB 和小角 BCF=CBG，没有提前调用 SSS。
- 大角减小角前须核角区。正文正组合式在 B 处展开为 v−u=(sv−u)/s+(1−1/s)(−u)，s>1 使两系数为正；不共线保证扇形非退化。C 处交换角色。这只用延长条件，不用等腰对称或待证角相等，不循环。
- 先通过第二 SAS 得到外角，再通过角消去得到底角，覆盖原命题两部分；未以现代反射证明冒充原路线。

## 模型与例子

精确角比较以非零向量为前提；交叉平方等式保留余弦绝对值，点积符号补回锐/钝、零角/平角区别。通常角在0到π的范围及余弦单射必不可少。程序拒绝零射线、浮点和布尔输入，不宣称处理反身角或绕行角。

正文 b=4、h=3 的例子：腰长5、延长长10、短外段5、跨边平方153；底角余弦4/5，外角−4/5；大角点积39、小角点积96及分母均核对正确。Notebook另用 b=3、h=4，跨边平方97、底角余弦3/5；正文明确二者不同。五类反例分别检验不等腰、退化、错误射线、错误辅助半径与丢失符号，均有效。

实现的角区叉积检查只在全部构造前提成立时使用，不是任意三射线的充分包含判据；README已明示。初审发现README及源码注释把 BC/CB 写反，作者已改成“CB 在 ACF 内，BC 在 ABG 内”；实际索引与判据本来正确。更正后重新运行并绑定本版，没有遗留阻断性问题。

## 独立实跑

[代码、命令及范围](../../reproduction/euclid-elements-i5/independent-review/README.md)，[结构化结果](../../reproduction/euclid-elements-i5/independent-review/results.json)。独立角 oracle 用 (点积, |叉积|) 的正射线同向性，不复制余弦平方式；外点 oracle 用精确分量比值，不调用原 outward。

| 实跑内容 | 结果 |
|---|---|
| 576个角两两异构比较 | 331776次一致 |
| 非规范整数等长腰、有理平移与3延长比例 | 1056正例通过 |
| 上述四类错误变体 | 4224份拒绝 |
| 固定三角形任意方格辅助点对 | 2401对与独立前提判据一致 |
| 原单元测试普通、-O、-OO | 各34项通过 |
| 原枚举三模式 | 各1200正例、4800错误变体，结构化结果相同 |
| Notebook独立顺序执行 | 5代码单元，逐单元stdout与已存输出一致 |

Notebook实际采用标准库 compile/exec、共享新命名空间，无 Jupyter 内核；这里复核stdout而不宣称覆盖富媒体输出或完整nbformat规范。有限样本和实现交叉检查不能证明一般几何定理，也不是尺规作图引擎。

## 最终版本绑定

SHA256逐文件记录及运行环境见 [binding.json](../../reproduction/euclid-elements-i5/independent-review/binding.json)。本审查绑定正文及5个原Python文件、Notebook、复现README、作者清单与独立审查代码；后续修改这些内容须重新核查。

- `papers/ancient/euclid-elements-i5.zh-CN.md`：`e94904bb6deb4bbffa9f7c96a4fd788757bd167955261a5b75748aabfa80be44`
- `reproduction/euclid-elements-i5/geometry.py`：`a0196907afc46cf8c9e99c49ad0822b9d88790277b090edf9296947f67a1c9ed`
- `reproduction/euclid-elements-i5/test_geometry.py`：`df2537239f614c7798180d741cf8bff98d3e5a817aee55762e1606e66e16a856`
- `reproduction/euclid-elements-i5/run_examples.py`：`70e2aae229291e04c5cdaa13f38af7dbe367743bf26bb8e52a9b2e8f630bf228`
- `reproduction/euclid-elements-i5/run_all.py`：`8f72464e3f0d2d7133af13e91c5899e13897119dd6848d7b876b0b87303d20ea`
- `reproduction/euclid-elements-i5/verify_notebook.py`：`788add0195ecbb78b1396b8155aa2d18ec917a6a40149c931d5f736d40cdddaa`
- `reproduction/euclid-elements-i5/teaching.zh-CN.ipynb`：`67b0a849987c97d3c0196e8e74ed3ba2a970ed6ac33308f96b359a227087adb1`
- `reproduction/euclid-elements-i5/README.md`：`a5ab410dd3ed5e318ce7e1b6d17b71d42b4891409edd5b1597f9ec16ba494a18`
- `reproduction/euclid-elements-i5/SHA256SUMS.json`：`804b9d2a7d56c2e7c4b1849f0bed346de634c27bc02766805e8f9d37d7bf781d`
- `reproduction/euclid-elements-i5/independent-review/audit.py`：`a26284970072534b407e80b773d88bc39d3c75ae683d8e655030e7c1c3e27131`

发布渲染复核后，仅将正文两处符号函数的排版宏从 `\operatorname{sgn}` 改为 `\mathrm{sgn}`。反向替换精确恢复前审正文SHA256，数学内容及所有实现、Notebook和实跑证据均未变化；本报告已重新绑定最终正文。
