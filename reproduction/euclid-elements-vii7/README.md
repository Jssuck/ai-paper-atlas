# 《几何原本》VII.7：减去同一份，余项仍同一份

[中文精读](../../papers/ancient/euclid-elements-vii7.zh-CN.md)重建古代配份和消去步骤。本目录用现代坐标和有限整数样本核验，不代替原证。

## 运行

仅依赖 Python 3.9+ 标准库：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[程序](subtract_same_part.py)、[测试](test_subtract_same_part.py)、[Notebook](euclid-vii7.ipynb)；实跑：[普通](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)、[回放](notebook-replay.log)。顺次执行 3 个纯 Python 单元，未调用 Jupyter 内核或验证前端渲染。

## 核验与限制

- 依次输入 AB、CD、AE、CF，前两项是待比较的全数，后两项是各自移去的数。要求 AB/CD=AE/CF=1/n，且都是真份，移去数严格小于对应全数。先向 C 外侧构造 CG=n·EB，再把 CF 对应的 n 份与 CG 对应的 n 份逐项配对相加。以 C 为 0，G、F、D 分别置于 −CG、CF、CD。核对匹配所得 GF=CD，再去掉共同 CF，得到 CG=FD。
- 例 (8,24,3,9) 给出 EB=5、CG=15、GF=24、FD=15；余比 1/3。穷举 3,036 个配置（AB=3 至 25、AE=2 至 AB−1、n=2 至 12），逐一检查坐标顺序、共同段消去，并用标准库 `Fraction` 独立核验三个比。253 例的 EB 恰为单位。没有声称古代「数」包括 1；正整数模型可分析题设四项均非单位而算出单位余项的情形。
- 输入 1 默认拒绝，可明确开启现代扩展。零移去或整项移去都不是这里的合法情形。若原比 1/3、移去的比 1/4，例如 (8,24,3,12)，余比会变为 5/12。程序显式构造两个等块序列，只作有限教学示范。
