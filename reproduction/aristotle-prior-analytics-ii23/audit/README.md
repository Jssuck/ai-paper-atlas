# 独立技术核验

[返回复现说明](../README.md) · [技术审查](../../../papers/ancient/aristotle-prior-analytics-ii23.technical-review.zh-CN.md)

`independent_oracle.py` 不导入生产模块，不使用位掩码包含算法：用组合枚举 `frozenset`，逐元素判断，逐个列出反例扩张，并检查覆盖失败时的构造见证 A=C。另用局部成员模式的闭式计数校验：各论域大小 n，完整归纳前提3^n，最小传递4^n，观察且分类5^n，非空特称5^n−4^n，失败定位前提6^n，全部世界8^n。对 n=0..4 求和。

运行先在上一层执行 `sh run.sh` 生成生产结果，然后：

```sh
sh audit/run-audit.sh
```

脚本真实运行普通、`-O`、`-OO` 三种模式的独立oracle和比较程序。每次比较4681世界的5规则汇总、逐n计数、弱前提统计、341个全A量化配对，以及独立集合表示的6个具名反模型。总规则评估23405，但只有满足相应前提的世界计入各规则的有效性检查；不将空前提模型算成实际证据。

- [独立算法](independent_oracle.py) · [比较器](compare_production.py) · [运行脚本](run-audit.sh)
- [普通oracle](oracle-normal.json) · [普通比较](comparison-normal.json)
- [-O oracle](oracle-O.json) · [-O比较](comparison-O.json)
- [-OO oracle](oracle-OO.json) · [-OO比较](comparison-OO.json)

结果全部匹配。闭式计数用于发现枚举遗漏；一般蕴含的正确性仍由正文元素证明负责。独立核验不是另一次生物学实验，也不能建立历史解释或样本外统计保证。算法仅Python标准库，未安装依赖；运行环境见[真实环境记录](../results/environment.txt)。所有检查显式抛异常，不依赖会被优化删除的 `assert`。
