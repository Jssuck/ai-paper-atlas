# II.26 独立技术核验

[技术审查](../../../papers/ancient/aristotle-prior-analytics-ii26.technical-review.zh-CN.md)另列正文证明、练习和最终文件哈希。本目录为独立审查实现与真实运行记录，不是作者自测的改名副本。

生产实现用位掩码与集合关系；[independent_oracle.py](independent_oracle.py)独立枚举每个对象的三项布尔成员身份，逐对象使用`all`/`any`计算各前提、结论和目标真假。它不调用生产实现的谓词或枚举函数来形成期望值，仅在得出期望值后调用被测`certificate()`比对完整返回字段，并最后比较聚合计数。

范围是域大小0–4，包含空域、空项及同构重复，4681个带标签世界。每世界6路线，每模式28086次完整证书比较。普通、`-O`、`-OO`均无差异；生产16项测试也由审查者逐模式重新执行。有限结果不证明任意域定理，不验证古代科学分类事实，也不衡量对话者对前提的接受度。检查条件用显式异常，不因优化删除。

复跑（Python标准库、Bash，环境沿用[environment.json](../environment.json)）：

```bash
cd reproduction/aristotle-prior-analytics-ii26/audit
bash run.sh
```

脚本会覆盖本目录自己的日志，不改作者日志；耗时可能变化。

- [独立实现](independent_oracle.py)、[命令脚本](run.sh)
- oracle：[普通](oracle-normal.json)、[-O](oracle-O.json)、[-OO](oracle-OO.json)
- 测试复跑：[普通](tests-normal.log)、[-O](tests-O.log)、[-OO](tests-OO.log)
- [三模式比较](comparison.log)

## 不依赖程序的计数交叉检查

按单对象的允许身份计数，上位两路线及第二格负路线各允许4种身份，故0–4域合计 $`\sum_{n=0}^{4}4^n=341`$。再限制B为空各有3种身份，得 $`\sum_{n=0}^{4}3^n=121`$；真正反驳数是220。

两下位路线在未要求C非空前各允许5种身份，C为空时有4种，故见证存在数为 $`\sum_{n=0}^{4}(5^n-4^n)=440`$。第一格特称路线先满足C包含于A时每对象有6种身份，排除B与C的共同见证后剩5种，因此 $`\sum_{n=0}^{4}(6^n-5^n)=774`$。域为空时这些差值均为0。这些等式解释计数来源，并不把有限世界枚举当成形式定理证明。
