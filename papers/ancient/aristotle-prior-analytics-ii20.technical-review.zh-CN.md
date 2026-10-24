# II.20 独立数学与实现审查

审查范围：[深读正文](aristotle-prior-analytics-ii20.zh-CN.md)的数学重建、例反例与六题答案，以及[复现源码与日志](../../reproduction/aristotle-prior-analytics-ii20/README.md)。来源与校勘另见独立来源审查；本报告不代替历史版本鉴定，也不声称完成整个《前分析篇》的验证。

## 结论与修订

**通过本单元限定范围的技术审查。** 初读提出的两项澄清已修正并复核：三个不同项名不要求外延互异；正文允许空项的集合语义与程序主枚举三项全非空的政策分开，18 个有效候选的统计不跨政策使用。程序 README 同样明确允许不同项名的集合相等。审查没有把网页公式实际渲染或远端发布验证作为已经完成；那些属于发布后另外核验。

## 一般证明和答案核验

1. A/O、E/I 的否定配对在所定集合语义中正确，空主项不破坏这两组矛盾关系；A/E 则不能同样处理。
2. 第 4 节任取对象证明包含传递，第 5 节用交集空与包含证明全称否定；二者均无需偷加主项存在。对一个固定有效结论，改变待反驳论题可以改变反驳性，程序没有把论题追加为前提。
3. 第 5 节第二格全肯定与第三格混合前提的反例，均逐项代入为前提真、所声称目标假；至少一肯定、至少一全称仅是该范围的必要条件。
4. 第 6 节三项两两分离与两端同外延、中项分离的两类模型，一起排除四种端项结论。每项非空，且 E/O 两种前提及其主谓方向均覆盖。
5. 第 7 节添加新见证不删除既有存在见证；端项分离使 I 假，端项重合使 O 假，按各前提另建见证可满足 I/O 任意组合。需要非空项时可在保留分离或重合约束下补对象。因此不是从一个例子跳到所有两特称情形。
6. 六题答案与上述证明一致。有限检验不是任意逻辑语言的完备性证明；复现 README 的七类型压缩论证只对固定三词 A/E/I/O 语法成立。忽略 000 类型时可在空支持情形保留一个 000 对象，故不偷换非空论域。

## 独立实际复算

审查另写了 [`independent_sets.py`](../../reproduction/aristotle-prior-analytics-ii20/audit/independent_sets.py)：不调用生产程序的类型生成器或命题真值函数，而在四对象论域上直接生成全部 15 个非空子集，以独立的 `all` / `any` 集合成员判断计算 A/E/I/O。每个候选检查 3375 种真实集合赋值，192 个候选合计 648000 次；仅在比对阶段调用生产 `check`。

- 正常、`-O`、`-OO` 各实跑一次，三个独立 JSON 逐字一致。
- 192 个分类全与生产结果一致：18 个有效候选，三格各 6；包含全称结论的特称弱化，不是历史式名总表。
- 对生产程序返回的全部 174 个首反模型，另转为真实集合，独立检查各项非空、两前提为真、目标为假，全部通过。
- 正常、`-O`、`-OO` 分别独立复跑原 8 项 unittest，均成功。检查依靠 unittest 或显式异常，不受优化模式删除裸 assert 的影响。
- 两负与两特称各 48 候选均无有效结果；两组有交集。全部前提对可满足，未把不一致前提的空泛蕴涵误计为有效结果。

独立 JSON 与日志位于 `audit/independent-sets-{normal,O,OO}.json` 和 `audit/recheck-{normal,O,OO}.log`。复算命令（仓库根目录）：

```sh
cd reproduction/aristotle-prior-analytics-ii20
python3 audit/independent_sets.py
python3 -O audit/independent_sets.py
python3 -OO audit/independent_sets.py
python3 -m unittest -v test_syllogism
python3 -O -m unittest -v test_syllogism
python3 -OO -m unittest -v test_syllogism
```

四对象独立枚举是有界交叉检查，不单独证明任意论域结论。一般有效性与排除结果分别由正文证明和构造论证承担。程序也不衡量真实辩论者是否接受前提、是否有语言歧义或是否被说服。

## 审查对象 SHA-256

| 对象 | SHA-256 |
|---|---|
| 深读正文 | `e63d4b3baeef64ccd541b303e61881ded19e9441df1148c4e0d079da6074ee03` |
| `syllogism.py` | `fdf976efc9d2ba4ad4be5a952092829f4ab9f4e9bcee61953750798d6ab1c4ef` |
| `test_syllogism.py` | `7c3b78504adb91458c4eaef357d8e65013819c100a325a48d6bf44081c20afcd` |
| `run.sh` | `834caeb7d8778570059597568931fda7c263d12f5f877f15ebe0a1ca0858edf7` |
| 复现 `README.md` | `0c990d1e581178d2e08188bbf8f1342d80d6cb0d724d6d1ae9853f3e31be6175` |

正文或上述实现修改后须重新核对，不能沿用旧哈希的通过结论。
