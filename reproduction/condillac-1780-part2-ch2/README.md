# 孔狄亚克《逻辑学》II.II：可运行教学重构

实际底本：1798年《Œuvres de Condillac》卷XXII，*La Logique* 第二部第二章，印页109–117。目录/路径沿用作品一版的已核书目年1780，不把1798底本误称为已读1780版。只处理该章，第三章不在范围内。[正文精读](../../papers/1780/condillac-logic-part2-ch2.zh-CN.md)另述历史解释与来源。

本附件是新写的有限数学教学程序，不是发现或复原一段历史算法，不含心理学验证。它分别展示：角色绑定能否保留、语境如何允许多种但非任意顺序、前缀如何缩小候选，以及类比何时需要额外假设。

## 先看什么

1. [MODEL.zh-CN.md](MODEL.zh-CN.md)：全部定义、一般证明、充分条件与反例边界
2. [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：可手算的逐步例子
3. [logs/results.json](logs/results.json)：实际demo结果
4. `model.py`、`demo.py`：核心实现与固定示例
5. `test_model.py`、`mutation_check.py`、`run_all.py`：作者验证代码

所有内容为Python标准库；无下载、无安装、无模型API、无网络调用、无notebook。建议CPython 3.10及以上；**实际验证仅在日志记录的CPython 3.12.14 / Linux环境**，不声称测试过其他版本。

## 精确运行命令

从本目录执行：

```sh
python -B demo.py
python -B -m unittest -v
python -O -B -m unittest -v
python -OO -B -m unittest -v
python -B mutation_check.py --mode normal
python -O -B mutation_check.py --mode O
python -OO -B mutation_check.py --mode OO
python -B run_all.py
```

最后一条会重新运行上述全部验证及demo，并覆盖本目录三个作者日志文件。`-B`避免新增字节码缓存；优化模式不会删除unittest检查或显式抛错。校验未使用裸assert，`run_all.py`也会做AST检查。不要用 `python -m ...` 从其他无关目录启动，否则本地模块路径可能不同。

## 已运行结果与范围

正常、`-O`、`-OO`均通过28个unittest测试方法。方法内含明确有限枚举：

- 1至3个特征、每域二值的全部29个DAG
- 402次完整合法编码及1588次合法前缀检查
- 两个二值特征、词码池{x,y,z}的全部81张字典；每张检查长度0至3的40个前缀，共3240次，含碰撞和超长序列
- 不等长值域、两种合法顺序、真实消息保留、非严格缩小、未知词码、非法顺序、框架切分、输入快照和类比不确定性

每优化模式另执行8个人工行为突变、8个对应的原版哨兵基线、5个故障分类控制。8个突变均被指定哨兵的断言失败检出；基线均通过；语法失败、导入失败、提前退出、真实超时与测试运行异常均归入各自类别。每个突变只执行一个针对性哨兵，**不是每个突变执行完整28测试**。人工选择的突变也不构成覆盖率或“任意bug都能抓到”的保证。

- [verification.log](logs/verification.log)：三个模式所有命令、stdout/stderr、退出码；突变记录含每次子进程输出。只将解释器路径和每次临时目录前缀替换为`${PYTHON_EXECUTABLE}`、`${MUTATION_DIR}`，不删除输出行；实际命令使用当前`sys.executable`
- [verification-summary.json](logs/verification-summary.json)：解释器、平台、执行时间、源码SHA-256、各阶段及分类摘要
- [results.json](logs/results.json)：demo输出，单独保留以便阅读

这些都是作者验证，独立审计若另有材料须单独标明，不能将这里的对照函数称为外部独立证明。有限穷举检查实现，一般结论依赖MODEL的证明。

## 实际示例摘要

消息(A,B,help)在agent、patient先于act的语境下有两种合法表达，均完整恢复。沿其中一种表达，候选数8→4→2→1。交换agent和patient的值，无标签多重集不变而带标签集合改变。让help与avoid共用词码后，三项全部收到仍有两个候选；直接拼(a,bc)与(ab,c)得到相同abc，JSON数组则不同。给定两条已知符号对应，有限假设空间仍可对第三符号预测2或4。

这些例子不证明“同时”必然损失信息，不证明所有非单射字典处处含混，也不证明字符正确传完便有人类意义上的理解。共同字典、封闭模式、完整覆盖与正确观察都是模型条件。
