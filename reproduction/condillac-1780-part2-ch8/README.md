# 数据够了吗？改写改变了什么？

孔狄亚克《逻辑》第二部第八章（1780年著作；本次据1798年印本实际页170–176）的现代、有限教学模型。仅用 Python 3.10+ 标准库，无安装、账号或网络要求。核心模型与演示不使用随机数；独立审核可另用固定种子产生可重跑的补充案例。它不是历史算法复刻，也不验证感觉论心理学。

## 快速运行

在本目录运行：

```sh
python3 demo.py
python3 -m unittest -v
python3 mutation_check.py
python3 walkthrough.py
python3 verify.py
```

- `demo.py`：输出确定性 JSON，包含资料充分性、筹码改写链、压缩纤维、最少补问树和共同出现不等于因果起源的反例。
- `walkthrough.py`：直接执行 [中文演练](WALKTHROUGH.zh-CN.md) 中全部 Python 代码块，文档与可执行例子共用一份内容。
- `verify.py`：真实重跑普通、`-O`、`-OO` 模式，保存 stdout、stderr、退出码、环境及源码哈希。任一命令失败或应确定的演示跨模式不同即失败。仅覆盖本地 `evidence/` 与验证说明。

## 先看四个结论

1. “数据充分”必须说明对哪个问题充分。两个世界可有同一答案；充分不要求查明整个世界。
2. 保持候选世界集合的改写比保持当前答案集合更强。补充资料另列为操作；不能把排除可能性伪称等义改写。
3. 表示压缩是否足够，看同一编码纤维中是否可能有不同答案。这个判准不保证编码资料已取得，也不提供免费观测。
4. 对三个比特 `s,a,b`，若目标是 `s=0` 时答 `a`，否则答 `b`，先问 `s` 再问选中的比特，最坏两问；任何固定两问都不够。

## 文件

- [模型、证明和边界](MODEL.zh-CN.md)
- [逐步可执行演练](WALKTHROUGH.zh-CN.md)
- [实际运行记录](VERIFICATION.zh-CN.md) 与 [机器汇总](evidence/summary.json)
- `condillac_model.py`：有限语义、改写、压缩和决策树
- `examples.py`、`demo.py`：明确的玩具世界与输出
- `test_condillac_model.py`：输入拒绝、反例和小规模穷举
- `mutation_check.py`、`test_mutation_check.py`：13种行为故障探针及故障分类器测试；异常不算击杀
- `independent_argument_checks.py`：由另一审计者编写的位掩码／分割与逐层决策树存在性 oracle；范围与实际数字见其输出
- `verify.py`：可重跑的日志生成器
- [独立代码审核](independent-review/review.zh-CN.md) 与 [重跑脚本](independent-review/run_review.py)：完整策略枚举 oracle、输入边界，以及验证器／变异分类器自身的故障检查；与作者测试分开

## API 速查

`Universe(fields, worlds)` 固定字段和有限世界顺序。两项均为元组；坐标只能是精确的整数或字符串，拒绝 bool、float、重复世界及维度不符。允许空世界域，但显式判为没有可识别答案。

`Table(u,name,values)` 是每世界一值的全域表，可用于目标、编码或观测问题；值为精确整数、字符串及递归元组。`Constraint(u,name,mask)` 是每世界一个真正 bool 的全域条件。`table(u,name,fn)` 与 `constraint(u,name,predicate)` 把回调一次采样为表；调用者负责回调纯度及假设的正确性，程序不证明任意 Python 函数确定性。

`Problem(u,target,constraints=())`、`analyze(p)`、`candidates(p)` 构成问题与解答。候选以世界索引元组返回；状态是 `inconsistent`、`identified`、`underdetermined`。只有 identified 可读取 `.answer`。

`compare_rewrite(before,after)` 要求相同有序世界域及目标映射，返回保持世界、保持答案和非空性标志，以及丢失／新增世界索引。`translation_chain(tuple_of_problems, preservation='worlds')` 逐步核对；可显式选 `'answers'`。`add_evidence(p,c)` 添加合取条件，返回新问题。

`compression(p,encoding)` 返回 `sufficient`、`vacuous`、有限 `decoder` 和冲突 `witness`；`.decode(code)` 仅接受候选支持的编码。`minimax_tree(p,questions)` 返回有限最坏问数最优树；同价优先输入中较早的问题。`follow_tree(p,questions,tree,i)` 回放一个候选世界，返回答案及问题名路径。

`Analysis`、`RewriteReport`、`Compression`、`DecisionNode` 是函数返回的受信任结果记录，不是经过完整校验的外部输入格式。`follow_tree` 仅用于本次 `minimax_tree` 生成的树，调用者须保留相匹配的问题与观测表；它不是任意树的认证器。

## 历史与计算边界

170–172页谈资料和问题的明确表达；173–175页把这种方法推广到理解能力的起源；176页把推理描述为传递同一性的翻译序列。模型只对这些问题作现代辨析。它没有把第九章带入选读，也没有把印本变量行的转录问题交给程序裁决。

筹码枚举只核对0至10的有限整数域。把上界错误设为6会得到 inconsistent，而不是证明原问题无解。因果玩具的两个世界是人为规定的逻辑反例，不是关于真实认知过程的数据。运行通过不证明孔狄亚克的跨学科主张。
