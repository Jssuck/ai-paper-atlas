# Condillac《逻辑学》I.IV：需求驱动分类的有限教学模型

本附件配合《逻辑学》第一部第四章完整章，原书印页32–48，所用1798年《全集》影印PDF第40–56页。目录中的1780是有书目支持的作品版本年；本次实读1798年影印版，未核1780年章内影像或最早版次。

**这里的Python、有限集合、任务输出、等价类、证明和测试，全部是现代教学重构。Condillac没有在本章提出这些算法；本附件也不是儿童概念发展或植物分类的经验复现。**

## 从哪里读

- [MODEL.zh-CN.md：定义、一般证明、假设与失效边界](MODEL.zh-CN.md)
- [WALKTHROUGH.zh-CN.md：逐步推演、输入与输出解释](WALKTHROUGH.zh-CN.md)
- [model.py：一般模型实现](model.py)
- [fixtures.py：全部8个虚构对象与人为指定的属性、任务输出](fixtures.py)
- [test_model.py：边界检查与小域穷举测试](test_model.py)
- [results/results.json：完整确定性结果](results/results.json)
- [results/summary.txt：简短实跑摘要](results/summary.txt)
- [results/tests.log：实际单元测试日志](results/tests.log)
- [results/execution.log：实际执行命令、输出和退出码](results/execution.log)
- [results/environment.json：运行环境与耗时](results/environment.json)
- [results/determinism.json：不同哈希种子下的逐字节复核](results/determinism.json)
- [results/manifest.sha256：附件文件校验值](results/manifest.sha256)

主文献：[Internet Archive影印《Œuvres de Condillac》第22卷](https://archive.org/details/b28772581_0022)。章节论证与页码的逐项对应见[MODEL.zh-CN.md的来源边界](MODEL.zh-CN.md#来源边界)。

## 一条命令复跑

要求Python 3.10或更高版本；只有标准库，没有安装步骤、模型下载、联网、API密钥或付费服务。进入本目录运行：

```sh
python3 run_all.py
```

这会重新生成本目录的results文件。命令依次检查Python语法、运行全部单元测试、生成教学实验结果，再用两个独立进程及不同哈希种子复算，核对results.json与summary.txt的字节完全相同。日志保留真实输出；测试失败时命令非零退出，不会继续报告成功。环境记录与耗时自然可变，**不属于确定性结果的字节一致性承诺**。

只运行实验或测试：

```sh
python3 run_experiments.py
python3 -m unittest -v
```

## 应看到什么

同一组8个虚构对象，在不同需要下产生1、2、5、7、8、5类：

1. 暂不要求区分任何任务输出：1类。
2. 只区分“采收/略过”：2类。
3. 区分苹果、梨、樱桃、桃及无果的分拣输出：5类。
4. 同时需要分拣和“供遮阴/略过”：7类。
5. 每个个体都单独命名：8类。仍然充分，但对第4步的需要多作一层没有必要的区分。
6. 撤回遮阴需要：最粗充分分区可恢复5类；模型不要求保留过去的所有细分。

只有“都是绿色”这条观测时，出现15对“观测相同、采收输出不同”的对象。增加人为给定的果类观测后，这个有限数据集上的冲突消失。它不是“算法从颜色学会识果”的结果。

另有边界命名与证据边界例子：树/灌木的中间带采用“植物”；未知观测不转换成假；只报告一个已经核对的属性可以准确，却不覆盖全部有限参照字段。

## 明确不推出的结论

- 类别数较少，不自动等于人的认知成本较低；本模型不测量记忆负担，不证明过细分类导致心理混乱。
- 已知任务输出下的充分分类，不等于从缺失、含噪或新样本中发现正确类别。
- 最粗充分分区的唯一性只在明确的有限论域、确定任务、零误差要求和“最粗”标准下成立；不是所有分类问题都有唯一答案。
- 使用上位词只适合当前任务确实不需要细分的情形；换任务后应重新检查。
- 这些现代形式化类比不证明Condillac对任何现代AI方法存在直接影响。
