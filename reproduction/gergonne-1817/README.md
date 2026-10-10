# Gergonne 1817：有限模型教学复现

以 Python 标准库重建《Essai de dialectique rationnelle》的外延逻辑部分。原文刊于 1817 年 1 月 1 日，卷 7、页 189–228；卷标为 1816–1817，不应把卷首年份当成本篇日期。

这是原创教学代码，不是发现或重跑一份历史源码，也不是对论文全部哲学论述的计算验证。[原文（NUMDAM）](https://www.numdam.org/item/AMPA_1816-1817__7__189_0/)

## 30 秒运行

要求 Python 3.10+，无安装、无网络、无第三方依赖。进入本目录：

```sh
python walkthrough.py
python run_checks.py
```

`run_checks.py` 会真实执行测试、重新生成结果、执行教学导览，保存运行环境、命令、退出码、耗时、完整日志与 SHA-256 清单。只想生成表：

```sh
python reproduce.py --out results
python -m unittest discover -s tests -v
```

随包实跑记录：30 项主测试和 9 项独立审查测试通过。独立审查额外采用见证约束求解、四对象论域枚举、源文图像比对和归约证书检查，可另行重跑：

```sh
python independent-review/audit_checks.py
```

## 结果

- 109 个三类均非空的占用模式 →54 个精确关系三元组，与 §49 扫描页独立转录逐项相符
- 256 个三段论候选 →24 个有效式；原文四个 figure 各 6 式
- 结论 A/N/a/n 的数量为 1/4/7/12
- 对其余 232 式逐一给出最小反例
- §59 的八条规则对全部 256 候选与模型判断一致
- 换位、对当、§§51–52 原例及 24→14→11→6→2 的分阶段归约均可复查
- 独立空类边界实验只余 15 个有效式，不混入主实验

这些结论背后的完备性证明见 [PROOF.md](PROOF.md)。测试还用独立的三对象具体集合枚举交叉验证，不能把该交叉检查误称为普遍完备性证明。

## 阅读顺序

1. `walkthrough.py`：中文逐步导览，先表示原子，再检查原例与反例，最后做归约和空类对照
2. `gergonne.py`：语义、figure、模型检查、八条规则、换位和归约
3. `PROOF.md`：为什么任意大小（包括无限）的外延都能压缩到七原子模型
4. `tests/test_gergonne.py`：自动化检查及独立求值器
5. `results/summary.json` 和 `results/validation.log`：可读结果及实际运行记录

`source_tables.json` 含单独读扫描页得到的 §49、§55、§58 表、§§63–64 选定代表，以及 §§51–52 的原文例句，并非从本程序结果反向生成。自动测试比较完整集合和原文代表，既查漏项，也查多项。两个例子保留原文 N(M,P) 的方向。

重要源文差异：§55（印刷页 216）N 行第四项实际印为 CH；紧接的 §56（页 217）重排同组关系时明确印 DH，且 §49、§52 及直接反例均支持 DH。本包分别保存原样转录与建议校正，明确报告原样不符、校正后相符。CH→DH 是本次指出的数学修正，未列入同卷正式勘误。它不影响 §49 的 54 项逐项吻合、§58 的 24 式及后续归约结果。

主要数据文件：

| 文件 | 用途 |
|---|---|
| `models_109.json` | 所有规范模式及具体 P/M/G 外延 |
| `relations_54.csv` | 54 个精确关系三元组及见证 |
| `relation_composition_25.csv` | 每个关系对的全部可能结论 |
| `moods_256.json` | 每个候选、原文/现代 figure、前提模型数、规则判定、反例 |
| `invalid_countermodels_232.json` | 仅无效式和最小反例 |
| `original_examples.json` | §§51–52 的准确有向例子；采用正式勘误 IH |
| `reductions.json` | 等价类、包含边、原文代表和四个反证证书 |
| `empty_term_boundary.json` | 空类边界与失效的九式 |
| `environment.json` / `validation.log` | 本次实跑环境、命令、耗时、日志 |

## 最容易读错的三处

- 字母 A/N/a/n 是作者命题符号；这里没有擅换成现代 A/E/I/O。I 是“外延相同”关系。
- D 是本项目对原文反向 C 的 ASCII 别名；rA/rN/ra/rn 表示原文旋转字形。r 不是否定。
- 原文 figure I/II/III/IV 对应常见现代 I/IV/II/III。三元关系固定按 (M,G),(P,M),(P,G) 排列，不能随 figure 改向。

主实验明确采用三个类都非空的外延语义，以匹配原文五关系划分、下属关系和 24 式。D、r 前缀、bit mask、JSON、自动反例均属现代教学表达。

本包使用可直接执行的 `.py` 导览，没有 `.ipynb`，因此不宣称执行过 Jupyter kernel。所有检查只需普通 Python。
