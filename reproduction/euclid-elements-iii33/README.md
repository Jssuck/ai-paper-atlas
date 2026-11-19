# 《几何原本》III.33：从一条弦和一个角构造弓形

[返回正文](../../papers/ancient/euclid-elements-iii33.zh-CN.md)

这是现代坐标教学重构，不是完整欧几里得尺规解释器。给弦端点 A、B，再以整数或有理数 (u,v) 指定与正水平轴成的角（v>0）。令 d=B−A，j 为 d 逆时针转 90°，取切线目标射线 u·d+v·j。左右方向的约定是输出弧位于有向弦 AB 的右半平面。若要镜像，需把该侧约定也镜像；代码的等变检验仅面向保持定向的有理相似变换。

非直角分支取切点法线与弦中垂线之交为圆心；直角分支直接取中点。圆的同圆性、切向垂直、交替侧、普通角相等分别核验。角签名保留点积的符号，只用叉积的绝对值；等角要求两对数正比例，避免误把补角混成同一角。另以精确的同侧见证验证补角；直角的两侧虽同为直角，侧别仍不可混写。

选取见证点时，沿 d ± s·j 从 A 作割线，s=v/(|u|+v)。第二个交点参数是 2(O−A)·(d ± s·j)/|d ± s·j|²，两者都严格为正，因为 |u|s/v < 1。这个选点规则是教学额外构造，不是原文的作图步骤。一点见证不能替代 III.21 给予的整条开弧上的角一致性。

## 运行

在本目录使用 Python 3.12（标准库，无外部数据或包）：

```sh
python segment.py
python -m unittest -v
python -O segment.py
python -O -m unittest -v
python -OO segment.py
python -OO -m unittest -v
python replay_notebook.py
```

- [模型源码](segment.py) · [6 项单元测试](test_segment.py)
- [普通模式](normal.log) · [优化模式](O.log) · [二级优化模式](OO.log)
- [教程 Notebook](euclid-iii33.ipynb) · [回放脚本](replay_notebook.py) · [实跑记录](notebook-replay.log)

三个模式各跑 315 个有理数组合，其中锐角、钝角各 156 个，直角 3 个。另测非法角、零长弦、错弧、射线缩放与有理相似变换。枚举不是一般证明，也不涉及统计准确率。本次环境没有 Jupyter 或 ipykernel；实际通过纯 Python 的 compile/exec 回放了三个 Notebook 代码单元，没有运行 Jupyter 内核。Notebook 不嵌入伪造输出。
