# Condillac《逻辑》II.I：观察纠错与互相支持

原创 Python 标准库教学重构，配合《La Logique》第二部第一章阅读。实际底本是 1798 年版《Œuvres de Condillac》卷 XXII，印刷页 96–108。1780 是作品已核书目年，未在本次独立认证最早版次、1780 章内影像或逐字文字。目录名不表示使用了1780扫描。

两个小模型分别回答：新观察排除了哪些候选？哪些判断只是相互支持，哪些能从外部给定锚点建立？词义不可区分的例子复用第一个模型。没有心理学实验、历史算法复原、现代AI性能评估或自动语义理解的主张。

## 运行环境与精确命令

需要 Python 3.10 或更新版本；只用标准库，无需 pip、网络、API 密钥、GPU 或数据下载。实际使用的解释器、系统、每条命令的退出码及源码摘要见 [environment.json](environment.json)。最低语法版本不等于已在所有新旧版本上测试。

在本目录执行：

```bash
python3 -B run_all.py
python3 -B demo.py
python3 -B -m unittest -v test_model
python3 -O -B -m unittest -v test_model
python3 -OO -B -m unittest -v test_model
python3 -B exhaustive.py
python3 -O -B exhaustive.py
python3 -OO -B exhaustive.py
python3 -B mutation_check.py
```

run_all.py 会生成或覆盖当前目录中的日志和环境记录，并把汇总实际保存到 logs/run-all-summary.json。修改代码后必须重新运行，旧日志不证明新代码已通过。它对每项外部进程设置180秒保护；超时不计为通过。

mutation_check.py 在本目录创建并清理隔离临时副本，只在副本里改变 model.py。它自己启动正常、-O、-OO 三组子进程，因而不必再从外面重复三次。真实超时控制会有意暂停并被终止；控制的预期失败不等于发布模型失败。

没有 notebook 文件、内核启动或 notebook 执行声明；全部证据来自上述实际 Python 命令。

## 阅读顺序与文件

1. [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：先手算，再查看每一步输出；包含覆盖缺失、错误证据、循环、单点撤回、替代支持和词义反例。
2. [MODEL.zh-CN.md](MODEL.zh-CN.md)：所有符号与假设、一般证明、时间与输入成本、API 边界、原文与现代补充的区别。
3. [model.py](model.py)：约150行，两个纯函数式有限模型；只用标准库。
4. [demo.py](demo.py) 和 [logs/demo.json](logs/demo.json)：稳定排序的实际例子输出。
5. [test_model.py](test_model.py)：40项作者 unittest 方法；校验不会因 -O 或 -OO 而消失。
6. [exhaustive.py](exhaustive.py)：作者确定性有限枚举；不是独立审计，不替代 MODEL 的证明。
7. [mutation_check.py](mutation_check.py)：人工选定行为突变与测试装置控制，分类独立报告。
8. [logs/run-all-summary.json](logs/run-all-summary.json)：总命令状态；[logs/mutation-summary.json](logs/mutation-summary.json) 为突变简报，完整结果在 [logs/mutation/report.json](logs/mutation/report.json)。

## API 一览

- filter_evidence(H, observations, initial=None)：返回包含 C₀ 的全部候选状态；每条观察是 H 的相容子集。
- Rule(body, head)：非空合取前提到一个结论；空前提必须改为显式锚点。
- HornSystem(V, rules).immediate(S, anchors=A, withdrawn=W)：计算一次 T(S)。
- HornSystem(V, rules).fixed_point("least", anchors=A, withdrawn=W)：从∅重新计算最小不动点。
- 将上项 "least" 改为 "greatest"：从 V\W 重新计算最大不动点。
- 返回的 FixedPoint.states 包含起点与每次严格变化，不含最后重复的稳定状态；result 是末状态，changes 为严格变化次数。

输入为有限非空字符串标签的集合或迭代器；全集本身允许为空。字符串 "abc" 不能冒充 {"a","b","c"} 的集合。集合之外的标签会报错。公开结果是不可变快照。直接构造 FixedPoint 只验证记录形状，不认证其手填轨迹已满足某组规则。

## 本次作者验证的实际范围

正常、-O、-OO 三模式各执行40项测试方法。三种模式在子进程中分别报告优化等级0、1、2，不能只是给最外层脚本加一个选项便声称优化测试已完成。

证据枚举使用 H={a,b,c}，共8个子集；初始集合取全部8种，观察长度取0到3，每次观察取全部8种子集。

- 历史数：8×(1+8+8²+8³)=4,680
- 每历史检验3个指定真候选：14,040次保真检查，另有14,040次唯一识别检查
- 排列检查：8×(0!×1+1!×8+2!×8²+3!×8³)=25,672；对重复观察也保留位置排列，因而有重复输入，不能当成25,672个不同历史

完整二判断 Horn 枚举：V={a,b}；非空前提有3种，每种可指向2个结论，因此6种规则、64个规则子集。锚点4种、排除项4种，共1,024个系统上下文。

- 直接枚举允许域的所有候选不动点：2,304个候选状态
- 算子单调性：4,096个包含关系状态对
- 撤回比较：64×3²×3²=5,184个参数对；分别比较 L 和 G，共10,368次

三判断补充枚举：V={a,b,c}，只允许单元素前提，因此9种规则、512个规则子集；锚点8种、排除项8种，共32,768个系统上下文与110,592个候选状态。它不是全部三判断合取 Horn 系统的穷举，后者有21种可选规则。每个上下文都以直接定义枚举不动点，并比较 L/G、轨迹、稳定性与变化次数上界。

各模式完整枚举报告分别位于 logs/exhaustive-normal.json、logs/exhaustive-O.json、logs/exhaustive-OO.json。以上统计单位互有重叠，不能相加成彼此独立的样本总数。

## 突变与装置错误必须分开

13个当前选定的行为突变，在三种模式下共39次运行。它们覆盖交集误写、遗忘旧证据、忽略初始覆盖、漏掉输入校验、偷加空前提、合取变析取、遗漏合取规则、丢锚点、丢排除项、让旧状态自我担保、错误迭代起点和过早停止。实际结果以本次日志为准，不凭预期编造。

一次“行为杀死”必须同时满足：

- 所有预定40项测试都开始并结束，方法身份和顺序与预定清单一致
- 子进程真实优化等级正确
- 只有断言失败，没有测试异常、跳过、预期失败或意外成功
- 有且仅有一个有效完成标记，退出状态与失败数相符

每模式另运行7个装置控制，共21次：语法错误、导入错误、提前正常退出、空套件、重复完成标记、测试运行异常与真实超时。它们分别识别为 harness_error、suite_mismatch、test_error 或 timeout，不计入行为杀死。

这是人工选定的有限错误集，不是所有可能错误的穷举，也不是独立验证。运行过程中发现会破坏单调性而振荡的探索性变异曾被正确识别为超时；最终行为组改用可正常完成的定点语义错误，真实超时另外保留为装置控制。未把超时改称成功杀死。

## 独立复核

独立审计由另一位审阅者编写，单独保存在 independent-review/，不把作者脚本的通过数当成独立证据。如果独立入口 independent-review/run_audit.py 存在，run_all.py 将调用它一次；该独立入口自己启动正常、-O、-OO 三模式，并保留实际子进程记录；没有该入口时，只记录作者验证并明确标为缺席。

独立报告自身说明所用参考算法、枚举范围、边界及实际结果。以 [independent-review/review.zh-CN.md](independent-review/review.zh-CN.md) 为准；不得仅因目录存在就声称审计通过。

## 四个不能省略的限制

- 观察淘汰保留真相，需要真实解释一开始就在候选内，且每次相容编码没有错排它。候选变少不等于越来越正确。
- L 表示相对于锚点的有限推导；G 允许循环互保。锚点或规则不可靠时，L 同样可能承载错误；不在 L 中也不等于为假。
- 从 A 中撤销根据，与加入 W 强制排除，是不同动作。替代支持存在时，撤回一个判断未必消灭所有判断；简单无锚点循环中，排除一个节点却可以让全圈消失。
- 代码不决定应撤回哪一项，不生成新假设、不模拟权势、从众、习惯顽固或教育效果。一般数学证明、有限程序验证与关于人的经验命题不能互相替代。

开发时完整阅读所提供页96–108文字抽取；OCR仅为阅读辅助，原典逐页影像和版本核查见配套[来源账本](../../papers/1780/condillac-logic-part2-ch1.sources.zh-CN.md)。发布包不含整章转录、扫描PDF或原书图像，运行也不依赖它们。
