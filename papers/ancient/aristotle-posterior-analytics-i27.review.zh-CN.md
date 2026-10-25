# I.27 独立技术审查

结论：通过，限于本文明确列出的教学重构及有限复现；不以这些测试证明亚里士多德的一般科学比较主张。

## 审查绑定

- 正文 SHA256：`fe395a98f01cf6e1a3b406f8382e1ea27eca556258e0a760e31800d254657fe1`
- `model.py` SHA256：`7df2e0f42ae219c804806ac7e861579dc7684f2271bda1c3d1ca951825eff477`
- `independent_oracle.py` SHA256：`b787f23189ea9de1edd19903540205c7600970e5a0e6d484f74321fc4d61df90`
- `independent-oracle-results.json` SHA256：`45c0000cc84008ea53ee6eeb618caf416a584c6b05ba5935fad3d7612b0f6889`
- 已执行 Notebook SHA256：`9dd1b1947b6b085393bcb290fe1ba43f2888b3e3a3d43d1fc39880c2507c083c`

## 数学与教学口径

逐项检查正文证明、算例、反例及22题答案。观察相同但干预不同的二元结构模型成立；干预替换方程，不能据此确认真实因果机制。遗忘映射的纤维恒定条件和不可恢复反证成立，非重合位置的反例有效。正向有限 Horn 闭包随规则添加单调，归纳证明正确；程序仅实现一元正规则，不冒充一般定理的完整实验验证。

重点核实：§9现为“前两标签距离”，不是全配置直径。独立程序另用 `(0,0,2)` 区分两者。64个规则集的24/40划分只检查固定种子 `{a}` 的旧语言后果投影，不是全理论保守扩张判定。两套预测反例均为明确标注的人造数据，不支持“复杂模型总更好”或古代学科总排序。原文三组比较与现代 SCM、遗忘映射、Horn、MSE 重构边界清楚；历史来源另由来源审查覆盖。

## 独立实跑

在复现目录执行：

```sh
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python verify_notebook.py
python independent_oracle.py
python -O independent_oracle.py
python -OO independent_oracle.py
```

三种模式各20项测试通过。Notebook四个代码单元在共享命名空间顺序执行，复跑后文件字节不变；这不是 Jupyter 内核执行，也未做 nbformat schema 或可视渲染验证。

独立 oracle 不是再次调用待验函数作为答案：以枚举所有满足事实与蕴涵的真值赋值、求其交集独立计算语义后果，再与待验闭包比较；以约束满足枚举求 SCM 解；用三进制解码生成位置配置。结果：

| 检查 | 实际范围 | 不符数 |
|---|---:|---:|
| 语义闭包与程序闭包 | 64规则集 × 8种子 = 512 | 0 |
| 规则包含关系的闭包单调性 | 5832 | 0 |
| SCM方程约束解 | 12 | 0 |
| 遗忘位置 | 120配置 | 0 |
| 前两标签距离 | 117配置 | 0 |

另核固定种子24个不增旧结论、40个增加旧结论；精确有理数 MSE 为 `1/2` 和 `0`。独立 oracle 三模式 JSON 输出逐字一致；无依赖可被优化关闭的 `assert` 检查。源码和机器结果分别见 [独立程序](../../reproduction/aristotle-posterior-analytics-i27/independent_oracle.py) 与 [运行结果](../../reproduction/aristotle-posterior-analytics-i27/independent-oracle-results.json)。

以上通过不替代发布后的 main 提交、文件完整性、链接与 GitHub 公式显示核验。
