# I.40 教学复现：目标不相同，不能删字后当作同一命题

本目录是对[中文深读](../../papers/ancient/aristotle-prior-analytics-i40.zh-CN.md)所列现代教学模型的低成本检查，不是原作者程序或完整古代逻辑复原。实际阅读 Owen 1853 印165第XL章后，将其“善／那善”的目标区分抽象为两个不同的结构化公式。**这不主张希腊定冠词总表达唯一性，也不将原章等同于现代描述词理论。** 本模型没有给古代伦理问题作真值裁决。

## 模型、输入与语义

`Model(n, good, p, g)` 的论域为整数0至n−1；n必须是正整数，两个指定对象p和g必须属于论域，`good`为论域子集，可以为空。对象编号没有伦理含义。布尔值不能冒充整数对象，越界解释会报错。

|代码公式|现代教学意义|不是何种主张|
|---|---|---|
|`GOOD_P`|p属于性质G的外延|不是“p就是那善”的同义改写|
|`IDENTITY`|指定对象p和g相同|不预设g满足G|
|`GOOD_G`|指定对象g满足G|不是由变量名字自动保证的事实|
|`AT_MOST_ONE_GOOD`|至多一个论域对象满足G；空G亦真，不保证存在|不是程序从冠词识别出的历史语义|

这里把g当作普通指定对象而不自动强制G(g)，目的是把桥接条件显式展示出来。因此p=g但G(p)假的模型只说明“没有桥接条件”的形式不蕴含，并非用来论证“那善不善”的古代结论。若约定g在所有模型里都满足G，便已添加了桥接条件，反向反模型不再属于该模型类。

## 两个核验层

1. `holds` 在一个给定有限模型中计算四种公式真值。
2. `licensed(source, target, assumptions)` 是**受限规则检查器**：同目标直接保持；同一性目标转性质目标须声明G(g)；性质目标转同一性目标须声明G(g)及至多一G对象。它要求枚举类型，不解析自然语言，不删词归一，不对任何任意推理宣称完备。

检查器只查声明规则，不认证假设真实。假设为假时，“规则被许可”不能保证结论真。测试中专门保留这个边界。它也不是完整的语义后果求解器：即使结论在某组假设下成立，程序仍可能因为没有列入相应规则而拒绝；拒绝不等于一般无效。

## 实际运行

要求 Python 3.10 或更新版本；无第三方依赖。实跑版本见[环境记录](logs/environment.txt)。在本目录执行：

```sh
python3 -m unittest -v test_model
python3 model.py
python3 -O -m unittest -v test_model
python3 -O model.py
python3 -OO -m unittest -v test_model
python3 -OO model.py
```

源码：[model.py](model.py)；测试：[test_model.py](test_model.py)。不使用会被优化模式去掉的`assert`来保护输入或判定测试。

- [普通模式测试](logs/tests-normal.txt)、[-O测试](logs/tests-O.txt)、[-OO测试](logs/tests-OO.txt)：各15项通过。
- [普通枚举](logs/survey-normal.txt)、[-O枚举](logs/survey-O.txt)、[-OO枚举](logs/survey-OO.txt)：统计相同。
- 域大小1、2、3、4的所有G子集和所有p、g解释共346个模型，计算口径为每个域大小n有`n*n*2**n`个解释。
- 真值对按`G(p), p=g`排列：00为124，01为49，10为124，11为49。四类都出现，不表示它们概率相同或现实中发生频率如此。
- 同一性与G(g)同时成立49次，没有G(p)失败；G(p)、G(g)、至多一G同时成立10次，没有p=g失败。
- 测试还遍历每个模型的16个声明假设子集、两种源目标与两种结论目标，共22144个规则检查组合。仅对“规则许可且源命题与全部假设真实”的组合检查结论；不把不满足前提的情况算作有效推导实例。

## 可手算的反模型

- 论域{0,1}，G={0,1}，p=0，g=1：G(p)和G(g)都真，p=g假。单有G(g)仍不足以反向推出同一性。
- 论域{0}，G为空，p=g=0：同一性真，G(p)假。没有G(g)桥接时，同一性本身不创造性质。
- 论域{0,1}，G={0}，p=0，g=1：至多一个G且G(p)真，但p=g假；还须确定g就是满足G的对象。

## 保证与限制

这些是有限、实跑的实现检查，**不能证明任意大小论域上的一般定理**。一般同一代换及唯一性论证见主文逐步证明；本程序只用于发现实现错误、显示小反模型并核对计数。`survey`刻意限制上界不超过6，默认只到4；没有声称覆盖无限域、完整三段论、自然语言或历史伦理学。没有训练数据、经验基线、准确率或付费服务，也没有伪装成实验论文的性能评测。

## 独立核验

[独立数学代码审查](math-code-audit.zh-CN.md)与[独立oracle](independent_audit.py)另用布尔成员向量生成模型，以逐对象量词公式判断至多唯一，不调用生产模型生成器或`holds`计算预期值。运行：

```sh
python3 independent_audit.py --tests
python3 independent_audit.py
python3 -O independent_audit.py --tests
python3 -O independent_audit.py
python3 -OO independent_audit.py --tests
python3 -OO independent_audit.py
```

各模式10项独立边界测试通过；346模型上1384次公式比较、1384次对象重命名比较一致，22144规则组合中1790个许可且全部前提真的实例结论均真。30个空G模型的“至多唯一”均真，但没有据此推出存在。日志：[普通测试](logs/independent-tests-normal.txt)、[普通枚举](logs/independent-normal.json)、[-O测试](logs/independent-tests-O.txt)、[-O枚举](logs/independent-O.json)、[-OO测试](logs/independent-tests-OO.txt)、[-OO枚举](logs/independent-OO.json)。独立文件不匹配`test*.py`，不计入生产15项测试。有限独立核验仍不是一般定理证明。
