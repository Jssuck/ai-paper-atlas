# 《几何原本》卷 V 命题 7：等量替换的两组比例

[回到中文精读](../../papers/ancient/euclid-elements-v7.zh-CN.md)。

用正有理坐标与量类标签模拟 V.Def.5 的三态比较。A、B、C 在此教学模型须为同类且事先统一单位；标签不做单位换算。由于坐标是正有理数，V.Def.4 所要求的可用整倍数相互超越在此模型内成立。整倍比较允许正整数 1 作为探针；不把 1 称为严格倍量。

一对探针 p、q 同时给出前向 pA 与 qC、pB 与 qC 的符号，和后向 pC 与 qA、pC 与 qB 的符号。先检验 A=B，再核对两组符号。交换前向的两个探针系数并翻转比较符号可以得到后向检验；这只是对两个结论关系的程序核对，不把任意同比的倒比推论当成原命题的新前提。

不合格示例：A=17/16、B=18/17、C=1。p、q 均在 1–8 时，两方向都未找到分歧；但令 p=16、q=17，前向输出 (0,−1)。交换下标后，后向为 (0,+1)。前向见证直接从 A/C 约分结果取得：分母为 p，分子为 q，保证 pA=qC；B≠A 则 pB≠qC。这是正有理数专用构造，不声称不能整次相等的任意不可公度量也可使用同一个办法。

## 环境及实跑

仅使用 Python 3.12.14 标准库。进入本目录后执行：

```sh
export PYTHONDONTWRITEBYTECODE=1
python --version
python equal_ratio_probes.py
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python replay_notebook.py
```

三种模式各通过 10 项测试。有限网格含 2 种量类、4 种 A=B 坐标、4 种 C 坐标与 6×6 个探针下标对，共 1,152 个探针对，每对核查两个方向，还独立核对交换下标后的符号翻转。三种比较结果均出现。日志只略去 unittest 耗时；Notebook 的 3 个代码单元已由标准库依次编译执行，未运行 Jupyter 内核或前端。有限网格不代替对任意比较系数的证明。
