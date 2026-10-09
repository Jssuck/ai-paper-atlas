# AI Paper Atlas · AI 论文历史精读

从人工智能的思想与数学前史出发，沿时间线逐篇阅读、解释和核验研究文献。目标是对不同方向、作者与影响力的论文采用一致的阅读标准，而非只整理名作。

## 当前状态

**持续精读阶段。** 深读 v2 标准已确认。已启用每小时定时推进：同一时间只处理一篇；研究、复现或核验超过一个周期时，继续该篇，后续论文顺延，不补发追赶。完成核验后逐篇公开发布。当前论文阶段见 [进度记录](workflow/progress.json)。这不是每小时必定完成一篇的承诺，也不表示某一年代文献已被穷尽。

## 阅读目录

| 时段 | 论文 | 定位 | 状态 |
| --- | --- | --- | --- |
| 1924 | [Schönfinkel《数学逻辑的构件》精读](papers/1924/schonfinkel-building-blocks.zh-CN.md) | AI 前史回填：组合子与变量消除 | 深读 v1 · 含实跑附件 |
| 1931 | [哥德尔不完备性论文精读](papers/1931/godel-formally-undecidable.zh-CN.md) | AI 前史回填：算术化、自指与形式系统边界 | 深读 v1 · 含实跑附件 |
| 1932 | [Church《逻辑基础的一组公设》精读](papers/1932/church-postulates-logic.zh-CN.md) | AI 前史：函数、替换与逻辑基础 | 深读 v1 · 含实跑附件 |
| 1936–1937 | [图灵《论可计算数》精读](papers/1936-1937/turing-computable-numbers.zh-CN.md) | AI 前史：可计算性基础 | 深读样稿 v2 · 含实跑附件 |

样稿不等于历史起点已被唯一确定，也不意味着更早或同期工作会被跳过。后续正式目录需按公开来源、纳入规则和年代逐步补齐，不以名气或引用量决定处理优先级。

## 图灵篇可运行附件

- [复现说明、模型定义和执行命令](reproduction/turing-1936/README.zh-CN.md)
- [交互式教学 Notebook](reproduction/turing-1936/turing_teaching.zh-CN.ipynb)
- [测试日志](reproduction/turing-1936/tests.log) · [运行结果](reproduction/turing-1936/results.json)

已实际执行 15 项单元测试与 9 个 Notebook 代码单元；后者使用标准库顺序执行器，并未通过 Jupyter 内核执行或完成页面渲染验证。小模型实验不构成对一般不可判定性的实验证明，也不是原文通用机的完整复现。

## 哥德尔篇可运行附件

- [编码、替换和有限证明的复现说明](reproduction/godel-1931/README.zh-CN.md)
- [教学 Notebook](reproduction/godel-1931/godel1931_toy.ipynb)
- [45 项测试及演示运行日志](reproduction/godel-1931/logs/test-and-demo-run.txt)

Notebook 的 7 个代码单元使用标准库执行器运行；不声称执行过 Jupyter 内核。有限编码与证明检查示例并非对不完备定理的计算验证。

## Church 篇可运行附件

- [替换规则、历史限制与复现说明](experiments/church1932/README.zh-CN.md)
- [教学 Notebook](experiments/church1932/church1932.ipynb)
- [32 项测试日志](experiments/church1932/tests.log) · [独立交叉核查](experiments/church1932/independent_checks.log)

已运行 8 个 Notebook 代码单元，使用标准库执行器；不等同于 Jupyter 内核验证。代码区分现代 β 约简和 1932 年规则的非擦除限制，不声称复现全部原公设或证明系统。

## 已发现的早期文献缺口

[候选与来源覆盖记录](reading-paths/early-foundations-candidates.json)列出本轮有限搜索发现的更早及同期文献、全文可得性和核查范围。后续优先核验较早的未读候选；无法取得原文的保留待补，不以名气或影响力排序，不声称此清单穷尽历史。

## Schönfinkel 篇可运行附件

- [组合子、变量消除与有限逻辑模型复现](reproduction/schonfinkel-1924/README.md)
- [教学 Notebook](reproduction/schonfinkel-1924/tutorial.ipynb)
- [11 项测试及分项检查](reproduction/schonfinkel-1924/logs/unittest.txt)

实跑包含 1,400 个替换例、64 个谓词对、两个高阶 U 有限模型与 8 个 Notebook 代码单元。Notebook 用标准库顺序执行，不声称 Jupyter 内核验证；有限模型不构成一般逻辑一致性证明。

## 每篇解析的共同标准

- 原始书目信息、版本和全文来源
- 当时的问题背景及与前人工作的关系
- 方法、定义、关键公式与论证的逐步解释
- 对实验型论文核对实验设置、对照与结果；对理论论文核对假设、证明结构与适用边界
- 作者主张、原文证据与分析判断分别呈现
- 局限、修正记录、可复核步骤，以及实际执行与未执行项目
- 对后续研究的关联保持证据约束，避免以今日观点替代历史事实

## 公开内容与核验边界

这里发布 AI 辅助撰写的原创中文解析、书目与原文链接，不镜像论文全文或 PDF。每篇注明实际阅读与核验范围；示意推导不冒充原文公式，概念练习不冒充已运行实验。发现错误后保留更正记录。原论文版权归各权利人所有。
