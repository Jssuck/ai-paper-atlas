# II.7 独立数学与代码审查

结论：**修正式名后通过本次数学与代码审查**。本审查独立于正文及主程序作者，实际阅读正文、实现与测试，并重新执行程序。它不替代另附的原文来源审查，也不声称已完成远端发布或视觉验证。

## 审查中发现并修复的问题

初版代码将 `original_datisi` 与 `original_disamis` 的名字互换，第三格有序恢复函数也使用了不符合其大项/小项方向的式名。其集合蕴涵虽有效，命名却会误导读者。最终版本已使 Datisi 对应 A(A,C)、I(B,C) 推出 I(A,B)，Disamis 对应 I(A,C)、A(B,C) 推出 I(A,B)；有序函数名为 `disamis`，测试、说明与三组日志同步重跑。此修正不可被“反例计数未变”替代：两条规则因交换词项而计数相同，单看数字无法发现语义标签错误。

## 数学逐项核验

1. 参数始终谓项在前：A(X,Y) 为 Y 包含于 X，O(X,Y) 的差集为 Y 减 X。正文的全部正向及恢复步骤按这一方向核过。
2. 第三格两全称原式所需的中项存在条件被显式写出。空中项的两个前提空真不产生特称结论；全词项非空制度则已提供该存在条件。
3. Datisi恢复中，Q 的交集见证经反向包含进入C，得到有向 I(C,B)，再换位得到 I(B,C)。二者语义等价但记录不同；程序没有把句法不匹配伪造成语义反模型。
4. Disamis恢复中同一见证由B进入C，直接得到 I(A,C)；Bocardo恢复时还保留“不在A”的性质，直接得到 O(A,C)。反向包含不是原前提的免费换位。
5. Ferison原式的共同见证属于B而不属于A。E简单换位与Q不能恢复B/C交集；正文三个非空单点集合反例成立。
6. 覆盖桥 U减A 包含于C 是教学采用的充分条件，并非E换位。共享见证桥本身已经包含目标交集信息；两个独立some不能合并为同一对象。正文对此均明确披露。
7. 正文第3至7节及练习中的具体集合逐一代入检查，输入真且目标假/真与声称一致。特称肯定对称、特称否定不对称、包含传递的任意见证证明成立。
8. 有序函数只是三个明确图式，不是全推导搜索器。程序和正文没有从它们的输出缺失推出任意证明系统下不可证明，也没有用有限枚举替代一般定理。

## 独立执行及不同实现交叉核验

主实现用Python集合。本审查另写[整数位掩码核验器](../../reproduction/aristotle-prior-analytics-ii7/independent_check.py)，不导入 `model.py`，以逐位运算独立编码18条输入与目标，再逐条比较两制度的前提模型数、反模型数及总数。1–4元论域合计4680（允许空项）及3746（全部项非空）；18条计数全部一致。该核验是另一种实现交叉检查，不是从有限检查得到一般有效性的证明。

[真实独立输出](../../reproduction/aristotle-prior-analytics-ii7/logs/independent-check.txt)；审查者另在[normal](../../reproduction/aristotle-prior-analytics-ii7/logs/reviewer-test-normal.txt)、[-O](../../reproduction/aristotle-prior-analytics-ii7/logs/reviewer-test-O.txt)、[-OO](../../reproduction/aristotle-prior-analytics-ii7/logs/reviewer-test-OO.txt)模式各重跑9项测试，全部通过。独立执行命令（在复现目录）：

```bash
python3 independent_check.py
python3 -m unittest -v test_model
python3 -O -m unittest -v test_model
python3 -OO -m unittest -v test_model
```

已检查输入和图式守卫使用显式异常，不依赖优化时消失的 `assert`。12条预期有效蕴涵在两制度都有满足前提的模型且反模型数为零。6条故意无效的提案按制度有预期反例；去掉存在条件的两条在“全项非空”制度无反例是制度差异，不是失败。三份主运行JSON逐字相同。

## 内容绑定

以下SHA-256绑定本次核验的正文、源码、说明、环境、原始实跑及独立核验证据；审查文档本身不自包含自己的哈希。绑定后的改动需复查，而不应沿用旧通过结论。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-ii7.zh-CN.md`|`9d85c258be581f2f9f612f9ee5079a98ea5179f548d6f479792ff0c304318552`|
|`reproduction/aristotle-prior-analytics-ii7/README.md`|`f8037b9b97a1dc8caae771fbeeb0cd2d2c7265e0109cbd7958c840da54941c8c`|
|`reproduction/aristotle-prior-analytics-ii7/environment.txt`|`c7357691151c8498c11ce6673efea0543c6a303ac51962faeb3b2e6c955bf3d6`|
|`reproduction/aristotle-prior-analytics-ii7/independent_check.py`|`e29297a0114e45440c77c45539bedd54b2094cc49c4cedfb3836e791ef9c8a52`|
|`reproduction/aristotle-prior-analytics-ii7/logs/commands.txt`|`89b238284ab4c7e6053d3e79f8d441ec281ba5e174625cbdd6353c25004c5cea`|
|`reproduction/aristotle-prior-analytics-ii7/logs/independent-check.txt`|`27acecb7660b6f2cff1187e17144b627a2fbfe1da4ea62c435a1866847160070`|
|`reproduction/aristotle-prior-analytics-ii7/logs/reviewer-test-O.txt`|`1cc873c345d7f8667eabac7117ef62707c030d7df9d311926920e0d0307f18af`|
|`reproduction/aristotle-prior-analytics-ii7/logs/reviewer-test-OO.txt`|`837281ccb23bfd9f03a109ba22b5facd27622655e90c84d44ff2949b66ff86e3`|
|`reproduction/aristotle-prior-analytics-ii7/logs/reviewer-test-normal.txt`|`1cc873c345d7f8667eabac7117ef62707c030d7df9d311926920e0d0307f18af`|
|`reproduction/aristotle-prior-analytics-ii7/logs/run-O.json`|`c8e5be9635377f1228697b95b6a3b510a36afc84a45e3dd7b7862988f9189bd7`|
|`reproduction/aristotle-prior-analytics-ii7/logs/run-OO.json`|`c8e5be9635377f1228697b95b6a3b510a36afc84a45e3dd7b7862988f9189bd7`|
|`reproduction/aristotle-prior-analytics-ii7/logs/run-normal.json`|`c8e5be9635377f1228697b95b6a3b510a36afc84a45e3dd7b7862988f9189bd7`|
|`reproduction/aristotle-prior-analytics-ii7/logs/test-O.txt`|`e4ad1a57881e4819a6f2c045984c946272ba30d81edf27de25e9117b538032ba`|
|`reproduction/aristotle-prior-analytics-ii7/logs/test-OO.txt`|`5ddd78146096d88f61262c3cc24b68e931bb1b5f3362580cf5317b6e9afa9e04`|
|`reproduction/aristotle-prior-analytics-ii7/logs/test-normal.txt`|`d0470f8123741a48433a5f13811920ff9526c7146542f39f06ef93789abd690e`|
|`reproduction/aristotle-prior-analytics-ii7/model.py`|`763ca1f0dbfcdfa20df89c030901c1d33143f4a9270f67580848d84fc897326b`|
|`reproduction/aristotle-prior-analytics-ii7/test_model.py`|`19dcd3c1a11475e2d269daadb33a62455981a18b5a4fd05e8a992b1a8a0fe7b4`|
