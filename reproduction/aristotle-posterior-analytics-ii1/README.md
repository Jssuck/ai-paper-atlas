# II.1 最小教学复现：四问与证据账本

对应《后分析篇》II.1的四种研究问题：[原文英译入口](https://classics.mit.edu/Aristotle/posterior.2.ii.html)第一章。源码是原创现代教学重构，**不是亚里士多德的算法、真实天文学实验、科学知识认证或完整复现**；不把第二章的中项统一论证算作第一章成果。

## 状态、接口与限制

`InquiryKey(kind, subject, context, attribute='')`固定问题类型、对象、事件/范围。`kind='attribute'`必须有属性，`kind='existence'`不得夹带属性。例如太阳在某次事件是否被食，与太阳是否存在，是不同问题。`context`是使用者明定的标识，不会自动理解时间或语义相等。

`EvidenceState.status`为`unknown/yes/no`。未知是**账本未有当前判定**，不是否定；肯定/否定也是调用者提供的判定，不等于程序已验证其为科学知识。`record(key, Status.YES/NO, evidence)`要求非空证据标签；标签不被机器认证，不能冒充真实观测。新记录替换同键旧记录，本程序不保留审计历史、不合并冲突证据；`withdraw`撤回当前判定。它是有意简化、非生产科研证据库。

`next_question`规则：

| 类型 | unknown | yes | no |
|---|---|---|---|
| 属性联结 | fact（是否如此） | why（为何如此） | closed_negative |
| 不附带属性的存在 | exists（是否存在） | what（其是什么） | closed_negative |

肯定后的`why/what`只是进入进一步研究，不是得到答案；`certified_answer`恒为`None`，明确禁止这个教学程序冒充原因或本质认证器。`propose`保存任意非空候选字符串且不改变判定。多个候选不表示多种已证明的原因；此功能让学生检查“提议≠回答”。程序甚至在未知/否定时也容许提出假想描述，所以不把本章读成禁止虚构对象研究。

`closed_negative`仅关闭这一个**肯定事实/实存的后续路线**；不表示不能问“为什么没有”、不能重新检验或不能研究虚构对象。否定分支、撤回与上下文键是现代教学设计，不是声称原文列出计算状态机。

## 一般不变式与反例

对任意键及任意有限动作序列：

1. 初态无记录，所以返回unknown对应的初问。
2. `record`只把指定键替换为yes或no，`withdraw`只删除该键；因此其他键不受影响。逐步归纳得到任意长度的键隔离。
3. 路由只看该键的类型和当前三态；两种类型、三个状态已穷尽。因此只有显式yes才能走其正向解释/本质路线；输入一次yes并不会使下一时刻、另一对象或另一属性自动yes。
4. `propose`不修改状态，所有公开操作都没有建立已认证答案的路径。因此录入事实和罗列候选均不能自动产生已认证解释。

这些性质来自**所选程序定义**，不证明古代四分法穷尽所有人类问题，也不证明调用者所填证据正确。程序故意不实现由属性肯定推出主体存在的语义推理；这是类型隔离政策，不是在哲学上否定这种蕴涵。

反例：账本空时`unknown`与记录NO时的路线不同，故不能把未查到当作没有；同一次太阳食的肯定不能回答另一事件；同一个肯定事实可以保留A、B两个未认证候选；人马描述可保存但实存问题仍未知。最后两例说明“事实/词义材料不足以自动输出解释/实存”，不声称已构造出真实科学的两个因果模型。

## 真实运行与Notebook

Python 3，仅标准库，无新增依赖。进入本目录运行：

```sh
python run_all.py
```

它依次实际执行：

```sh
python model.py
python -m unittest -v test_model
python -O -m unittest -v test_model
python -OO -m unittest -v test_model
python run_notebook.py
```

[源码](model.py) · [测试](test_model.py) · [Notebook](tutorial.ipynb) · [顺序执行器](run_notebook.py) · [批运行器](run_all.py) · [环境](environment.json) · [SHA256](sha256.json)

[演示](logs/demo.log) · [正常测试](logs/tests.log) · [-O测试](logs/tests-optimized.log) · [-OO测试](logs/tests-double-optimized.log) · [Notebook执行](logs/notebook.log)

真实穷举两种问题类型，每种长度0至4、每步取yes/no/withdraw的全部动作序列，共2×(1+3+9+27+81)=242条、2×(3+18+81+324)=852次转移，核查路由、上下文隔离与不制造解释。15项unittest在三种优化模式各实际执行，使用unittest断言方法而非可被优化删除的`assert`。有限穷举不能替代上面的任意长度归纳，也不能验证古代认识论。

已读取已装Notebook技能。当前没有nbformat/nbclient/ipykernel，技能指定helper路径不存在，附属结构资源读取失败；未安装新软件，沿用已有Notebook结构改写四个纯Python代码单元。以CPython标准库`exec`按序执行，保存输出，**不是Jupyter内核执行**，不支持magic/widgets/display协议。Notebook里的天文与人马证据标签都为显式假设，不是新观测。

`sha256.json`排除自身和`__pycache__`；重新运行将更新真实时间、测试耗时和摘要。不要把运行耗时当作古代认知速度。
