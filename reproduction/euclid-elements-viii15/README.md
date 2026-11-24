# VIII.15：立方数的量度与边长的量度

现代整数教学重构，不是古代实跑或一般命题的计算证明。先建立平方层 E=C²、F=CD、G=D²，然后用 A=CE、H=CF、K=DF、B=DG 得到立方桥。若 C 量度 D 共 k 次，则三个相邻的量度次数均为 k，A 量度 B 共 k³ 次。反向从 A 量度 B 开始，沿 VIII.7 的思路核对 A 量度 H，再由 H/A=D/C 恢复 k。直接整数求余与 Fraction 分别核对程序的证书。

(4,12) 的立方桥为 (64,192,576,1728)，三个相邻次数为 3，首末次数为 27；(4,6) 无相应的整除。Joyce 在线版如果把附加的「A 量度 G」当成证明所需前提，就不能覆盖 (2,6)：此时 A=8，G=36，B=216，A 量度 B 却不量度 G，而 C 确实量度 D。这是额外条件非必要的对照，不是原命题反例。默认边长是不同的非单位正整数，现代模式另收单位与等边。

## 重跑

在本目录使用 Python 3.9+ 标准库，无需联网。

```sh
python3 -B cube_divisibility.py
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

每模式运行 5 项测试。有限网格为两边各取 1 至 40 的 1,600 对，其中 158 对存在向前量度。另核对超大整数与非法输入。Notebook 三个代码单元由标准库真实顺序回放，并非 Jupyter 内核运行。

实跑环境：Linux / CPython 3.12.14。回到[中文精读](../../papers/ancient/euclid-elements-viii15.zh-CN.md)，查看[原典核对](source-review.zh-CN.md)和[独立技术核对](technical-review.zh-CN.md)。

[实现](cube_divisibility.py) · [测试](test_cube_divisibility.py) · [Notebook](euclid-viii15.ipynb) · [重放脚本](replay_notebook.py)

[普通模式](normal.log) · [-O](O.log) · [-OO](OO.log) · [Notebook 重放](notebook-replay.log)
