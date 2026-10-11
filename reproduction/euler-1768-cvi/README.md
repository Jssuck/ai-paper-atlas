# 欧拉第 CVI 信：三段论的有限支持教学复现

这是原创、离线、仅用 Python 标准库的教学程序。研究范围只有《Lettre CVI》，不把前后相邻信件纳入。本项目不是欧拉原代码，也不声称复原了他的实际操作步骤。

## 先看结论

- 原信按四格列出 **19 式**，各为 4、4、6、5。
- 在明确允许空类的现代集合语义下，**15 式**无需附加存在假设。
- 原列另外四式所需的最小类存在条件：III-AAI、III-EAO、IV-EAO 需要 M≠∅；IV-AAI 需要 Q≠∅。
- 若统一要求 P、Q、M 都非空，256 个候选式中有 **24 个有效式**。按同格同前提比较结论，排除五个严格弱化结论后，剩下的 **19 式精确等于原表**。
- 另一个现代对应：只要求 Q、M 非空、允许 P 为空，也恰得原表 19 式。这些对应都不能单独证明欧拉的历史语义。

P 是结论主项，Q 是结论谓项，M 是中项。特别注意，127 页例子的类名 `class_A` 和命题类型 A（全称肯定）是不同概念。

## 三条命令复跑

需要 Python 3.10 或更高版本；无需 pip、网络、API 密钥或收费服务。在本目录运行：

```sh
python3 -m unittest discover -s tests -v
python3 tests/independent_audit.py
python3 syllogisms.py report --output results/report.json
```

也可用 `bash run_all.sh` 重跑并保存环境、测试、审计、查询示例和报告日志。脚本只在本目录写入 results/ 与 logs/；不安装软件，不联网。运行前若想保留旧日志，请自行备份，因为同名日志会被覆盖。

## 询问一个式

```sh
python3 syllogisms.py query 3 AAI
python3 syllogisms.py query 3 AAI --exists M
python3 syllogisms.py query 4 AAI --exists P M
python3 syllogisms.py query 4 AAI --exists Q
python3 syllogisms.py query 1 AAI --exists P
```

第一条会给出反模型；第二条变为有效。第三条仍然无效，说明第四格 AAI 不能只假定中项存在。第五条演示原表未列、但加入 P 存在后可由 AAA 弱化得到的第一格 AAI。

输入要求：格为 1–4 的整数；式为严格大写的三字符 A/E/I/O；`--exists` 只接受不重复的 P、Q、M。错误输入以退出码 2 和简短错误说明结束。`query` 中有效/无效本身都以退出码 0 正常返回；请读取 JSON 的 `valid` 字段，不要用退出码表示逻辑有效性。

## 文件导航

- `syllogisms.py`：语义、穷举、最小存在条件、严格结论支配、命令行。
- `MATHEMATICS.zh.md`：独立于运行的支持压缩完备性证明、全部十九式逐式推导、四个存在条件的必要性反例、15/19/24 区分、四项歧义例。
- `WALKTHROUGH.zh.md`：从原文到变量和结果文件的逐步阅读说明。
- `tests/test_syllogisms.py`：回归单元测试，包括全部 2048 个式/存在制度组合。
- `tests/independent_audit.py`：独立生成类集合的复核程序，含更小带标号论域的反模型检查及去掉原表仍得相同结果的非循环性检查。
- `results/report.json`：全部 256 式、两个核心语义制度的检查和反模型、每式全部最小存在假设、八种制度摘要、原表顺序、四个条件式的具体反例。
- `results/source_map.json`：公开扫描链接、影像页码、原信范围、转录顺序、输入指纹记录位置及现代增补声明。
- `results/environment.json`：实际执行环境。
- `logs/`：真实命令输出，未手写伪造测试通过记录。
- `REVIEW.zh.md`：独立审阅范围、结论与边界。
- `requirements.txt`：说明无第三方依赖。

## 结果不是只有「测过小集合」

程序穷举八个 P/Q/M 隶属原子的 255 个非空支持；其中三类皆非空者有 218 个。数学证明表明任意大、甚至无限论域的此类模型，都可按隶属型压缩到这些支持之一而保持命题真值。因此这套穷举对已声明语言是完备的。此证明见数学说明第 3 节；它与实际运行证据分开呈现。

程序检验已经形式化的三个固定类，不处理自然语言歧义、等词、对象数约束、模态命题，也不自动证明历史解释。所有源数据转录与现代附加规则均分开保存。
