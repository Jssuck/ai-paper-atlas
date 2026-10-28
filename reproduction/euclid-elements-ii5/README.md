# Euclid II.5 最小教学复现

[中文深读](../../papers/ancient/euclid-elements-ii5.zh-CN.md) · [来源审查](source-review.zh-CN.md) · [独立技术审查](technical-review.zh-CN.md)

这是原创现代有理坐标教学模型，不是完整尺规作图引擎或证明助理。原几何证明及版本说明见正文。本目录以精确算术检查构造后的点线资格、区域身份、等积替换链和覆盖；有限实验不能证明一般命题，也不能用现代面积代数循环奠定代数本身。

## 模型、输入与验证

[geometry.py](geometry.py)只接受普通整数与`Fraction`，拒绝bool、float、字符串和坏点容器。C为中点位置；u=CB，v=CE须非零、等长、垂直；t=CD/CB须严格满足0<t<1。此版本**只实现原图A—C—D—B的右半内切分支**，不把左半输入悄悄取绝对值。左半切分的一般数学情形可交换A/B名称，重选指向新B的基向量后应用同一证明；端点和D=C是本构造的退化极限，不属于该严格输入域。平移、旋转和反射均允许，负坐标不表示负长度。

以C+xu+yv为仿射坐标，A=(-1,0)、C=(0,0)、B=(1,0)、D=(t,0)、E=(0,1)、F=(1,1)、G=(t,1)、H=(t,1−t)、L=(0,1−t)、M=(1,1−t)、K=(-1,1−t)。H必须在BE对角线上。完整有序边界：

- CH：C-D-H-L；HF：H-M-F-G，二者是相等余形。
- DM：D-B-M-H，LG：L-H-G-E，二者是对角线所穿过的两小正方形。
- CM：C-B-M-L；DF：D-B-F-G；AL：A-C-L-K；AH：A-D-H-K。
- 磬折形gnomon：C-B-F-G-H-L；大正方形：C-B-F-E。

`construct`提供候选证书。`verify`不调用构造器，而逆解每个提交点的仿射坐标，逐个绑定点名、位置和有序区域边界；显式验证H共线、DH=DB和三正方形等边直角。四个格子由x=t、y=1−t两条内部切线组成，覆盖单位正方形，内部互不重叠，公共边界允许重合。这是由固定顶点和输入范围保证的覆盖，不是从“面积相加恰巧相等”推出覆盖。

随后用鞋带面积独立计算各区域，验证11项关系，包括CH=HF、分别加DM后的CM=DF、AL=CM、AH=AL+CH、磬折形=DF+CH、AH=磬折形，最后加LG补成大方。生产检查全用显式异常，优化选项不会删除验证。接口只面向声明的普通Python数据，不声称抵御任意恶意对象或超大整数资源耗尽。

## 真实运行与复跑

在本目录执行：

```sh
python3 run_all.py
```

仅Python标准库，无第三方安装。运行器使用当前Python解释器执行七条命令，日志以`python`作为解释器脱敏标签，记录stdout、stderr和退出码。环境没有账号、主机标识、私有绝对路径或秘密。

- [20项unittest](test_geometry.py)在normal、`-O`、`-OO`分别全部通过；网格测试包含64构形。覆盖右半切分、平移旋转反射、有理基、端点外点、零边、非方矩形、非直角菱形、坏数据、所有点坐标篡改、有序边界翻转、错对角线和整体平移伪证书。
- [四算例](results.json)：默认、旋转、反射均为21+4=25；分数例为45/49+4/49=1。各中间区域面积均保存，不只最终等式。
- [Notebook](teaching.zh-CN.ipynb)五个代码格依次标准库`compile/exec`实跑捕获stdout，再用新命名空间[回放](verify_notebook.py)，输出全部一致。**未启动Jupyter kernel**，`execution_count`保留null；不声称Jupyter前端渲染或完整nbformat模式认证。
- 已读安装的Notebook技能及结构规范；本环境未找到脚手架`new_notebook.py`，故按规范手建，不声称使用helper。
- [环境](environment.json)、[命令与退出码](run-summary.json)、[Notebook回放报告](notebook-check.json)。独立技术复核单独报告，不把不同检查计数累加为定理数量。

[构造与检查](geometry.py) · [测试](test_geometry.py) · [算例](run_examples.py) · [运行器](run_all.py) · [Notebook生成执行器](create_notebook.py) · [回放器](verify_notebook.py) · [原创图源码](draw_figure.py) · [原创SVG](figures/partition.svg)

真实日志：[normal](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)、[算例](logs/examples.log)、[Notebook执行](logs/notebook-execute.log)、[回放](logs/notebook-replay.log)、[作图](logs/figure.log)。

只公开原创解释、教学代码、原创图和脱敏运行证据，不含源书PDF或全文翻译。模型按Heath1908印382–383与Fitzpatrick2008印54–55的原构造标号建立；Joyce正文辅助核对。现代坐标是教学重构，不冒充古代文字。
