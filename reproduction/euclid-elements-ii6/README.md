# Euclid II.6：精确坐标教学核查

这不是自动证明器，也不是一般定理的完整复现。它把《几何原本》II.6指定构形变为有理数坐标，分别核查点、平方资格、区域面积及等积转移。来源及版本辨析见[中文深读](../../papers/ancient/euclid-elements-ii6.zh-CN.md)。[原命题在线版本](https://mathcs.clarku.edu/~djoyce/elements/bookII/propII6.html)。不附源书PDF或全文翻译。

## 范围与接口

- `a > 0`、`b > 0`为相对于基向量的坐标系数，顺序为 A–C–B–D。令S=u·u，实际AC=CB=a√S、BD=b√S；只有单位基S=1时，a、b直接等于对应长度。
- `construct(a=3, b=2, origin=(0,0), u=(1,0), v=(0,1))` 生成指定点证书；`verify(cert, 同一组参数)` 校验并返回各区域面积。
- 输入只收 Python `int` 与 `fractions.Fraction`，拒绝布尔值、浮点数、零长和负长。基向量须非零、等长且正交；可旋转、镜像、缩放和平移。不处理任意斜平行四边形、无理坐标或一般尺规作图可实现性。
- 原点局部坐标 A=(0,0), C=(a,0), B=(2a,0), D=(2a+b,0)，E=(a,a+b), F=(2a+b,a+b), H=(2a,b)，L=(a,b), M=(2a+b,b), K=(0,b), G=(2a,a+b)。从局部坐标经 `origin + x*u + y*v` 映射。
- `verify` 先核对精确构形与H在DE上，再核查CEFD/LHGE等边直角，独立用鞋带面积计算 AL=CH=HF，AM=AL+CM=CM+HF，再加LG补成整平方。末尾才对照长度乘积；不把最终平方差恒等式当成合法输入筛选条件。
- 证书点必须与指定规范构造一致，这是防篡改检查而非任意几何证明验证；构造与校验共享规范，独立技术审查另作外部计算以降低同源错误风险。

## 实跑

Python标准库，无第三方包、网络、密钥或付费服务。在本目录执行：

```sh
python run_all.py
```

该命令依次执行正常、`-O`、`-OO` 三模式20个单元测试（其中网格项64种正长度组合），四个例子，Notebook生成/实跑、Notebook新命名空间回放、SVG生成。命令与真实退出码在 `logs/`；汇总在 [run-summary.json](run-summary.json)，环境在 [environment.json](environment.json)。断言禁用不会关闭生产校验，因为校验用显式异常。重跑会替换本轮输出日志，不把本仓已有日志当作你的机器实跑。

默认 a=3,b=2：AL=CH=HF=6，CM=10，AM=16，LG=9，整平方25。其他例覆盖分数、旋转缩放平移、镜像，详见 [results.json](results.json)。测试还拒绝零/负长度、浮点/布尔、坏基、缺点/多点、非法证书容器及移动各点；这些数量只说明有限测试覆盖。

[教学Notebook](teaching.zh-CN.ipynb) 有5个代码格，已用标准库 `compile/exec` 按顺序执行并保存stdout，随后在新命名空间回放比对。**未启动Jupyter kernel，execution_count保持null**，不声称做过kernel执行。已读安装Notebook技能；本地未找到其脚手架helper，按其结构规则生成JSON。Jupyter用户可自行打开由首格运行。

[原创构形SVG](figures/ii6-gnomon.svg) 由 [draw_figure.py](draw_figure.py) 生成；标色辅助识别区域，N/O/P曲尺形标识不是新增点，本图直接以CM与HF描述其并集。图中相邻区域仅共享边界，不以SVG视觉精度代替面积计算。

独立核验及其计数以 [技术审查](technical-review.zh-CN.md) 和 [来源审查](source-review.zh-CN.md) 为准。有限有理数实跑不能证明所有欧氏构形、史学归属或现代二次问题的全部适用范围。
