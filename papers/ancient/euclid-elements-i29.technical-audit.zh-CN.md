# I.29 独立技术审查

审查日期：2026-10-27。结论：通过，未发现阻断性技术错误。

最终审查正文 SHA256：`4721d2db8606e5252e00619f5e2bdf120b7b71e9cce6140884a1a97f8cdb1750`。

## 数学与解释核验

- 原证 a 大于 z 时，a+y=2R 而 y+z 小于2R；第五公设所需角确为同侧内角。教学补显 a 小于 z 使用 z+w=2R，再得 a+w 小于2R，切换到 A、C 一侧；不遗漏反向分支，不循环用 I.32。
- x=a 来自对顶角，x=z 后同加 y，再调用 GE、GH 反向的邻补关系。原文与更短替换路线明确区分。
- 坐标输入的非零侧向行列式已保证 t、u、v 非零和不同支承线；同号加 det(u,v)=0 推出 v=λu、λ>0。角指标中点积符号与平方有理值合用，垂直零符号和锐钝角均处理正确。
- 手算例的 λ=3/2、三个135度及45度成立。错侧 D=(−2,0) 对应45度；远交点(1001,1)正确；退化例不冒充定理反例。
- Playfair替代路线明确具有额外唯一性前提；欧氏有理坐标模型与一般原证明、第五公设独立性没有混同。

## 独立真实运行

在复现目录执行 `python3 independent_probe.py`、`python3 -O independent_probe.py`、`python3 -OO independent_probe.py`，三条命令均 exit 0。每模式分别：

- 3120 个精确正输入，独立重算角指标与尺度；
- 6240 个非法几何输入直接调用生成器并要求 ValueError，包含反向射线及极小非平行扰动；
- 385 项证书结构、字段、类型、布尔/数值混淆、NaN、输入绑定攻击；
- 128 项非法输入类型及非规范有理数字符串，直接要求生成器拒绝；
- 六个 Notebook 代码格独立按序 compile/exec，未覆盖原 Notebook；捕获输出与已保存输出一致，仅归一化 unittest 耗时。此执行不是 Jupyter kernel。

另独立重跑 `python3 -m unittest -v test_geometry`，32 项通过；核对原运行三模式日志均32项通过及336正/8负批例结果。命令、退出码见[独立运行摘要](../../reproduction/euclid-elements-i29/independent-run-summary.json)，实际输出见[普通探针](../../reproduction/euclid-elements-i29/logs/independent-normal.log)、[-O探针](../../reproduction/euclid-elements-i29/logs/independent-O.log)、[-OO探针](../../reproduction/euclid-elements-i29/logs/independent-OO.log)和[单测](../../reproduction/euclid-elements-i29/logs/independent-unittest.log)。探针源码为[独立探针](../../reproduction/euclid-elements-i29/independent_probe.py)。

## 边界

这不是形式化证明助理审计，也不认证全部实数输入、古代作图操作或外部测量真实性。有限测试不证明一般定理和公理独立性。未执行远端写入；公开链接和GitHub公式实际显示由发布流程单独核验。最终发布者应将新探针和日志纳入内容哈希清单。
