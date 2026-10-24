# II.19 独立数学与代码核验

## 结论与审查范围

**结论：通过。** 独立核读了 Owen 1853 印页 221–222 的章 XIX 与 Jenkinson 1913 Book II 第19节；核对正文的数学模型、逐步证明、反例、六道带答案练习、源码、单元测试及真实结果。文献异读与希腊原版位置另见[来源台账](aristotle-prior-analytics-ii19.sources.zh-CN.md)和来源审查。本报告不将古代辩论建议当作已验证的心理学结论。

## 数学检查

1. 主词→谓词的箭头方向与集合包含一致。五条链节经四次传递推出 F→A；链长归纳不依赖询问顺序。集合实例仅作解释而非一般证明。
2. 重复词项并不足以产生所求结论。正文的分叉包含反例、重复前提反例、缺边反模型和全部练习答案均成立，且相关反例不依赖空项。空项不提供存在结论。
3. 只计算两端不同的可达对，闭包包括已有前提；这是输出统计约定，不是否认包含的自反性。终止和路径完备论证的范围明确限制于教学图。
4. 所选错开次序的前三问来自原文例子；末两问是现代补齐。省略中间结论、打散呈现次序与删除前提是不同操作。局部相邻共享计数不是有效中项检测，更不是人类欺骗程度。
5. 主程序的队列遍历给出最短路径证书；生成器、重复前提、环、未知项、空图与非法边的处理与文档约定一致。

## 独立实跑证据

主测试的 8 个测试方法再次实跑通过。另写了不使用被测遍历程序来生成期望结果的[独立 oracle](../../reproduction/aristotle-prior-analytics-ii19/audit/independent_oracle.py)：用单元素成员赋值直接检验每个包含前提和查询。

- 枚举四词项全部 4096 个无自环有向图，对每图 12 个非自反查询共 **49152 次**检查语义蕴涵与证书存在性；有证书时检查端点、边、无重复节点，并独立枚举所有更短简单路径检查最短性。
- 独立构造六项五边链，核查全部 120 个排列及其 **600 个前缀**的语义闭包大小与目标可得时刻。
- 独立重算相邻共享项直方图：0、1、2、3、4 对分别对应 **14、40、48、16、2** 个排列。两个展示顺序的前缀大小分别为 **1,3,6,10,15** 与 **1,2,4,6,15**，相邻共享数分别为 **4 与 0**；每种排列最终闭包大小都是 15，目标都在第五步才出现。
- 普通、`-O`、`-OO` 三模式均通过。审查脚本用显式异常检查，不依赖优化模式会删除的 `assert`。

命令（在复现目录内）：

```sh
python3 audit/independent_oracle.py
python3 -O audit/independent_oracle.py
python3 -OO audit/independent_oracle.py
```

真实输出：[普通](../../reproduction/aristotle-prior-analytics-ii19/audit/oracle-normal.log)、[-O](../../reproduction/aristotle-prior-analytics-ii19/audit/oracle-O.log)、[-OO](../../reproduction/aristotle-prior-analytics-ii19/audit/oracle-OO.log)。这些是有限实现核验，不是对任意图的测试穷尽，更不证明所有古代三段论或人类行为主张。一般链论证仍由正文的传递性与归纳承担。

## 修订与剩余边界

终审要求将“程序只有六项图”改成明确的展示/核验输入域，并明确闭包统计过滤自反项对；最终正文已落实。未发现需修正的数学结论或代码错误。代码作者最初将错开顺序相邻共享数预期写成 1，最终正确值为 0；已重跑并由独立 oracle 确认，复现 README 如实记录此修订。

这份技术通过意见不代替发布时的远端字节、链接、GitHub 公式实际显示与分支冲突核验。

## 最终审查对象 SHA-256

下表绑定本报告实际审查的文件；任何对象改动都应重新核查对应结论。报告不自引用自身哈希。

| 文件 | SHA-256 |
| --- | --- |
| `papers/ancient/aristotle-prior-analytics-ii19.zh-CN.md` | `f4677568b3de0abfd3b3ace86b1667619714e5566caed595a3eb75919ef6232b` |
| `reproduction/aristotle-prior-analytics-ii19/presentation.py` | `e0fdf278ebe4b0f97b063eeb478d45162f7cb78f56bcf6cc2680a9a677dd2867` |
| `reproduction/aristotle-prior-analytics-ii19/test_presentation.py` | `0e011a9fbc256ef0a55e16eea4ca59e75aef2feb9d75a1d04c3299ca1db8879d` |
| `reproduction/aristotle-prior-analytics-ii19/run.sh` | `290c2273588797e3f1456c44b7b809c327313f0ae2b3aaf8f615f5465c231dc7` |
| `reproduction/aristotle-prior-analytics-ii19/README.md` | `8ad591097218b7cdbec679063644649d7d7407efe33a75c55ae95912ae005d5e` |
| `reproduction/aristotle-prior-analytics-ii19/audit/independent_oracle.py` | `95a8816abf45c7237cc8b79e60fd7565b188789897e5b96429ab20b7c92aaeb8` |
| `reproduction/aristotle-prior-analytics-ii19/audit/oracle-normal.log` | `2da241fdc754a885a9758c3e6f915d5b77e7b9a5d0beaa4b90bbc29d6f555041` |
| `reproduction/aristotle-prior-analytics-ii19/audit/oracle-O.log` | `2da241fdc754a885a9758c3e6f915d5b77e7b9a5d0beaa4b90bbc29d6f555041` |
| `reproduction/aristotle-prior-analytics-ii19/audit/oracle-OO.log` | `2da241fdc754a885a9758c3e6f915d5b77e7b9a5d0beaa4b90bbc29d6f555041` |
