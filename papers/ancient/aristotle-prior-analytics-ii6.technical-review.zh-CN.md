# 《前分析篇》II.6：独立数学与代码核验

## 结论

修正后通过本次数学、实现与证据一致性审查。审查者未编写初始教学程序或正文；独立阅读正文、来源台账、根目录说明、代码、测试及全部实跑日志，另写逐成员型量词oracle。原文来源与版本校读另见[来源审查](aristotle-prior-analytics-ii6.source-audit.zh-CN.md)。此结论不替代远端提交、链接和实际数学渲染验证。

## 发现与修正

1. 初稿正文明确覆盖H与结论Q已足够，但主程序覆盖规则还保留E(A,B)。虽该较强规则也有效，却未直接检验正文承诺的较弱前提。现主规则移除E；全255型的前提模型数为32、全词项非空218型为30，均零反例。相关README和三份JSON已同步。
2. 复现README表后原称“后三类”，实际列五类不足规则，已修。
3. 正文证据行段与来源台账曾不齐，现已由来源审查同步；本报告不独立裁断希腊文本校勘。

## 数学核验

- 全称肯定方向始终为A(X,Y)表示Y包含于X；E对称换位合法，肯定全称反向关系是新增假设。四正向式与Camestres、Cesare、Baroco反向式逐对象证明正确。
- Festino独立存在见证反例三个词项均非空，两个存在量词确可由不同对象满足；同一见证补充和补集覆盖均显式标作教学条件。
- H覆盖所有B外对象是充分但非必要条件；正文三元素非必要例逐项验真。P与H合取推出A恰为B补集，亦正确。
- 八成员型压缩保留所用一元外延命题及覆盖条件；全0类型不可省。255与218计数正确，后者可由容斥255−3×15+3×3−1得到。重复型删除不保留基数，正文已明确语言边界。
- 反例最小性按元素数检验，压缩论证支持从代表模型推广至任意更小集合模型；不把有限数值运行说成证明全部古代逻辑。
- 正文算例、16题答案和AI类比未发现逻辑错误。根README只收录本章完整单元，不把它冒充现代AI论文或全书完成。

## 独立实跑

- 普通、`-O`、`-OO`三模式各10项测试通过，退出码0；JSON分别与作者保存输出逐字一致。
- 255与218域中均9条有效规则零反例、5条不足规则有反例，所有有效式都有满足前提的模型。
- 新写[独立量词oracle](../../reproduction/aristotle-prior-analytics-ii6/review/independent_check.py)，不用被测A/E/I/O函数构造期望值，逐一比较255×14条前提和目标真值；全部匹配。并独立检查H非必要反例。
- 作者测试包含4680个1至4元素带标签赋型压缩核验、参数非法输入和空项方向检查；显式异常与unittest断言在优化模式保留。
- [独立运行输出](../../reproduction/aristotle-prior-analytics-ii6/review/independent-output.txt)和[命令记录](../../reproduction/aristotle-prior-analytics-ii6/review/commands.txt)可复核；三个独立测试输出在同目录。

## 最终文件绑定

以下SHA256绑定本次实际审阅与重跑后的文件。排除缓存、进度状态、来源审查报告及本报告自身，避免自引用；任何文件修改均需复核重绑定。

|仓库相对路径|SHA256|
|---|---|
|`README.md`|`3bd0a77fcd938dd72a05ee716df699f38d42eab5ba38784d6c25f454edf4295b`|
|`papers/ancient/aristotle-prior-analytics-ii6.zh-CN.md`|`35cf35e98dc756f7f821e16d2603fe5f7a1ccc176f7a7369760807048edb2ac9`|
|`papers/ancient/aristotle-prior-analytics-ii6.sources.zh-CN.md`|`673c384a84f2340f1781ba3fac2fcbe58f5b10bea98e54818c5d38411d074aea`|
|`reproduction/aristotle-prior-analytics-ii6/README.md`|`1971c8d1e3a506b5d784b2e51fd109189c0757ac1b04f1c173806ff34c7fa299`|
|`reproduction/aristotle-prior-analytics-ii6/environment.txt`|`c2ba54338e2ded06160281cc99cbd44e91534e6a00ccd96d2f5770977ff2e21d`|
|`reproduction/aristotle-prior-analytics-ii6/logs/commands.txt`|`ebae16983b63d7789b31ca16ed7e0a022aa323b45a2b56fa3bc4b17ee531a01a`|
|`reproduction/aristotle-prior-analytics-ii6/logs/run-O.json`|`c5df5770b5edc6391f0200158d3b0f0f8bb6458268f334b222b6018983460c8f`|
|`reproduction/aristotle-prior-analytics-ii6/logs/run-OO.json`|`c5df5770b5edc6391f0200158d3b0f0f8bb6458268f334b222b6018983460c8f`|
|`reproduction/aristotle-prior-analytics-ii6/logs/run-normal.json`|`c5df5770b5edc6391f0200158d3b0f0f8bb6458268f334b222b6018983460c8f`|
|`reproduction/aristotle-prior-analytics-ii6/logs/test-O.txt`|`d5f7b69555116c9b92ea292b62d1eea7f418f883f6655e003f9a78006753515a`|
|`reproduction/aristotle-prior-analytics-ii6/logs/test-OO.txt`|`ad755a2d8da4676dbb6e71dbbc485e6f52e3b0d322254cb0aa9c710658d4563f`|
|`reproduction/aristotle-prior-analytics-ii6/logs/test-normal.txt`|`e12f4e618f09c3b8402a3016da30e6ccb714114ebcd389aa141c27483f9157df`|
|`reproduction/aristotle-prior-analytics-ii6/model.py`|`71b84b84e70700f587ac2111b4c8523817bf921c33ed5748e2fe5605e6ed21ca`|
|`reproduction/aristotle-prior-analytics-ii6/review/commands.txt`|`aae563171d2f42c74b405379330e29e5d63115493b983d8c6360bcd7c0ef113c`|
|`reproduction/aristotle-prior-analytics-ii6/review/independent-output.txt`|`0b029f30a10af6d46f7197b4f3c6154debde8ea7c2d1a62f721471767a98b085`|
|`reproduction/aristotle-prior-analytics-ii6/review/independent_check.py`|`cd10841c298eadee9bfe76e7f51a8ac9af5f1ac0b7f252d674c591b15cced800`|
|`reproduction/aristotle-prior-analytics-ii6/review/test-O.txt`|`5e99aaf42f14cf0d38c582e0e98eaa284d66211d2b98c7f82abacc0a8e18837e`|
|`reproduction/aristotle-prior-analytics-ii6/review/test-OO.txt`|`bf927fa1069f5da18ff9e0673cf37fb3aeb7ed8dafd94fde3176218502c997fe`|
|`reproduction/aristotle-prior-analytics-ii6/review/test-normal.txt`|`87cd20532a24c7de2c717667e3c7f73de844152192ae3408f854b305024ff7a8`|
|`reproduction/aristotle-prior-analytics-ii6/test_model.py`|`8966cde28b57d7ea112d785f6fdd5e028416c9ab1ddc2272d054dc34a224b26e`|
