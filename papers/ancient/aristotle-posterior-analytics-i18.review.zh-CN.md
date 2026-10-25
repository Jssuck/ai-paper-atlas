# 《后分析篇》I.18：独立数学与代码审查

## 结论与审查范围

**通过（2026-10-25）。** 审查者与正文、复现作者分开；独立阅读正文、复现说明、源码、测试、Notebook和保存日志，并实际重跑。审查针对下列散列的文件；任何内容或公式格式修改后须重新核对，结论不自动延伸到后续版本。来源解释由另附来源审查负责；本审查不是对全部古代认识论的认证。

## 数学核验

1. 观察纤维常量当且仅当目标可由观察恢复的双向证明成立。解码器定义于实际观察像；空域由空函数处理，不额外假设观察满射，也不把存在性等同于有效学习或高效计算。一般证明不依赖有限枚举。
2. 四情形反例含相同观察而不同目标，足以排除全域精确的确定解码器。正文异或通道手算可由第一位与异或值恢复第二位；公开程序使用直接观察目标位的较简单替代例。正文已经明确两者不是同一次实跑。
3. 背景限制与新增通道的逻辑角色分开；抽象是否保留目标是相对任务的条件，不支持人的感官能力结论。
4. 有限样本不覆盖时翻转一个未观察位置，得到样本一致而全域不同的目标。其范围明确限定为无额外约束的全部二值目标；全覆盖只能认证给定有限域的逐点值，不认证本质、原因或无限普遍规律。
5. 必要条件依赖链的逆否推理正确，正文未将依赖条件本身冒称为无条件现代定理；也未把感觉可用当作科学知识成功的充分条件。

## 独立执行与交叉检查

- 在复现目录分别运行 `python -m unittest -v test_observability`、`python -O -m unittest -v test_observability`、`python -OO -m unittest -v test_observability`：各8项通过、退出码0。未覆盖作者保存的日志。
- 独立运行 `python observability.py`，结果与公开 `results.json` 逐字节一致。
- 另写独立枚举器，搜索全部二值总解码器，不复用作者纤维算法作为判据。0至4情形的行计数依次为1/1、4/4、16/12、64/28、256/60（总映射对/可恢复），合计341/105；额外扩展5情形的1024映射对也与实现一致，124可恢复。
- 独立完成函数枚举核对256组目标/样本组合；240组不唯一，唯一的16组均为全覆盖。每组候选数为2的未观察位置数次方。
- 空向量返回空字典而非失败；失败仅用 `None`。非法比特类型、长度不符、重复或越界样本下标有显式检查。测试用 `unittest` 方法，未依赖优化模式会删除的裸 `assert`。
- 私有命名空间顺序执行Notebook全部4个普通Python代码单元，输出与保存输出一致。未启动Jupyter内核，未声称交互界面验证；附件明确相同限制。

本实验仅标准库、合成有限数据。日志运行时间的微小差别正常，不将新日志覆盖作者真实记录。没有发现需要修正的技术错误。仍不声称完成证明助理认证、真实传感器实验或人体认识过程复原。

## 最终文件SHA-256

| 文件 | SHA-256 |
|---|---|
| `papers/ancient/aristotle-posterior-analytics-i18.zh-CN.md` | `1b6c0e4be20d55bfda1dee32988365263828d3566f47a5f16c1d1e05ed1f00e6` |
| `reproduction/aristotle-posterior-analytics-i18/README.md` | `a4004cbc6731702dbcd0179d0c57508ad48d381dacf9c51e543d17190156f2c7` |
| `reproduction/aristotle-posterior-analytics-i18/logs/environment.json` | `a9bdae24fc409d3d3c5d6930ff7709f5e0c5556b2068beed02afa63759393c35` |
| `reproduction/aristotle-posterior-analytics-i18/logs/notebook.log` | `facd128d87190c77a5558618056f493af0321df5b3115b69eba043301adfeb4d` |
| `reproduction/aristotle-posterior-analytics-i18/logs/tests-O.log` | `b4f0c1093f0ca79b32c175bcd269cdb7f6d0cb6503cbec861fd683324389aa81` |
| `reproduction/aristotle-posterior-analytics-i18/logs/tests-OO.log` | `844551b1c43c6128a81f2494c5cd5815dd8b6aebfeebb530a7ef6fbcad8ad711` |
| `reproduction/aristotle-posterior-analytics-i18/logs/tests-normal.log` | `b4f0c1093f0ca79b32c175bcd269cdb7f6d0cb6503cbec861fd683324389aa81` |
| `reproduction/aristotle-posterior-analytics-i18/observability.py` | `e7846bdb2577c69b95f88a159aa3ce4ef22c065c2a558415573099fad7d0da05` |
| `reproduction/aristotle-posterior-analytics-i18/results.json` | `fb46028697cfcaaf88333ae39dc2fc48c94ba8d529339a2359ff310c87b7ac9a` |
| `reproduction/aristotle-posterior-analytics-i18/run_notebook.py` | `f95f2da848c48d401f4da998e92f8b3f8e500b8c217edce45c36af420967cdc4` |
| `reproduction/aristotle-posterior-analytics-i18/test_observability.py` | `dc9debe78a8c1e6e7959adde6ffef93e6b4b5017352f9acff748ab07fa9c51fe` |
| `reproduction/aristotle-posterior-analytics-i18/tutorial.ipynb` | `61c51b1c31833107c17d58d4b01f7448c4362ffe5f29c5564f1b644dc9db9855` |
