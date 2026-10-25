# 《后分析篇》I.28 独立技术审查

核验日期：2026-10-25。结论：**在下述有限规格与边界内通过**。审查为与撰稿分离的AI技术复核，不是人类专家、证明助理或古代科学划界完备性认证。来源解释另见[来源审查](aristotle-posterior-analytics-i28.source-audit.zh-CN.md)。

## 绑定对象

- [最终正文](aristotle-posterior-analytics-i28.zh-CN.md) SHA256：`ff91b7f576bc97a6fc2fd327d29f24c71d3b9a110c037bf4fbade770f7b7d3df`。
- [model.py](../../reproduction/aristotle-posterior-analytics-i28/model.py) SHA256：`3054f66e0fd7720ed6aa7917aacf03d6b1c590370eb0557e070878c82dcfc926`。
- [独立oracle源码](../../reproduction/aristotle-posterior-analytics-i28/independent_oracle.py) SHA256：`2852abcd9d63550f16eda9954436316fb73c72cb52fab4cac09b10cc4e32d4fa`。
- [独立实跑结果](../../reproduction/aristotle-posterior-analytics-i28/independent-results.json) SHA256：`2332dd07226a82c5762a12ad0bf9f53cd6409b884e4eb9e77a52a5ff5ffcfc0e`。

正文若改动，本绑定不自动延伸到新版本。

## 证明、算例和18题

逐项检查正文第4–7节及18个练习答案，未发现需要修改的技术错误。

1. 终止界以有限全集包含全部种子和规则原子为前提。同步轮次公式与程序同一轮内即可使用新事实的异步扫描次序不同，但都保持新增项有根据，且最终达到同一个最小固定点；不将运行轮数与公式轮数混同。
2. 可靠性归纳可将首次导出记录展开为证明树。它保证满足前提及规则的赋值保真，不保证现实前提真。
3. 固定点的特征赋值确为满足所有正Horn规则的模型；遗漏目标由此不被语义蕴涵。它不意味着目标在每个模型里为假。规则前件非空，事实另行声明；不借空规则暗中自举。
4. 同标签不新增规则；合取前件缺一不可；无种子的正循环不产生事实。单向派生不对称。共同根的非空交叠不是传递关系，故不能作为未经论证的身份等价关系。
5. 包含最小支持不同于最小基数，也不同于唯一真实原因。附加反例有规则p→r和{q,s}→r，其包含最小支持同时包括{p}与{q,s}。
6. 第1、3、17题的版本事实交由来源审查；其技术用法没有把章界、译者补语或后世脚注混成算法证明。其他题的结论与所声明语法一致。

## 独立语义oracle

预期闭包**不调用待测derive或normalize**：枚举三原子的全部8个布尔赋值，筛选满足种子和每条蕴涵的赋值，再求其中恒真的原子交集。所有正规则都有全真模型，故没有空模型集合导致的假阳性。

对9条非空前件且结论不在前件中的候选规则，枚举全部512规则子集：

| 核验 | 实际次数 | 失败 |
|---|---:|---:|
| 语义模型交集与闭包一致 | 4096 | 0 |
| 所有声明根子集上的包含最小支持 | 12288 | 0 |
| 正序、逆序、重复及外来规则证书与独立重放判据一致 | 49152 | 0 |
| 缺失/N/G三种标注及无桥、全桥、部分桥的规则分区 | 41472 | 0 |
| 额外边界检查 | 20 | 0 |

证书另逐目标检查生成证书的可达结论与语义后果一致。类型分区的预期直接按每条规则的所有原子是否有标注、标注是否相同、跨域规则是否精确列为桥计算；桥不能补缺失标注。边界检查包括含自身结论的规则、拒绝空前件、不蕴涵但真假皆可能、共同根非传递以及不等基数的最小支持。

重跑命令（在复现目录）：

```sh
python -m unittest -v test_model
python -O -m unittest -v test_model
python -OO -m unittest -v test_model
python verify_notebook.py
python independent_oracle.py > independent-results.json
python -O independent_oracle.py
python -OO independent_oracle.py
```

审查者独立重跑22项测试在三种优化模式均通过；oracle三模式输出字节一致，失败数均为0。Notebook四代码单元在新Python进程按顺序执行，前后SHA256均为`9a4440230a756d7f57183981bcb2d518fa21f9232cbd9bec57a43c305ab51fa8`；没有声称Jupyter内核、完整nbformat模式或页面渲染经过本审查验证。原始测试日志及环境见[复现说明](../../reproduction/aristotle-posterior-analytics-i28/README.md)。

## 保证边界

- 该oracle穷举有限候选语法，额外边界测试不等于穷举任意大小输入；一般结论由正文证明而非测试次数支持。
- 字符串种子、有限输入和正确数据结构是调用者约定。程序显式验证规则原子的字符串类型及非空前件，不是全面的输入模式验证器；类型检查针对规则局部签名，不校验全部种子的现实语义。
- 输入标签、桥接许可和起点身份需要外部证据。本程序不从文本发现自然属，不判定真实因果性，也不声称完成古代科学分类。
- 公开材料为原创解析与教学代码，审查不包含私人对话、账户信息或原典扫描全文。
