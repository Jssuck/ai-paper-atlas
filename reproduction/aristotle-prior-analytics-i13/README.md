# I.13：逐对象偶然性与整句偶然性的标准库教学模型

本附件是原创现代教学重构，不是古代完整模态逻辑实现。固定非空有限论域与非空世界集合，所有列出的世界均纳入模态量化；没有另建可达关系、时间因果或自然规律。实际世界固定为第0项。A、B的外延可随世界变化，主项集合S在一次句子求值中固定。

## 定义与实现

- `necessary(v)`：非空真值列全真；`possible(v)`：至少一个真；`contingent(v)`：至少一个真且至少一个假。
- `individual(x)`：对象x在至少一个世界属于A，在至少一个世界不属于A。
- `subject('actual')`：B在世界0的外延；`subject('possible')`：B全部世界外延的并集。
- `all_each_contingent(S)`：S内每个对象分别具有A及非A的可能性；空S按全称真处理。
- `some_each_contingent(S)`：至少一个这样的对象；空S为假。
- `sentence(S, form)`：每个世界对固定S分别计算all、none、some、notall，之后才可对整条真值列计算偶然性。
- `complement()`补的是各世界的A外延，保持B不变；不是交换A/B。
- `probability(v, weights)`接受非负有理权重，输出精确分数，只演示额外权重与模态支持的差别，不是原章概率论。

输入边界明确验证：n必须为正整数且不能是bool；世界序列是非空tuple；各外延为frozenset且对象是合法整数；A/B世界数相同。空世界、非法对象、不支持的形式、非布尔真值、负权重及零总权重都报ValueError。允许空谓词外延与空主项S，以显式暴露存在条件。

## 运行

Python标准库，无第三方依赖。在本目录执行：

```text
python -m unittest -v test_model
python -O -m unittest -v test_model
python -OO -m unittest -v test_model
python demo.py
python -O demo.py
python -OO demo.py
```

[环境](environment.json)、[结果](results.json)、[逐步走查](WALKTHROUGH.md)。

真实日志：
- [普通测试](logs/tests-normal.txt)、[-O测试](logs/tests-O.txt)、[-OO测试](logs/tests-OO.txt)
- [普通示例](logs/demo-normal.txt)、[-O示例](logs/demo-O.txt)、[-OO示例](logs/demo-OO.txt)

三个模式各通过22个unittest方法；同一穷举测试每模式枚举2对象×2世界的256种(A,B)模型，并遍历4个固定S，共1024模型/主项对。不要把22个方法计为22个模型。补集与换项另有直接外延断言（含空集、全域、部分集合、保持另一谓词与原模型、双次操作复原），不只检查性质不变性。所有演示日志逐字相同。all_each为真576次（包含空S），some_each为真448次；实际B主项的all_each为真144模型，可能B主项为真100模型。此计数属于这个非常小且允许空类的模型空间，不是自然发生频率或历史文献分类。

## 可说明什么，不能说明什么

交替对象实例显示“每个对象都可A也可非A”不保证存在同一个世界所有对象都A，亦不保证共同全非A。补A时逐对象偶然性不变；其一般理由是交换“出现”和“不出现”两个存在条件，而非有限计数。可能B集合包含实际B，故其逐对象全称要求更强。原章的通常/自然倾向没有被实现为频率阈值；权重示例只证明给定语义下可能性不决定数值概率。

小测试不能证明任意论域的一般定理，不能验证古代作者的全部体系、自然现象或人类推理，也不构成现代AI效果实验。未使用Notebook，不声称Jupyter执行。独立代码审查另由审查者给出，不把本作者测试冒称独立复现。


[独立代码审查](CODE_REVIEW.md)记录独立位掩码核对、三模式重跑及定向故障注入；修正前后证据均保留，检出范围不等于软件无缺陷证明。
