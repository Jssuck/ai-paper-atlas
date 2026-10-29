# Euclid Elements II.13 — 精确投影与面积差

原创、仅 Python 标准库的教学复现。这里验证

**BC² + BA² = AC² + 2 BC·BD**，

D 是 A 到 BC 所在直线的垂足，所选角 B 严格锐。此处的乘积是矩形面积；不是三角形面积。

## 原命题与现代推广必须分开

- `original-domain`：三个角都严格锐。调用 `verify(A,B,C,original_only=True)` 可强制此定义域；足必在 BC 内部。
- `modern-extension`：仅 B 锐，但 A 或 C 直/钝。仍满足同一恒等式，**不称为原命题的全锐三角形**。
- `case` 独立显示 `interior`（0<t<1）、`at-C`（t=1）、`beyond-C`（t>1）。内足不充分保证全锐；例如 A=(2,1)、B=(0,0)、C=(5,0) 顶角 A 钝。
- B 直/钝、共线、重合点、bool/float 或非法坐标格式均拒绝。仅接受二维整数或 `Fraction` 坐标。

原图主证明：II.7 应用于 D 对 BC 的内部分割，给出 BC²+BD²=DC²+2BC·BD；两边同加 AD²，再通过两次 I.47 分别代入 BA²、AC²。现代外足/端点情况以向量展开验证，不能冒称原文同一构形。`II7_algebra` 只是等式检查标签：外足情况下不宣称调用了原始内分命题；端点情况下某个辅助三角形退化，平方和等式仍有效，但不把它称作非退化直角三角形的 I.47 应用。

## 运行

进入本目录，运行：

```sh
python run_all.py
```

这会真实运行 normal、`-O`、`-OO` 各 **23 项 unittest 方法**（其中一项遍历 54 个有理三角形），输出净化的 `logs/tests-*.log`，以及实例、SVG 生成和 Notebook 重放日志。生产校验无 `assert`，优化模式不会跳过验证。`run-summary.json` 记录每步退出码。

`teaching.zh-CN.ipynb` 是教程；已实际读取安装的 Notebook 技能，但指定本地 `new_notebook.py` helper 不存在，因此 `create_notebook.py` 以标准 nbformat 4.5 结构生成。`verify_notebook.py` 顺序 compile/exec 五个代码格并写回输出：**不是 Jupyter kernel 执行**，没有安装依赖，也不声称验证了 kernel 集成或 Notebook 浏览器排版。运行目录必须是本目录；`run_all.py` 自动切换到该目录。

## 精确性与局限

任意有理 A、B、C：u=A−B，v=C−B，t=(u·v)/|v|²，D=B+tv。BC·BD=u·v，无需平方根；边长可无理而乘积有理。所有几何计算使用 `Fraction`；只有 SVG 显示宽度转换为浮点像素。

测试覆盖三种足位置、内足顶角直/钝、全锐限制、非锐 B、退化、非法类型、极小正投影、有理平移/旋转/缩放/反射，以及无理长度的有理乘积。有限实例与测试不是普遍定理的证明。

原创图：`figures/ii13-projection-cases.svg`。上排三种投影构形，下排用同一面积比例尺比较总量与 AC²+橙色矩形差。几何模型与向量说明属于现代教学重构，不是古文程序化转录。

文件：`geometry.py` 核心；`test_geometry.py` 单测；`run_examples.py` 示例；`draw_figure.py` 图生成；`create_notebook.py` 教程生成；`verify_notebook.py` 非 kernel 重放；`run_all.py` 入口。没有网络调用或第三方依赖。
