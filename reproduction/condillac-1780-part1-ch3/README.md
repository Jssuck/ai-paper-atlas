# Condillac《逻辑》第一部第三章：现代分解／重建教学模型

这是原创、低成本、可重复运行的现代语法模型。它帮助区分“保留零件”“保留关系”“重建原结构”“得到相同输出”四个问题。它不是 Condillac 提供的算法，不是对人的认识活动或实体机械的实证复现，也不验证他关于分析法普遍有效的哲学主张。

## 文本范围与版本

依据《Œuvres de Condillac》卷 XXII，Paris：Ch. Houel，An VI–1798，*La Logique*，第一部第三章，实际印页 25–31（该扫描的 PDF 页 33–39）。关键启发来自印页 27 的机器分解和按原次序重新组合。印页 32 起的下一章不属于本次范围。

- [1798 年版公开扫描，直接打开第三章](https://archive.org/download/b28772581_0022/b28772581_0022.pdf#page=33)
- [同一版本的另一份公开书目／扫描记录](https://books.google.com/books?id=tdSdMhj8gcwC)

目录名中的 `1780` 只是作品的书目年标签，不认证最早版次，也不代表本模型采用了 1780 年版的逐字文字或原页码。

## 最小环境与运行

- Python 3.10 或更新版本；作者实测 Python 3.12.14
- 仅 Python 标准库；没有 pip 依赖、网络请求、随机数、训练、GPU 或付费服务
- 在本目录运行以下命令；所有结果由本地程序产生

```bash
python --version
python demo.py
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python -OO -m unittest discover -s tests -v
python enumerate_model.py
```

`verify.py` 是统一作者验证入口，运行上述演示、穷举和三种优化模式测试，逐项检查退出码，并保存真实输出：

```bash
python verify.py
```

此命令覆盖 `validation/author-validation.log`、`validation/demo-output.txt`、`validation/census.json`、`validation/manifest.json`。日志标明 UTC 时刻、解释器版本、命令、退出码和完整 stdout/stderr。`manifest.json` 给出代码、测试、文档和验证入口的 SHA-256，可核对独立审阅针对的内容。作者验证不冒充独立审阅。

## 文件导读

- `MODEL.zh-CN.md`：领域、全部形式假设、编码和解码定义、结构归纳证明、最小反例、穷举计数及适用边界
- `WALKTHROUGH.zh-CN.md`：逐步运行与手算示例
- `model.py`：树、严格校验、带类型前缀表示、解析、输出和三个投影
- `demo.py`：与导读对应的八个表达式及拒绝样例
- `enumerate_model.py`：1–4 叶、叶值 {0,1,2} 的完整有限普查
- `tests/test_model.py`：18 个测试方法，内含参数化样例及全域检查
- `validation/`：作者实际运行输出；后续独立审阅应单独标识

## 已运行结果

1、2、3、4 片叶子的树分别为 3、18、216、3240 棵，共 3477 棵。全部不同的结构前缀均成功往返。完整前缀、有序叶序列、叶多重集、整数输出分别产生 3477、120、34、15 个等价类；细节见 `validation/census.json`。

这些数字是指定有限域内的精确计数，不是成功率、准确率、实验受试者结果或统计估计。一般性的往返结论来自证明，有限测试只检查本实现及选定输入域。

## 输入边界

`parse` 接收 Python 元组组成的元组。例如：

```python
(("SUB",), ("LEAF", 2), ("ADD",), ("LEAF", 0), ("LEAF", 1))
```

这不是文本协议。程序不执行 `eval`；不会自动转换 JSON 列表、字符串、浮点数或布尔值。`census.json` 中的列表只是便于阅读的 JSON 展示形式，不能直接当作 `parse` 输入。无效输入抛出 `TypeError` 或 `ValueError`；安全校验使用显式分支，在 `-O`、`-OO` 下仍生效。

数学定义允许任意有限树与整数；实际运行受内存、整数表示、执行时间等资源约束。生成器规模增长很快；本任务只穷举到 4 叶。树的核心遍历／解析是迭代实现，但 dataclass 的相等比较及 Python 的整数转字符串仍有各自的运行时限制。演示的大深度测试只证明所测试深度上的行为。

## 完整阅读与独立审阅

- [本章完整精读](../../papers/1780/condillac-logic-part1-ch3.zh-CN.md)
- [版本、页码与来源核验](../../papers/1780/condillac-logic-part1-ch3.sources.zh-CN.md)
- [完整论证审阅](../../papers/1780/condillac-logic-part1-ch3.audit.zh-CN.md)
- [独立代码审阅报告](independent-review/review.zh-CN.md)

独立审阅的对象、方法、结果及限制由各报告自行列明；作者日志保持单独标识。

## 可选原创示意图

`figures/structure.svg` 和 `figures/structure.png` 是为本次讲解制作的原创图，不是历史原图。图示比较同一叶序列和减法操作在不同括号结构下的输出；核心模型、18 项测试、演示及穷举均不依赖图形包。

在本目录可仅用标准库重新生成 SVG：

```bash
python figures/build_figure.py
```

仅当需要重新生成 PNG 时，才需额外准备 Pillow 12.3.0 及 DejaVu Sans／DejaVu Sans Bold 字体；然后运行：

```bash
python figures/render_png.py
```

PNG 渲染是可选图形流程，其验证另行记录，不属于 `verify.py` 的无第三方依赖核心验证。已附的 SVG／PNG 可以直接阅读，无需安装这些可选组件。
