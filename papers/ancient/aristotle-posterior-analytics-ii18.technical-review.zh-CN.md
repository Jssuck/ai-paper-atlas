# 《后分析篇》II.18：独立技术核验

## 结论及绑定范围

结论：**在明确的现代教学模型范围内通过**。本次审查覆盖正文的形式推导、反例、配套程序、测试、Notebook执行及结果统计；不把程序通过当作原文版本考据或现实因果认证。来源问题另见[独立来源审查](aristotle-posterior-analytics-ii18.source-audit.zh-CN.md)。

审查绑定以下SHA256字节版本：

- [正文](aristotle-posterior-analytics-ii18.zh-CN.md)：`194c21ecb4c835b2be1d863e6bae7a68ca04627e638e49b50dc5150455bb9ce1`
- [model.py](../../reproduction/aristotle-posterior-analytics-ii18/model.py)：`ed9f93d4c1c27b14f1d55f4b59262ab860634c3f4629cbd57d544c926a0be48a`
- [test_model.py](../../reproduction/aristotle-posterior-analytics-ii18/test_model.py)：`a00922ed7f12404b5d4f069d62a9afc14ffc4f998aea3673028f231141a8b63c`
- [run_all.py](../../reproduction/aristotle-posterior-analytics-ii18/run_all.py)：`fc481ab528d608dc4b8319ff54cb0562b9b9be471520d13dda4b121b416aacad`
- [tutorial.ipynb](../../reproduction/aristotle-posterior-analytics-ii18/tutorial.ipynb)：`c5aea1cdf47cbca1c51768342df9d0a670c1f39ea185d37ea6e40d96c06a4654`

后续更改上述文件应重新核对相关结论；本报告不是对未检查版本的预先保证。

## 1 数学与语义核验

1. **方向与传递。** “A属于所有B”在模型中表示B⊆A。D⊆C、C⊆B、B⊆A确实推出D⊆A。正文先建立C⊆A，再以C为中项得到端点结论，未省去其上游依赖。
2. **有效中项与最近中项。** C与B都满足D⊆M⊆A，均可用于形式证明；最近名字只由指定链的次序和当前主体决定。模型不以包含关系认证“科学原因”，并明确输出`certifies_real_explanation=False`。
3. **一般证明。** 第4.3节按链段长度归纳，对任意论域、任意有限链成立；有限枚举不是这项一般结论的证明。
4. **端点。** B→A仅有两个项时返回主体B是声明的端点约定，不新增B→B。重复项名、仅目标而无链都被拒绝；程序也不声称证明B→A不可再分。
5. **反例。** 缺少C⊆B时的反例、逆推失败、等外延异次序、分支多候选及空真均符合声明。练习7已明确A、B、C、D全部非空；在此约束下二元素论域最小，因为一元素论域的四个非空子集只能全部相同。整数例已分别说明每条相邻包含，而非只展示24的倍数属于全部后继集合。
6. **闭包陷阱。** 原始边集无D→A，传递闭包有此边。程序在原始边集下拒绝两项捷径；把闭包误当原始边输入时会返回D端点。该实验展示输入层级混淆，不是声称程序可自动识别一切伪直接前提。

## 2 独立实际运行

在不覆盖作者发布日志的隔离副本，分别实际执行：

```sh
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python model.py
python run_notebook.py
```

三种模式各24项测试通过，五条命令均退出0。之后对最终的`run_all.py`再次隔离运行，其五项子命令也全部退出0。测试使用`unittest`的断言方法，优化模式不会像裸`assert`那样取消这些检查。

Notebook有5个代码单元。本次及作者的执行方式均为Python标准库`exec`顺序执行，**不是Jupyter内核**；独立重执行后的Notebook与发布文件逐字节一致。未检验Jupyter前端、扩展或魔法命令。

作者的[三模式测试与实跑日志](../../reproduction/aristotle-posterior-analytics-ii18/README.md)与所述结果一致；[sha256清单](../../reproduction/aristotle-posterior-analytics-ii18/sha256.json)逐文件重算零错配。缓存目录不属于交付文件。

## 3 不调用作者模型的独立计数

审查另用逐元素布尔成员位枚举，不导入`model.py`，检查D属于某元素则C也属于、C则B、B则A，并另外核对D到A的结论。

| 论域元素数 | 总赋值 | 链成立 | 链成立且D非空 | 传递反例 |
|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 0 | 0 |
| 1 | 16 | 5 | 1 | 0 |
| 2 | 256 | 25 | 9 | 0 |
| 3 | 4096 | 125 | 61 | 0 |

一般计数解释为：每元素四个独立成员位共16种，满足链时只余5种单调模式，故n元素有16ⁿ个总赋值与5ⁿ个合格赋值。D为空时去掉“属于四集”的模式，得到4ⁿ个；D非空为5ⁿ−4ⁿ。n=0时非空D数为0，与枚举相符。

## 4 限制及发布后检查边界

- `nearest_choices`只汇总提供的同一问题证书，不自动核实外延；需要先调用`validate`。README已说明，不能把它单独返回的集合当作真值证书。
- 直接性、必要性、对象存在及因果适当性未被自动认证。外延相等不等于同义，分支名字不同不等于现实机制不同。
- 本报告核验最终本地字节与运行证据，不代替发布者对GitHub main、链接及公式实际显示的检查，也不提前宣称远端发布成功。
