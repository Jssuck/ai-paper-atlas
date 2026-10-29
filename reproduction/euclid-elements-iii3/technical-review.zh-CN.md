# III.3 独立技术审查

结论：通过。审查对象为当前正文与配套精确坐标实现；不把有限测试称作一般证明或完整公理形式化。

## 绑定

- 正文 SHA256：`f09b528fb6042fc84a5429a07d3e28976a5df343f9b7a1fb1eea79dffc18a84b`
- geometry.py SHA256：`11c2aa89821a32eb7788a1ff53524062fa6014dc325035125331fc36433db246`
- Notebook SHA256：`99b514e32a40ac3aaa587ce986a9955adf7e407ba17a1a9036c6461eddff5864`
- SVG SHA256：`34296e92175939a84ea0005c12e7e3c40e45610a3c1cc1c7376d499ec0ca87a4`

## 证明与正文

正向三边对应为AF↔BF、FE↔FE、EA↔EB，I.8推出F处等角，直角定义才能给垂直；EF非零后才可把结论转移到CD。逆向先I.5，后直角相等，再用EF作为EAF/EBF对应角的对边调用I.26，不循环假定平分。

支持线垂足在弦内的补证有效：若F–A–B，EAB的A角为EAF的外角，大于F处直角；I.5与I.17矛盾。端点情形也会导致等腰三角形有两个直角。非直径条件确保三角形非退化，不能把EF=0的点积当几何方向。

独立展开验证两式：等半径推出(A−E)·v=−s/2，故(F−E)·v=(t−1/2)s；距离平方差=(2t−1)s。支持线上t可任意，但公共API刻意只收严格内点，正文没有混同两个适用域。正常4–3–5、斜交F=(1,3)、偏心x=1、直径斜线、非圆周端点及练习t=2数值均复核正确。附件3–4–5与正文4–3–5已明确不同坐标，未混用。

## 实跑

独立脚本[源码](independent_check.py)从不同尺度（含负尺度）、平移、正交同尺度变换、弦高及参数生成实例，独立算距离和点积预期值。负尺度只作为线性变换，不称镜像。

每种模式均实际执行并退出0：

- 普通、`-O`、`-OO`各1134合法证书，15876篡改证书，20非法输入；全部通过。
- 全字段篡改包括bool/int类型混淆、Fraction加一、tuple/list类型改变、字符串改变；重算核验均拒绝。
- 额外手算正文例子、零方向拒绝与外点恒等式通过。
- 五格Notebook独立只读compile/exec回放，与已保存stdout逐字一致；不是Jupyter kernel。
- 原24项单测再次在三种模式实际执行全部通过，各含900网格。

命令：`python -B independent_check.py`、`python -B -O independent_check.py`、`python -B -OO independent_check.py`，对应[普通](logs/independent-normal.log)、[-O](logs/independent-O.log)、[-OO](logs/independent-OO.log)。单测复跑见[普通](logs/review-tests-normal.log)、[-O](logs/review-tests-O.log)、[-OO](logs/review-tests-OO.log)。输入拒绝由显式异常实现，不依赖优化时可消失的assert。

## 图与边界

原创SVG使用已安装Inkscape导出PNG并实际目视：两圆等比例，左面板F为中点、直角标记正确；右面板F偏移、斜EF及4/2/6标注一致，文字不裁切。此为本地图形审查，GitHub最终显示由发布验收另外核实。

实现允许内建int/Fraction输入，证书采用Python tuple/Fraction对象，不声称JSON反序列化接口。证书核验不等于原文作图历史、任意实数计算、一般求交或现实圆识别。普通、优化模式和精确算术结果都不能取代正文一般证明。本次未发现阻断发布的数学或实现错误。
