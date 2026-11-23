# VII.15：整除次数的交换

现代整数模型，不是古代实跑或一般定理的计算证明。输入为 X、Y、Z；默认都是大于 1 的整数。单位量是 1，不是作为历史「数」给出的第四个输入。单位量度 X 恰为 X 次；如果 Y 量度 Z 同为 X 次，则以 X 为段长的相邻区间恰好覆盖同一整条 Z，而且需要 Y 段。

例如 X=3、Y=4、Z=12。按 Y 分割的切点是 0、4、8、12；按 X 重排的切点是 0、3、6、9、12；单位量度 Y 恰为 4 次。程序显式列出两个区间分割。测试另用遍历覆盖的单位格与 Fraction 核对。Z=13 有余数，Z=16 则能被 Y 整除但次数不符，两者均拒绝。modern=True 单独开放 X=1 或 Y=1 的现代算术边界；零、布尔和浮点数仍不接受。

## 重跑

当前目录用 Python 3.9+ 标准库，不需联网。

```sh
python3 -B unit_measures.py
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

每种模式 5 项测试。有限网格让 X、Y 各遍历 2 至 18，共 289 组。Notebook 有三个代码单元，按顺序以标准库真实回放，不是 Jupyter 内核运行。
