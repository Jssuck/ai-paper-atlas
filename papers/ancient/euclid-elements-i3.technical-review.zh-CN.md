# 《几何原本》I.3：独立技术审查

> 核验日期：2026-10-26。对象为本仓库原创中文解析与标准库教学复现。本审查独立检查数学推导、实现和实际证据；不是古代文本来源审查、专家签名或证明助理认证。最终版本摘要见第7节。

## 1. 结论与适用范围

**在明确的实数平面数学合同及 `Point` / `Certificate` 有理坐标接口合同内，未发现阻断性数学或实现错误。** 解析生成、坐标证书检查、有限实验及原始尺规构造认证已作区分。公开结果不能扩大为“完整证明了欧几里得”“执行了I.2”或“支持全部实数／代数数输入”。

实际复跑原有33个 `unittest` 方法，普通、`-O`、`-OO` 三模式均通过；不是99种独立测试。另写了不同逻辑的独立oracle，三个模式各通过47,806个检查组合，输出相同。Notebook在副本中重新执行后，解析得到的整个JSON对象与发布版一致，确认5个总单元、3个代码单元及顺序执行编号；这仍是标准库执行，**不是Jupyter kernel运行**。

本报告只修改自身与 `reproduction/euclid-elements-i3/audit/`，不把改动被审实现当作“独立审查”。历史版本、引用与原文定位另见[独立来源审查](euclid-elements-i3.source-audit.zh-CN.md)。

## 2. 数学推导的独立复核

### 2.1 存在、内部、等长与唯一

设 `v=B−A`、`L=||v||>0`、`0<c<L`。取 `t=c/L`，则 `0<t<1`，`E=A+tv`存在于实数平面且严格位于AB内部；`||E−A||=tL=c`。若另一个内部点为 `A+sv` 且距离为c，则 `sL=c`，所以 `s=t`。余段长 `(1−t)L=L−c>0`。

这里的存在性依靠明确选用的实数平面，不是声称仅凭“可以画圆”已形式证明交点存在。唯一性只针对从A端沿AB截取的指定版本，不针对整个圆周或未选端点的两个截取版本。

### 2.2 不开平方的候选检查是双向规格

令 `w=E−A`、`q=v·v`、`C=c²`，并保留 `c>0` 的长度语义。下列条件组与目标等价：

$$
q\gt 0,\quad 0\lt C\lt q,\quad v\times w=0,\quad 0\lt v\cdot w\lt q,\quad w\cdot w=C.
$$

在二维实数平面，`q>0`排除零向量；叉积为零给出 `w=sv`；内积界成为 `0<sq<q`，故 `0<s<1`；平方长度给出 `s²q=C`。由于长度非负且目标为正，得到所需距离。反向从严格内部正确截点代入，也得到全部条件。没有把“有限测试通过”作为这个一般证明的理由。

额外的D检查要求 `||D−A||²=C`。代码同时检查AD目标等式、圆关联等式和AE目标等式，故有有意的冗余；第6项可由前两项等式推出。**充分必要的条件组不等于每个列出条件都逻辑独立、缺一不可。** 这些命名检查用于定位错误，而不是声称最小公理集合。

### 2.3 手算与反例

正文手算 `A=(1,−2), B=(7,6), c=4` 给出 `E=(17/5,6/5)`；复核得 `q=100`、叉积0、内积40、`AE²=16`、余段长6，`D=(1,2)`也确有 `AD²=16`。

反向点通过长度和共线性但违反正向位置；同距离离线点通过长度却不在AB上。更强的有理反例 `E=(6/5,8/5)` 相对于 `A=(0,0), B=(5,0), c=2`，内积为6、平方距离为4，但叉积为8，表明内积界不能单独替代共线性。等长、过长、零长和退化AB均不满足严格题设。正确E配错误D，最终目标成立却不能让整份包含D的证书通过。正文这些区分均成立。

## 3. 实现合同及精确表示范围

- `Point`坐标及目标平方长度接受 `int` / `Fraction`，排除 `bool`、浮点数和字符串；没有浮点容差。代码参数 `c` 的实际语义是平方长度C，不能与正文中的长度c混用。
- `verify`不取平方根；在声明的类型域中，所得六项布尔条件与上面的数学合同一致。`A=B`优先分类为退化，即使同时C负或零；退化输入不会因全部距离为零而通过。
- `rational_sqrt`对约分后分子、分母分别作整数平方根检查；非平方有理数明确报 `RationalWitnessUnavailable`，负数报 `ValueError`。
- `analytic_witness`只处理**目标长度和AB长度分别有理**的子族，而不是所有有理点可表达的截取。更一般地，对给定有理A、B和C，正确E有理的必要充分条件是 `√(C/q)` 有理；实现并没有利用这一更宽条件。它是有意受限生成器，不是完整求解器。
- 正文新增 `A=(0,0), B=(2,2), C=2, D=E=(1,1)` 已专门实际检查：验证通过，生成器报不支持。`B=(1,1), c=1`则需要无理坐标E；有理表示失败不能推出几何无解。
- 若未传D，程序直接以坐标给出 `A+(0,√C)`；这不执行I.2，也不证明D的构造来源。没有连线、延长、画圆、选交点的历史轨迹检查。
- **接口不是不可信外部数据的schema验证服务。** 结构损坏的对象，如 `None`、元组冒充Point或缺失D，可能抛 `TypeError` / `AttributeError`，不会统一返回 `valid=False`。本次独立检查明确验证了这一限制，而未把它包装为友好输入处理。

## 4. 独立oracle及计数

源码：[independent_oracle.py](../../reproduction/euclid-elements-i3/audit/independent_oracle.py)。它不调用实现中的 `dot`、`cross`、`norm2`、`domain_status` 或原实验族来决定期望值。它从v的一个非零坐标直接求参数s，再检查两个坐标的仿射关系 `E=A+sv`、`0<s<1`及独立写出的平方距离等式。这个算法是对语义合同的另一种表达，不是复制原验证器六个布尔表达式。

| 每模式检查组 | 数量 | 实际结果 |
|---|---:|---|
| 三个平移原点、九个方向/退化位移、49个候选偏移、九种目标、四种D组合 | 47,628 | oracle接受21、拒绝47,607；实现逐项一致 |
| 无理长度但有理坐标证书，验证器通过而生成器不支持 | 36 | 符合声明 |
| 正文新增B=(2,2)、C=2例子 | 1 | 验证通过，生成不支持 |
| 另外的整数毕达哥拉斯向量、比例、尺度与平移生成样例 | 72 | 与独立坐标答案一致 |
| 10¹⁸⁰平移及10⁻¹⁸⁰级端点间隔 | 3 | 精确保留严格内部点 |
| 11种非法数值分别用于五处入口 | 55 | 均抛TypeError |
| 非严格目标分类及生成拒绝 | 4 | 符合合同 |
| 退化AB的分类优先级 | 3 | 均拒绝 |
| 结构错误的Python对象 | 4 | 抛异常，未当成有效证书 |
| **合计** | **47,806** | **三个模式分别通过且JSON结果一致** |

这是检查组合/调用组的计数，不是47,806个互异几何图形；循环中D或目标可能重复，部分组内部有多次断言。三种优化模式重复同一套组合，不累加为三倍“独立测试”。有限格点检查不是随机统计、代码覆盖率声明或一般正确性证明。

## 5. 原证据、优化模式与Notebook复核

审查入口：[run_independent_audit.py](../../reproduction/euclid-elements-i3/audit/run_independent_audit.py)。它只在 `audit/` 写审查结果，Notebook在临时副本中重跑，不改被审源码或作者的 `evidence/`。

实际执行内容：

1. 三模式分别重跑原33个 `unittest` 方法；逐方法成功名单相同。
2. 三模式分别运行独立oracle；比较完整JSON结果相同。
3. 单独重跑 `experiments.py`；与发布 `evidence/results.json` 的600正例、2,400反例及各维度、分类计数相同。
4. 原记录内七个源文件摘要与实际文件一致。
5. 在副本执行Notebook并比较整个解析后的JSON对象；发布输出、执行编号和元数据一致。代码单元按1、2、3执行。
6. AST扫描被审Python源码和独立审查脚本，Python `assert`语句数均为0；使用 `unittest` 方法或显式异常。因此这里没有因为 `-O` / `-OO` 删除assert而得到空泛通过。
7. 运行前后摘要一致才生成最终通过结果，防止在并发改写时把旧测试绑定到新源码。

日志和结构化结果都来自实际执行，而非手填预期输出：

- [原测试普通模式](../../reproduction/euclid-elements-i3/audit/original_normal.log)、[-O](../../reproduction/euclid-elements-i3/audit/original_optimized.log)、[-OO](../../reproduction/euclid-elements-i3/audit/original_double_optimized.log)
- [独立oracle普通模式](../../reproduction/euclid-elements-i3/audit/oracle_normal.log)、[-O](../../reproduction/euclid-elements-i3/audit/oracle_optimized.log)、[-OO](../../reproduction/euclid-elements-i3/audit/oracle_double_optimized.log)
- [实验族重跑](../../reproduction/euclid-elements-i3/audit/independent_experiments.log)、[Notebook副本重跑](../../reproduction/euclid-elements-i3/audit/independent_notebook.log)、[审查结构化结果与摘要清单](../../reproduction/euclid-elements-i3/audit/results.json)

Notebook执行器仅用 `compile/exec`、共享命名空间、stdout捕获。没有Jupyter kernel、magic、富显示、隔离或完整nbformat schema校验；当前环境也未为审查安装依赖。成功重放仅认证这份教程的普通Python代码和记录输出，不能推广成通用Notebook兼容性结论。

## 6. 如何复跑及如何解读通过

在复现目录执行：

```sh
python audit/run_independent_audit.py
```

命令重建审查日志及 `audit/results.json`。它要求作者证据的源文件摘要仍匹配；若先改动实现，请先重新生成作者证据，再重新审查。摘要不匹配或运行期间文件变化会拒绝出具本轮最终PASS。审查完成后若继续修改正文、README或源码，本报告的旧摘要即不再覆盖新版本，必须重跑并重绑定。

通过意味着：本次快照的数学论证经独立推导复核，已执行的有限检查和发布记录一致。在未测输入上仍可能有程序缺陷；并无形式证明、完整尺规过程认证、历史出处认证或全部实数输入覆盖。

## 7. 最终版本绑定

本表由最终实际执行的 `audit/results.json` 生成；正文、七个复现文件及两个独立审查脚本在该次执行前后保持相同摘要。报告不对自身作循环摘要。

审查完成时间（UTC）：`2026-10-26T19:56:37.539910+00:00`；结果：**PASS**。环境：CPython 3.12.14，Linux x86_64，无新增依赖。

| 发布相对路径 | SHA-256 |
|---|---|
| [papers/ancient/euclid-elements-i3.zh-CN.md](euclid-elements-i3.zh-CN.md) | `8da74b81a5325a58dea7ba8703d4d7d24aac45dd0a8e0a4aa1b85901fdabf994` |
| [reproduction/euclid-elements-i3/euclid_i3.py](../../reproduction/euclid-elements-i3/euclid_i3.py) | `231c54693bc9e407b2f2c522abbaa428eebc88ef0673a2b7174c17c1e94dbc3c` |
| [reproduction/euclid-elements-i3/experiments.py](../../reproduction/euclid-elements-i3/experiments.py) | `f18c8cf22ed3e6b5f7b1312845c27a88a92d1a64ecb966c1fcbdf5c3dee03549` |
| [reproduction/euclid-elements-i3/test_euclid_i3.py](../../reproduction/euclid-elements-i3/test_euclid_i3.py) | `d8a1b0801900562fdb44b5f79bac5aaf22ef5e560900058bab7c24ddda11e08e` |
| [reproduction/euclid-elements-i3/execute_notebook.py](../../reproduction/euclid-elements-i3/execute_notebook.py) | `4051c73e93420b5720aac37ba7bfcad135ba696db9c070d43225d8e99dc745ff` |
| [reproduction/euclid-elements-i3/run_checks.py](../../reproduction/euclid-elements-i3/run_checks.py) | `13bae1fa926405bed7790d8c83ec1a14d6314dae4473cfe153b4acd4b52c2e3f` |
| [reproduction/euclid-elements-i3/tutorial.ipynb](../../reproduction/euclid-elements-i3/tutorial.ipynb) | `62c2c689ba27f8408e65f3838e9a5304f2c6c24a5ec25be4aa94b73498c1d63a` |
| [reproduction/euclid-elements-i3/README.md](../../reproduction/euclid-elements-i3/README.md) | `3fac56a43844d86672100e203fa3d7b9340bc08d6ed98817db4299b0b2c71e85` |
| [reproduction/euclid-elements-i3/audit/independent_oracle.py](../../reproduction/euclid-elements-i3/audit/independent_oracle.py) | `417ec1088271391d234910ff54772f6506df04d96e1ea5cceeafa0acaba8c7a9` |
| [reproduction/euclid-elements-i3/audit/run_independent_audit.py](../../reproduction/euclid-elements-i3/audit/run_independent_audit.py) | `07be21235972c59a1589cbf16104f0c568ec8a4b5c9c74293608ad9622548cd3` |

`audit/results.json` 自身SHA-256：`2bc266c2a94ed6fb67c9d745eafb277c803d1c625036ae54a9d214992d3cb57a`。

作者证据及本次八份日志的摘要另保存在该JSON的 `evidence_sha256` 中。所有公开命令与文件引用使用项目相对路径，不含私人工作目录。
