# 《几何原本》IX.28：奇数次取偶数，积为偶数

按 VII.定义15 的乘法方向，以奇数 $`A`$ 决定份数，取偶数 $`B`$ 共 $`A`$ 份。每取一份 $`B`$，两边都添一份 $`B/2`$，因此每一步的总数都等于两组半数的和。例如 $`A=3,B=8`$，逐次总数为 8、16、24，每侧半数合计 12。

程序限制奇数份数 $`A\ge3`$、偶数每份 $`B\ge2`$。偶数份数乘偶数仍为偶数，说明奇数份数不是现代一般结论的必要条件；交换输入在本接口不合前提，却不改变现代乘积。单位份数和零份数不在该古代非单位正数模型内。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线用加法预生成输入类型及半数的对照表，再用直接乘法核对重复累加的实现。两输入各取 1 至 64；日志的步数按每取一份计一次，不是所有算术操作的总数。有限检验不替代证明。Notebook 日志来自标准库回放三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-ix28.ipynb) · [普通模式](normal.log) · [-O](O.log) · [-OO](OO.log) · [Notebook 回放](notebook-replay.log)
