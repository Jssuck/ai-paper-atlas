# 《后分析篇》II.15：解释同一性的有限教学模型

这不是亚里士多德物理学的复现，也不是一般因果定理的证明。它仅把 98a24–34 中辨别问题关联的提示重构成可检查的声明结构。月亏、天气、尼罗河的关系只作为原文历史示例的假设图，不作为现代科学事实。

## 运行

Python 3.10+，仅标准库；本轮实际版本见 [environment.json](environment.json)。进入本目录：

```sh
python run_all.py
```

该命令执行并保存真实退出码和输出：

- `python -m unittest -v` → [tests.log](logs/tests.log)
- `python -O -m unittest -v` → [tests-optimized.log](logs/tests-optimized.log)
- `python -OO -m unittest -v` → [tests-double-optimized.log](logs/tests-double-optimized.log)
- `python model.py` → [demo.log](logs/demo.log)
- `python run_notebook.py` → [notebook-exec.log](logs/notebook-exec.log)

[Notebook](tutorial.ipynb) 有稳定 cell IDs；本轮保存输出来自逐格 Python 标准库 `exec`，**没有通过 Jupyter 内核执行**。执行器不支持 IPython magic，不验证 Jupyter 前端功能。已阅读安装的 Notebook 技能；本地找不到 scaffold helper，故手工构造 nbformat 4.5，不安装软件。`run_all.py` 重新生成日志、环境和内容 SHA256，因此再次运行会改变时间戳和测试耗时；`sha256.json` 不自哈希，不纳入缓存目录。

## 数据、判定与失败条件

`Middle` 使用 canonical key、genus、species、适用域与所需条件；label 仅展示。`Problem.validate` 拒绝越域和缺条件。相同 key 的声明必须完全一致，拒绝悄悄改变同一标识的含义。

`classify` 返回最具体操作标签：`exact` 表示相同中项声明；否则同 genus 返回 `generic`，否则 `unrelated`。这不是原文提出的三类互斥划分：**`shares_genus` 是包容性关系，exact 同时属于同属**；此处 `generic` 输出只是“同属但身份不同”的程序分支。词名相同而 canonical identity 与 genus 不同，不合并。历史 echo、镜像、虹使用同一历史 genus、不同 species，并不声称现代机制相同。`antiperistasis` 未并入该 genus。

`Chain` 是有限有向无环声明图。边为“原因→被解释项”，level 是人为指定的解释次序而不是实测时间。构造时拒绝未知节点、重复标识、循环和违背该次序的边；`explains` 只检查有向可达性，不给逆向推理或自身解释。若 level 或因果边本身不真实，代码仍不能发现其经验错误。

## 真实运行与能说明什么

20 个 unittest 方法通过，普通、`-O` 和 `-OO` 各一次；三对历史现象在一个测试中用 subTest 核查。demo 给出：教学同中项 `exact`；该 pair 的 inclusive genus 为 True；三对历史现象为 `generic`；同名神经“反射”为 `unrelated`；假设图正向可达 True、逆向 False、自身 False。

测试检查输入契约、反例和实现行为；不能证明任意解释系统正确、古代前提真实、同属可迁移或所有因果关系都是 DAG。复杂度：分类为有限集合包含比较；当前 DFS 遍历邻边时扫描边集，最坏约 O(VE)，适合这个三节点低成本示例，不是大型图优化器。

## 练习与答案

1. 两个问题同名就同中项吗？不；canonical identity、声明和适用条件才决定本模型的 exact。
2. exact 是否排除同属？不；`shares_genus` 同时为 True。
3. 为何月亏→尼罗河可达不证明真实因果？因为边和层级由我们声明，既无水文数据，也无因果识别或反事实验证。
4. 删除天气→尼罗河边会怎样？月亏至尼罗河不再可达；这仅显示论证链缺项，不证明现实中没有关联。
