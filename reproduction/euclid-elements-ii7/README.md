# Euclid II.7：重叠矩形与曲尺形的精确教学核查

这是原创、仅使用 Python 标准库的有理坐标教学模型。原文阅读范围为 Fitzpatrick 2008 印56–57页以及中文正文所列 Heath 与 Joyce 来源。原命题依靠几何论证；本程序不会将有限枚举冒充一般证明，也不是形式化证明助手或尺规作图器。

## 对象与输入

`a`、`b` 分别是 AC、CB 的基系数，严格正；等分 `a=b` **合法**。基 `u,v` 必须非零、正交、等长。实际 AC、CB 长度分别为 `a*sqrt(dot(u,u))` 和 `b*sqrt(dot(u,u))`，面积乘 `dot(u,u)`。默认单位基时才可直接把 a,b 读为长度。接受精确 `int` 或 `Fraction`，拒绝布尔值与浮点近似。

A=(0,0), C=(a,0), B=(a+b,0), D=(0,a+b), E=(a+b,a+b), F=(a+b,b), G=(a,b), H=(0,b), N=(a,a+b)。实际点经原点平移与基向量映射。图的竖向基画向下，不是反转符号定义。G 在对角 DB 上。

| 原文区域简称 | 边界顶点 | 默认面积 a=3,b=2 |
|---|---|---:|
| AG | ACGH | 6 |
| GE | GFEN | 6 |
| CF，亦称 BG | CBFG | 4 |
| DG，亦称 GD | HGND | 9 |
| AF | ABFH | 10 |
| CE | CBEN | 10 |
| 曲尺形 KLM | ABENGH | 16 |
| 全平方 ADEB | ABED | 25 |

KLM 是曲尺形标记，不是三角形顶点。面积和 AF+CE=20，而区域并集面积只有16；交集 CF 面积4被计了两次。代码以鞋带公式计算凹多边形 ABENGH，另按基坐标区间交集核对 CF，然后验证容斥计数。遗漏 G 会把内凹拐角误连成斜边，不再是该曲尺形。

## 审核内容与边界

`construct` 产生固定构造证书，`verify` 校验模式、全部点名与精确坐标；显式检验对角线共线、三个正方形的等边/直角资格、AG=GE、同加 CF 后 AF=CE、重叠计数、曲尺形补 DG 后为整体，以及最终面积等式。

生产验证依赖同源规范构造，不能自称独立算法证明；外部独立审查脚本与记录另列于技术审查。所有资格检查使用显式异常，不能靠 `assert` 在优化模式下消失。等式在 a=0/b=0 等退化代数输入也可能成立，但本几何构造明确拒绝这些输入。负数、斜基、非等长基也不在模型范围。

## 一键重跑

在本目录运行：

```sh
python run_all.py
```

各命令与 exit code 写入 `run-summary.json`，环境写入 `environment.json`，不安装依赖。实际命令：

```sh
python -m unittest test_geometry -v
python -O -m unittest test_geometry -v
python -OO -m unittest test_geometry -v
python run_examples.py
python create_notebook.py
python verify_notebook.py
python draw_figure.py
```

20 单测在三模式各跑一次，网格项含64组正整数构形；另涵盖分数、等分、非单位正交旋转缩放、反射、非法输入与逐点篡改。四算例为(3,2)、(2,3)、(2/3,5/7)、以及基(3,4),(-4,3)的面积25倍缩放。

## Notebook 的实际执行方式

`teaching.zh-CN.ipynb` 五格代码使用 Python 标准库逐格 `compile/exec`，捕获真实 stdout；随后新命名空间回放并逐格比对已存输出。**未启动 Jupyter kernel**；`execution_count` 为 null，并在 metadata 标注。已读安装技能，但其本地 scaffold helper 未出现，采用明示结构生成的后备路线。可在具有 Jupyter 的环境中自行用 kernel 再跑；本仓未声称已做 kernel 测试。

## 图与日志

[原创 SVG](figures/ii7-overlap.svg) 展示四块、重叠和曲尺形，不复制原文图片。日志在 `logs/`，均为真实子进程 stdout/stderr，记录退出码。有限有理样本不覆盖所有实数，更不能替代原文的一般证明。无外部数据集、训练基线或统计指标，因为此任务是确定性几何教学核查。
