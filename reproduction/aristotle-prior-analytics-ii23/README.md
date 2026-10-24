# II.23 的最小教学复现：穷尽覆盖到底增加了什么？

[原创中文深读](../../papers/ancient/aristotle-prior-analytics-ii23.zh-CN.md) · [来源与章界](../../papers/ancient/aristotle-prior-analytics-ii23.sources.zh-CN.md)

这是原创集合语义教学代码，不是古代生物学实验、亚里士多德的原算法、完整历史复现或现代统计学习基准。实际依据是《前分析篇》II.23 关于经全部个别项建立全称关系的论述，以及 Jenkinson 注99对第三格到第一格的解释。亲读 Jenkinson [Book II](https://en.wikisource.org/wiki/The_Works_of_Aristotle/Prior_Analytics/Book_II) 第23节及注97–99，并视觉阅读 Owen 1853 印230–231正文、边注、脚注。动物名称不作为输入数据，不验证关于寿命、胆汁的生物学真伪。

## 1. 定义、一般证明和实验边界

固定现代论域 $`U`$ ，令 $`A,B,C\subseteq U`$ 。$`A`$ 为待转移性质，$`B`$ 为目标类，$`C`$ 为已列举对象的并集。位掩码的第 $`i`$ 位表示对象 $`i`$ 是否属于集合；`subset(left,right)` 判断左集合包含于右集合。这里允许空项，也单列空论域作为软件边界测试，**不是宣称原典使用空论域语义**。

三类前提必须分开：

1. **观察**：$`C\subseteq A`$ 。所有列举对象均有待转移性质。
2. **分类**：$`C\subseteq B`$ 。列举对象属于目标类。
3. **覆盖**：$`B\subseteq C`$ 。目标类没有未列举的成员。

分类和覆盖合起来才给 $`B=C`$ 。任取 $`x\in B`$ ，覆盖给 $`x\in C`$ ，观察给 $`x\in A`$ ，因此 $`B\subseteq A`$ 。这个元素证明适用于任意集合，不依赖枚举程序。分类对原典列举结构有作用，却不是上述最小传递定理所必需的前提：有些列举对象在 $`B`$ 以外，只要覆盖与观察仍真，传递依旧有效。

更精确的必要充分命题为：固定 $`B,C`$ ，以下两件事等价：

$$
B\subseteq C\quad\Longleftrightarrow\quad
\forall A\subseteq U\;(C\subseteq A\Rightarrow B\subseteq A).
$$

左到右已证；右到左取 $`A=C`$ 即得。若要保持分类前提，可把等价式限制在 $`C\subseteq B`$ 的配对上。**对所有可能性质可靠转移**不能误写成**每次结论偶然为真都必有覆盖**；后者错误，见反例文件中的 `incomplete_but_accidentally_true`。

若只有观察和分类，但 $`C\ne\varnothing`$ ，任取其见证可推出 $`A\cap B\ne\varnothing`$ ，不能推出全称。如果 $`C=\varnothing`$ ，连这个存在结论也不保证。在观察为真时，全部结论反例准确满足：

$$
B\setminus A=(B\setminus C)\setminus A.
$$

左边对象不可能在 $`C`$ 中，否则观察迫使它在 $`A`$ 中；反向直接由包含关系得。这说明未覆盖位置是可能失败的位置，不表示每个未覆盖位置必然失败。

## 2. 实际运行

依赖仅 Python 3 标准库，没有安装第三方包、随机抽样、外部数据或网络调用。

```sh
cd reproduction/aristotle-prior-analytics-ii23
sh run.sh
```

`run.sh` 真正分别执行 `python3`、`python3 -O`、`python3 -OO` 的程序及单元测试，保存三份 JSON、三份测试日志、环境版本/运行UTC和JSON比较日志。JSON不含时间等非确定字段，三份逐对象相等。实现检查用显式抛异常，单元测试用 `unittest` 方法，不靠会被优化删除的 `assert`。

- [实现](induction.py)；[11项单元测试](test_induction.py)；[运行命令](run.sh)
- [真实环境](results/environment.txt)；[三模式比较日志](results/comparison.log)
- [普通JSON](results/normal.json)；[普通测试](results/normal.tests.log)
- [-O JSON](results/optimized.json)；[-O测试](results/optimized.tests.log)
- [-OO JSON](results/double_optimized.json)；[-OO测试](results/double_optimized.tests.log)

## 3. 真实结果与计数口径

逐一枚举 $`n=0,1,2,3,4`$ 的所有 $`(A,B,C)`$ ，每个 $`n`$ 有 $`8^n`$ 个世界，共 **4681**。空集也计入，计数并非古代存在预设下的计数。

| 检查 | 满足其前提的世界 | 违反结论 |
| --- | ---: | ---: |
| 观察、分类、覆盖 ⇒ 全称结论 | 121 | 0 |
| 观察、覆盖 ⇒ 全称结论 | 341 | 0 |
| 非空列举、观察、分类 ⇒ 存在结论 | 440 | 0 |
| 普通演绎：目标类有性质、列举属于目标类 ⇒ 列举有性质 | 341 | 0 |
| 观察 ⇒ 上述失败定位等式 | 1555 | 0 |

仅观察和分类的世界共 **781**，其中 **440** 的全称结论为假。此为穷举集合模型比例，**不是统计失误率或经验频率**。另对 **341** 个 $`(B,C)`$ 配对逐个遍历全部 $`A`$ ，覆盖与全性质可靠转移等价，0违例；其中121对满足分类。这一双层量化与上表不同，不能把341对说成341次实验样本。

三模式各 **11项单元测试通过**。JSON另含六个具名模型，直观展示缺覆盖、缺观察、空样本、最小传递不需分类、缺覆盖却偶真、完整玩具枚举。它们不是历史实例或实际动物数据。

## 4. 能证明与不能证明的事

程序能揭露项位写反、漏覆盖、以空样本取得存在结论等实现错误。零反例只说明上述有限边界内未发现错误；一般正确性来自第1节独立元素证明。程序不能判定希腊文校读、归纳认识论、类的实际穷尽可得性、现代统计泛化或历史影响。`max_n` 仅是有限枚举上限；接口拒绝布尔值、负值、非整数和大于6，避免意外巨量计算，默认上限为4。

实际系统若只得到有限观察，不能自称已经取得覆盖；需要另有封闭数据库、完整分类表或领域论证。程序接受一个位掩码并不构成这种外部证据。本复现没有训练模型、没有准确率、没有为样本外对象预测，也没有把小实验充作一般定理证明。

## 5. 独立核验入口

[独立oracle、命令及三模式比较](audit/README.md)使用不同的集合表示，不导入生产函数；[技术审查](../../papers/ancient/aristotle-prior-analytics-ii23.technical-review.zh-CN.md)绑定最终源码和正文摘要。独立核验不扩大上文的有限实验边界。
