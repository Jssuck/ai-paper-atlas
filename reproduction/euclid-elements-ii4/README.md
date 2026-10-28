# Euclid II.4 最小教学复现

[中文深读](../../papers/ancient/euclid-elements-ii4.zh-CN.md) · [来源审查](source-review.zh-CN.md) · [独立技术审查](technical-review.zh-CN.md)

本目录实现第二卷命题4的现代有理坐标证书，不把数值实验当一般证明，也不声称完整复现尺规作图、公理系统或证明助理认证。正文重建原几何证；本目录检查其一个明确的现代模型。

## 输入与证书

`geometry.py`仅接受整数或`Fraction`，拒绝浮点、布尔和字符串。A为起点，u为AB，v为AD；两向量必须非零、等长、垂直。t为AC/AB，须严格介于0与1。平移、旋转、反射均可；负坐标不是负长度。模型不要求取平方根。

参数坐标为A=(0,0)、B=(1,0)、D=(0,1)、E=(1,1)、C=(t,0)、F=(t,1)、G=(t,1−t)、H=(0,1−t)、K=(1,1−t)。实际坐标由A+xu+yv得到。原文对角线是BD，不是GH；G为BD与CF交点。四区域依原文简称：HF为H-D-F-G；CK为C-G-K-B；AG为A-H-G-C；GE为G-F-E-K。HF与CK为正方形，AG与GE为等面积余形。

`construct`产生候选证书；`verify`不调用构造器，而用行列式逆解每一点的仿射坐标，逐一点名绑定，校验有序区域边界、直角、正方形等边、G在BD上。两条参数切线x=t及y=1−t把单位方形划为四个闭区域：内部两两不交，边界可以共享；四格参数面积之和为1。已绑定的顶点与严格内部切点一起排除漏区、错位和等面积重叠冒充覆盖。最后独立鞋带面积验证余形相等与四块总面积。

这仍以现代坐标、行列式和有理算术为前提，不能用来无循环地奠定代数分配律；有限有理测试不覆盖不可通约情形。一般结论须靠正文证明。

## 真实执行与重跑

在本目录运行：

```sh
python3 run_all.py
```

运行器使用当前Python解释器执行七条命令，命令中的`python`是该解释器的脱敏标签。每条命令独立保存stdout、stderr及退出码。只用Python标准库，无安装操作。

- 18项unittest分别在normal、`-O`、`-OO`全部通过；网格测试包含64构形。生产检查使用显式异常，不依赖优化时删除的assert。
- 四算例：[results.json](results.json)。整数例与旋转/反射例均为25=4+9+6+6；单位边长分数例为1=4/49+25/49+10/49+10/49。
- [Notebook](teaching.zh-CN.ipynb)有5代码格，以标准库`compile/exec`顺序实跑并保存stdout，再用新命名空间回放，输出全部一致。**未启动Jupyter kernel**，`execution_count`保留null；不声称Jupyter前端渲染或完整nbformat模式认证。
- 已读安装的Notebook技能与结构规范；本机未找到技能脚手架`new_notebook.py`，故按规范手建，没有声称使用模板helper。
- [环境](environment.json)、[命令与退出码](run-summary.json)、[Notebook检查](notebook-check.json)。独立技术复核另见独立审查报告，不能把其计数与单元测试相加成定理证明数。

## 文件与反例

[模型](geometry.py) · [测试](test_geometry.py) · [算例](run_examples.py) · [运行器](run_all.py) · [Notebook生成执行器](create_notebook.py) · [回放器](verify_notebook.py)

[原创SVG](figures/partition.svg)由[源码](draw_figure.py)生成：AC=2、CB=3，四块4、9、6、6；纸面向下为AD方向，仅改变图示方向，不改变标号。

测试覆盖端点和外切、零边、不等长矩形、等边但非直角菱形、浮点/布尔/字符串、坏点容器、缺失字段、对角线错误、逐点篡改、交换小方、反转区域边界，以及整体平移后面积仍相等的伪证书。检查器面向声明的普通整数/Fraction数据，不承诺抵御任意恶意Python对象或超大整数资源耗尽。

真实日志：[normal](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)、[算例](logs/examples.log)、[Notebook执行](logs/notebook-execute.log)、[回放](logs/notebook-replay.log)、[作图](logs/figure.log)。

仅公开原创解析代码、原创教学图及脱敏真实证据，不含源书PDF、全文翻译、私人对话、账户或秘密。来源与历史说明见正文。
