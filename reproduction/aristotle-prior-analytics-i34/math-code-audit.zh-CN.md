# I.34 数学与代码独立审核

## 结论与范围

2026-10-22 独立检查本文现代教学语义、一般证明、代码及发表计数。审核通过。此结论不是古代模态语义的完备性证明；来源与版本问题由单独来源核验负责。

- 第2.2节固定情境下的 Celarent：任取对象经子集关系与排斥关系即可证明，空集合不破坏证明。未误称有限零失败为一般证明。
- 第3–5节分别可能与同情境共同可能、∀x∃w与∃w∀x的反例均满足前件并否定所述强结论。健康/疾病互斥是声明的教学条件，不是医学结论。
- 状态对象与状态承载者的类型区别、跨情境个体身份等均被明确标作教学重构，不冒充原文公式或完整模态系统。

## 发现并复核的修正

初版聚合函数在空域可绕过条件参数检查；合取的短路也可能漏检第二条件。已要求作者在聚合入口先校验参数，新增两项回归测试。独立脚本明确测试空域的非法字符串/未知状态，以及恒假首条件下的非法第二条件，修复版全部拒绝。真实有限模型的数值结果未改变。

## 独立方法与真实运行

[独立源码](independent_audit.py)不调用作者的计数函数来产生预期值：它按每个人的两情景状态对重新枚举，使用见证集合计算各个量词读法，再逐项比较作者方法；Celarent按每个对象的三个布尔值直接求前件与后件，再与集合实现比较。最后读取results.json核对已发表计数。检查用显式异常，不依赖会被优化移除的裸assert。

```sh
python3 independent_audit.py > independent-logs/audit-default.log 2>&1
python3 -O independent_audit.py > independent-logs/audit-O.log 2>&1
python3 -OO independent_audit.py > independent-logs/audit-OO.log 2>&1
python3 -m unittest -v test_model > independent-logs/tests-default.log 2>&1
python3 -O -m unittest -v test_model > independent-logs/tests-O.log 2>&1
python3 -OO -m unittest -v test_model > independent-logs/tests-OO.log 2>&1
```

三种模式均独立实跑通过；各模式作者测试10项通过。独立范围额外覆盖3人两情景729个赋值；发表的0/1/2人计数一致（模型1/9/81，前提真1/5/25，强结论反例0/2/16，范围交换缺口0/0/8）。Celarent覆盖0–3人1/8/64/512组，前提真1/4/16/64，失败均0。日志目录为[independent-logs](independent-logs)。这些范围之外不作穷尽保证。

## 绑定的文件 SHA-256

下列摘要绑定实际被审文件；正文之后的修改需要重新审核对应差异。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-i34.zh-CN.md`|`ae7c32c1baeaccb7feea2c5bd31cef11fcd1fbd295475edc8d6b9d4a70c91eb0`|
|`reproduction/aristotle-prior-analytics-i34/model.py`|`58468e6ad5b24bb3f5483364c073c45e6c102d0618a462c421996b634ac50ff6`|
|`reproduction/aristotle-prior-analytics-i34/test_model.py`|`7a18695fd52e57dafa995a0d756760c8b1c7929200835ffb9dc29590db7a09ea`|
|`reproduction/aristotle-prior-analytics-i34/results.json`|`cfee22f7b100cdcace6fdd0e1757bf7103e9b61c0333830e5cc50920e0aebf3a`|
|`reproduction/aristotle-prior-analytics-i34/README.md`|`528c468caea652124a39340b8637afe61b9c43d30bd1b33d07f307f1436775a1`|
|`reproduction/aristotle-prior-analytics-i34/independent_audit.py`|`2cfaeb265f9ed282b5f18a14bd6f1b66891c346195f0cd67204e46e45716e59f`|
