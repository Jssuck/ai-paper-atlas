# Euclid II.3 最小教学复现

[中文深读](../../papers/ancient/euclid-elements-ii3.zh-CN.md) · [来源审查](source-review.zh-CN.md) · [独立技术审查](technical-review.zh-CN.md)

本目录只实现第二卷命题3的现代有理数坐标模型。整体AE是矩形；所选分段CB上的CDEB（亦称CE或DB）才是正方形。没有把II.2的整体正方形条件偷换进来；没有完整复现古代尺规构造、公理基础或证明助理认证。

## 输入、构造与独立检查

`geometry.py`接受`A,u,v,t`：A为基点，u是AB，v是AF（亦为CD、BE），t是AC占AB的比例。所有标量必须为Python整数或Fraction，布尔、浮点和字符串不接收。要求u非零、0<t<1、u与v垂直，且v的长度平方等于(1−t)²乘u的长度平方。后一条件保证高等于CB，通常不等于AB，也未必等于AC。

点位：B=A+u，C=A+t·u，F=A+v，D=C+v，E=B+v。证书包含六点及三条有序四边形边界：AE为A-F-E-B，AD为A-F-D-C，CE为C-D-E-B。`construct`提供候选，`verify`不调用构造器，而是逆解非奇异仿射坐标核对每个点，再核对区域顶点、直角、对边、正方形等边和共享边，最后用鞋带公式独立计算面积相加。严格参数区间和精确顶点绑定对应相邻两条参数带，防止等面积却重叠或错位的区域蒙混过关。反射及平移允许，负坐标不是负长度。

这是按现代坐标模型检查有限输入，不是从实验推导一般定理。Fraction只覆盖有理坐标；不可通约长度的一般几何证明须看正文。鞋带公式和向量运算本身依赖现代算术，不能声称它们无循环地奠定分配律。

## 重跑命令

在本目录运行（仅Python标准库，不需安装依赖）：

```sh
python3 run_all.py
python3 independent_check.py
python3 -O independent_check.py
python3 -OO independent_check.py
```

`run_all.py`用当前解释器执行七条命令，每条写入自己的真实日志；日志中的`python`表示该运行器当前解释器，不是另一个环境。它重跑三种模式单元测试、四算例、Notebook生成与标准库执行、Notebook回放、原创SVG。修改代码后必须重跑，不能沿用旧日志。

## 本次真实结果

- CPython 3.12.14，标准库；[环境](environment.json)、[命令及退出码](run-summary.json)。
- 21项unittest在普通、`-O`、`-OO`三模式全部通过；其中网格项含64构形。主命令七条全部退出0。
- 独立技术脚本每模式120合法证书、360项解析面积对照、2273项非法或篡改拒绝；普通、`-O`、`-OO`均通过，见[独立命令与退出码](independent-run-summary.json)。该数量不与单元测试数相加成“定理证明数”。
- [四算例JSON](results.json)：整数例24=8+16；旋转例15=6+9；反射例24=8+16；分数例3/2=1/2+1。
- [Notebook](teaching.zh-CN.ipynb)有五个代码单元，真实`compile/exec`顺序执行、保存stdout，另在新命名空间回放且输出一致；[检查记录](notebook-check.json)。没有启动Jupyter kernel，execution_count保留null，不声称完成Jupyter前端渲染或nbformat完整模式认证。
- 已阅读安装的Notebook技能和结构规范；环境中没有找到技能脚手架helper，读取其脚本资源也未成功。因此此Notebook按规范手建，未声称调用模板helper。所有代码格已按上文真实执行，不为此安装第三方包。

## 文件

- [模型及证书检查器](geometry.py)、[单元测试](test_geometry.py)、[独立核验](independent_check.py)。
- [运行器](run_all.py)、[算例](run_examples.py)、[Notebook生成与实跑](create_notebook.py)、[回放器](verify_notebook.py)。
- [原创新图生成器](draw_figure.py)、[图](figures/partition.svg)：AB=6、AC=2、CB=4，高4；右侧正方形面积16，左矩形8，整体24。上下翻转原图纸面方向不改变点名。
- 测试日志：[普通](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)。
- 独立日志：[普通](logs/independent-normal.log)、[-O](logs/independent-O.log)、[-OO](logs/independent-OO.log)。
- 其他日志：[算例](logs/examples.log)、[Notebook执行](logs/notebook-execute.log)、[回放](logs/notebook-replay.log)、[作图](logs/figure.log)。
- [SHA256清单](SHA256SUMS.json)记录交付文件（不包含自身及随后绑定正文的审查报告，避免循环hash）。

## 反例与范围

测试检查外切/端点、零底边、不垂直、错高、浮点/布尔、坏容器、错点、反序或错区域、平移后面积仍相等的伪证书。生产检查不用可被优化模式删除的assert。独立脚本检查的也是声明的现代模型，不保证任意Python恶意对象、任意大整数资源耗尽或完整几何系统的安全性。

本目录公开原创代码、解析图和经检查的真实运行证据，不含源书PDF、全文翻译、账户或会话信息。原文来源与史学解释以正文和来源审查为准。
