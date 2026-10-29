# Euclid III.9：精确有理数教学证书

这是《几何原本》III.9 的**现代坐标教学重构**，不是古代算法复原，也不是一般几何证明助手。Python 标准库 `fractions.Fraction` 进行精确运算，不用浮点容差；有限测试不能证明一般定理。

![三点等距与直径中点分支](diagram.svg)

## 输入与两种问题

`geometry.py` 的公开入口接受三个二维点以及（需要时）候选点。坐标只接受整数、有理数字符串或 `Fraction`；拒绝布尔值、浮点数、坏分母及非法形状；三个点必须互异且不共线。

- `circumcenter(points)`：求**任意**非共线三点的外心。钝角三角形的外心可以在三角形外，不要求候选点在三角形内。
- `make_certificate(points, candidate)`：先验证候选点到三点的平方距离严格相等，再记录中点、垂分线法向量（即弦方向向量）、垂直平分线残差和非零行列式。
- `verify_certificate(cert)`：从输入重新计算全部字段，进行类型严格的规范 JSON 比较；篡改字段、增加字段、漏字段均不通过。它是同一教学实现内的复核，不是独立形式化证明器。
- `certify_known_circle(points, candidate, known_center, radius_squared)`：额外验证三点确实位于**已提供参数**的同一正半径圆上。这才对应“给定圆的圆心”问题。程序不能从三个无背景的点认证一个未知对象的整个圆周。

## 数学对应与零方向分支

设三点为 A、B、C，候选点为 D，E 为 AB 中点、F 为 BC 中点。展开平方距离并相减，得到 `(B-A)·(D-E)=0` 与 `(C-B)·(D-F)=0`。三点不共线保证两条垂分线法向量（即弦方向向量）的行列式非零，因此两条垂直平分线有唯一交点。`circumcenter` 用二元线性方程求该点，证书记录两个残差均为零。

当 AB 是直径且 D=E 时，**D-E 是零向量，不可拿它确定直线方向**。程序以非零弦向量 B-A 作垂直平分线的法向量，故不错误拒绝这一合法分支。原几何证明可用 I.11 在 E 处作 AB 的垂线：D=E 使 D 属于该线，III.1 推论使给定圆心也属于该线，再与另一条不同的弦垂直平分线利用交点唯一性确定中心。普通弦的中点本身并不足以确定圆心；这里没有把退化的“三角形 ADE”当成合法三角形。

只有两点等距不足以确定圆心：A=(3,4)、B=(3,−4)、C=(−5,0)，D=(3,0) 到 A、B 的平方距离都是16，到 C 则为64。程序拒绝这一候选点。

## 真实运行与复现

从本目录运行：

```sh
python run_all.py
```

运行器调用以下六个子进程，并保存各自 stdout、stderr、退出码；不依赖 `assert` 实施输入验证：

```sh
python -m unittest -v test_geometry
python -O -m unittest -v test_geometry
python -OO -m unittest -v test_geometry
python run_examples.py
python create_notebook.py
python verify_notebook.py
```

此次 CPython 3.12.14 实跑：三个模式各24项测试通过，六个子进程退出码全部为0。每个测试模式中含600个精确圆实例（25种平移 × 4种正有理缩放 × 6种三点形状）；因此是每模式600例，不是600条独立测试方法。另含普通、第一/第二弦为直径、钝角外心、重复点、共线点、非法数值、错误圆参数、错误候选点、证书篡改等检查。

五个输出算例为普通圆、直径分支、平移、有理缩放以及三角形外部外心。详见：

- [源码](geometry.py)、[测试](test_geometry.py)、[算例](run_examples.py)、[运行器](run_all.py)
- [环境](environment.json)、[六次退出码](run-summary.json)
- [普通测试日志](logs/tests.log)、[-O 日志](logs/tests-O.log)、[-OO 日志](logs/tests-OO.log)
- [算例真实输出](logs/examples.log)
- [Notebook](teaching.zh-CN.ipynb)、[生成器](create_notebook.py)、[只读回放器](verify_notebook.py)
- [Notebook 执行日志](logs/notebook.log)、[只读回放日志](logs/notebook-replay.log)

Notebook 有5个代码单元。使用标准库 `compile/exec` 在共享命名空间实际执行并捕获输出，再只读执行全部单元逐一核对已存 stdout。**未启动 Jupyter kernel**，`execution_count` 留空；不能把它称为 kernel 复现。已检查安装技能所指模板脚本不可用，因此用本地 nbformat4 构造器，未安装第三方依赖。

## 证据边界

一般结论依靠平方差恒等式、非共线性的非零行列式及直线交点唯一性证明，而非600例枚举。程序仅处理有理坐标，不能覆盖所有实数输入；不证明古希腊文本的版本史、不判断图像上的点是否精确共圆、不验证未经提供的圆周。SVG 是原创示意图，不是测量证据。日志仅记录教学运行，未包含私密对话、主机账户路径或秘密。
