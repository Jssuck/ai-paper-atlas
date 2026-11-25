# VIII.22 教学复现：返回整数平方根

配套[深读](../../papers/ancient/euclid-elements-viii22.zh-CN.md)、[原典核对](source-review.zh-CN.md)与[独立技术核对](technical-review.zh-CN.md)。构造用现代整数运算验证连续比例与首项平方，再以整除求末项正根，不是古代的执行记录。单位和等端点只按现代约定测试。

仅需 Python 标准库，实跑 CPython 3.12.14。在本目录执行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

- [源码](square_endpoints.py)、[测试](test_square_endpoints.py)、[Notebook](euclid-viii22.ipynb) 与[回放脚本](replay_notebook.py)。
- [普通](normal.log)、[-O](O.log)、[-OO](OO.log) 均为 5 项通过；[回放](notebook-replay.log)使用标准库执行 3 个代码单元，不是 Jupyter 内核运行。

端点各取 1 至 100，10,000 对有序输入的预期接受集合独立由平方表构成。实际接受 100 对，拒绝 210 对有整数中项但首项非平方的链，以及 9,690 对无整数中项的端点所配的一条向下取整候选。后者不代表遍历了所有错误中项。没有外部数据、历史实验或性能基准；有限检查不能代替整数性证明。
