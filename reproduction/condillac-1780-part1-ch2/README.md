# Condillac《逻辑学》I.II：有序观察与关系重组

这是**原创的现代教学重构**，只用 Python 标准库。它帮助拆开“列出对象”“记录关系”“重组一个可比较的整体”这三件事。它不是孔狄亚克写过的算法，不是心理学实验，也不验证其全部哲学主张。

## 读的是什么

- 唯一历史文本：Condillac, *La Logique*, 第一部第二章。
- 年代标记采用作品 **1780 年版的书目年，不裁定最早版次或发行日期**；本次实际读取的是 **1798 年《全集》第二十二卷，印页 16–24，对应提供的 IA/Wellcome PDF 第 24–32 页**。不声称逐字核验了 1780 年版。
- 16–18 页：一次看到许多东西，与能分辨并说明这些东西不同；把同样的未分辨印象延长，不自动变成知识。
- 19–22 页：先比较主要对象的位置，再把其余对象按关系放入；依次分解，是为了在心中重组共存的秩序。
- 22–24 页：同时在心中呈现，不等于每一部分都同样清楚；进一步分析仍需要依次辨明，整体还承担核对是否遗漏的作用。

程序仅挑出其中**对象身份与相对位置的关系结构**。形状、感觉、灵魂、练习对人的影响、对多片风景的审美判断等，不由这个模型说明。页码对应和本地源文件哈希见 [PROVENANCE.json](PROVENANCE.json)。

## 三分钟运行

需要 Python 3.10 或更新版本；本次用 CPython 3.12.14 实跑。无需安装包、网络、GPU、API 密钥或 Notebook。

```bash
cd reproduction/condillac-1780-part1-ch2
python3 run_all.py
python3 -O run_all.py
```

第一条重跑常规模式；第二条检验 Python 优化模式，并把 `-O` 明确传给各个子进程。检查使用显式失败函数，不会随优化关闭。本次两种模式均实际通过，优化模式的证据另存于 `logs/optimized/` 和 `outputs/optimized/`。脚本会重新生成对应模式的执行日志和 JSON 结果。也可分别运行：

```bash
python3 -m unittest discover -s tests -v
python3 walkthrough.py
python3 exhaustive.py
```

建议顺序：先读 [逐步中文走查](WALKTHROUGH.zh-CN.md)，再读 [一般模型与证明](MODEL.zh-CN.md)，最后看 `model.py`。教程不要求预先了解图论。

## 最小例子

五个教学对象为 A 主楼、B 塔、C 磨坊、D 桥、E 树林。为了能手算，只取一条水平轴，教学参考位置为 0、6、2、9、12。数字与具体对象名称均为本次构造，**不在原文中**。

```python
from model import ObservationBook, reconstruct

book = ObservationBook(("A", "B", "C", "D", "E"), 1)
for name in book.inventory:
    book = book.observe_object(name)
for u, v, distance in (("A", "B", 6), ("A", "C", 2),
                       ("B", "D", 3), ("B", "E", 6)):
    book = book.observe_relation(u, v, (distance,))

result = reconstruct(book)
print(result.summary())
print(result.difference("C", "E"))  # (10,)，虽未直接观察 C→E
```

这时有 5/5 个对象、4/10 对直接观察的不同对象关系，以及 10/10 对可由关系推出的相对位置。**不必直接观察所有对象对**；精确且一致的连通关系网已经足够。A 放在 0 只是选定坐标原点，不能据此说已经知道绝对位置。

## 本次核验

- 18 个单元测试方法通过，其中两个方法含 40 个非法输入子例。
- 五对象案例含：正确重组、只列对象、重复记录、漏掉 E、关系断开、错绑 C、矛盾循环、整体平移。
- 四条正确关系的全部 24 种次序得到同一个最终相对布局。三个矛盾关系的全部 6 种次序都被拒绝。
- 独立枚举坐标赋值的 oracle 与生产求解器对照：一维 216 个三对象图，二维 1,000 个三对象图，共 1,216 个输入图；430 个一致，786 个不一致。
- 每个图还检查反转全部边并取反偏移的结果，以及在测试范围内求解器表示的整个解族是否恰好等于直接满足方程的赋值。
- 642,496 是“输入图 × 候选赋值”的检查次数，**不是独立图的数量，更不是人的实验次数**。有限测试不代替一般证明。

实际命令、退出码、时间和运行环境分别保存在 [logs/commands.json](logs/commands.json)、[logs/environment.json](logs/environment.json)。主日志见 [logs/unit-tests.txt](logs/unit-tests.txt)，完整例子见 [outputs/walkthrough.json](outputs/walkthrough.json)，穷举计数见 [outputs/exhaustive.json](outputs/exhaustive.json)。计时只记录本机程序执行，不能解释成人类观察效率。

## 重要边界

1. **一致不等于真实。** 把 C 的偏移错误地绑定到 B，可以得到自洽但错误的整图；程序不知道观察者有没有认错对象。
2. **完整清单是外部给定的。** 没有可靠对象范围，就不能凭本模型宣称没有遗漏。
3. **“同时整体”是表示层面的类比。** 程序保存一整套关系，但一次查询只问一对；这既不验证也不否定人类同时呈现多项内容的能力。
4. **没有证明主要对象优先普遍最优。** 同一组精确约束的最终解集与输入次序无关；教程另设的中途指标只是明示的账面指标。
5. 坐标轴方向、尺度、身份标记固定；输入是精确整数向量。模糊测量、噪声、旋转、遮挡、连续知觉和自动视觉辨认均未建模。
6. 只处理这一章。不包含扫描 PDF、逐页图像或 OCR 全文；没有 Notebook 执行声明。

## 文件说明

- `model.py`：严格输入检查、对象登记、差分约束、连通分量与平移解族
- `walkthrough.py`：教程的真实可运行案例与全部小规模次序排列
- `tests/test_model.py`：边界、反例、非法输入与回归测试
- `exhaustive.py`：不用生产遍历算法判断满足性的直接赋值 oracle
- `run_all.py`：在本地重跑并保存证据；会覆盖本包的日志与结果
- `MODEL.zh-CN.md`：一般定义、性质及证明、穷举界限解释
- `WALKTHROUGH.zh-CN.md`：逐步手算和带答案练习

所有代码均为本次教学用途新写。没有复制或替代旧章节的文件。
