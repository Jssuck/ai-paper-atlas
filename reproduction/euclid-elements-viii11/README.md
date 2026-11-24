# VIII.11 · 整数比例中项：教学复现

回到[中文精读](../../papers/ancient/euclid-elements-viii11.zh-CN.md)｜[原典核对](source-review.zh-CN.md)｜[技术核对](technical-review.zh-CN.md)。

仅用 Python 标准库。实跑环境 Python 3.12.14，Linux。从本目录运行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

[构造及验算源码](square_means.py) · [测试](test_square_means.py) · [Notebook](euclid-viii11.ipynb) · [重放脚本](replay_notebook.py)  
[普通模式](normal.log) · [优化模式](O.log) · [二级优化](OO.log) · [Notebook 单元重放](notebook-replay.log)

`from_sides(c,d)` 接收正整数边，按文献顺序造出平方、中项、平方，返回三元组、边比与端点比，用精确分数表示比。`integer_mean(a,b)` 是现代扩展，对任意正整数端点计算整数平方根；只在回代成立时返回该数，否则返回 `None`。`is_mean` 直接比较交叉积。实现把单位和相等端点作为现代边界输入；不会把布尔值、浮点数、非正数当作合法参数。

一条测试对 196 对有序边测试构造和精确比；另一条对 1–36 的 1,296 对端点用**候选穷举**和**约分后平方表**与平方根法交叉核对，90 对有整数中项。包括首尾互换、相等端点、非平方正负例、超出浮点精度输入及无效参数。没有历史数据、统计指标或性能基线；三种解释器模式的检查旨在排除依赖可被优化清除的断言。Notebook 文件没有填入伪造执行结果；重放方式是标准库执行三个 Python 代码单元，不是启动 Jupyter 内核。仅应重放自己信任并审阅过的 Notebook。
