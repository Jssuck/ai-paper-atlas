# 独立复核：Sylvester 1852 原创教学复现

## 复核范围与当前结论

复核对象是本目录的原创 Python 实现、精确多项式证书、Notebook、输出数据与两幅原创 SVG；另直接核看原刊 366–369 页的扫描，并对 368 页使用较高分辨率图。原刊图片没有放入公开复现目录。复核不是另一套 OCR 的重复读取，也不是宣称取得了第二个独立历史底本。

在下述明确范围内通过复核：最终 40 个单元测试通过，Notebook 的 11 个代码单元由独立 CPython 运行器逐一执行并与保存输出完全一致，独立几何预言器和精确系数检查通过，两幅最终 SVG 已实际渲染并检查。复核发现的四类有界数值问题均已修复并回归。本报告不把有限采样、Python 单元测试或多项式恒等式称为关于一切证明方法的证明。

## 独立核查如何避免自我比较

1. **分角线与交点。** 不调用实现中的正弦长度式生成期望值。先以两条边的方向向量解 2×2 线性方程求顶点，再以向量叉积解分角线和对边直线的交点；独立计算有向投影、欧氏距离及边段参数。固定种子 1852 的 1,200 例通过，最大尺度化坐标误差约 7.2×10⁻¹³。覆盖正/负参数、内部/外部交点和不同底边尺度；这只是有限覆盖。
2. **角平分线。** 以坐标生成三角形，将相邻边的两个单位向量相加，直接求内部角平分线方向和对边交点，再测量长度平方。500 例与实现一致；没有以另一处抄写的角平分线长度公式充当几何预言器。
3. **精确恒等式。** 实现使用多变量指数—整数系数字典；独立核查改用稠密一元系数数组，以 a=z、b=z⁷、c=z⁴⁹ 编码。待核两边总次数为 6，各变量次数不超过 6，故该七进制编码无碰撞。清分母后两边各有 14 个非零项，差的每个整数系数均为零。这比代入 4,010 个有理数三角形更强，验证的是该多项式恒等式本身；仍不是证明助手中的全套形式化几何证明。
4. **圆弦。** 直接解直线与底弦所在直线的交点，再解直线代入单位圆后的二次方程，得到另一个圆交点。119 个方向通过，并检查固定图中的 1/2≤x<1。另确认 near_segment(3,1) 虽有合法代数正根，却小于 1/2，因而不能直接放进该固定圆和底弦配置。另用 90 位十进制运算检查 4 个正根实例。没有只用实现的 x(x+a)=b² 再与同一式比较。

完整可重复脚本：[review_oracles.py](evidence/independent-review/review_oracles.py)。实际结果：[oracles.log](evidence/independent-review/oracles.log)。几何误差容差和采样域写在脚本中。

## 数学定义与原刊字形

- 内角平分线是 n=2 的内部线段模型；正向射线、整直线的有向参数和通常绝对长度分开计算。n=−2、A=96°、B=24° 的精确角度实例有 t_A=−1、t_B=1；另保留 A=90° 下 B≈22.7350867996022° 的数值求根补充。两者都有 t_A=−t_B，且 t_A·t_B<0；它不能冒充原来的有向等式或两条正向射线实例。
- n=−1、A=B 时，无除法残差为零，但分角线与目标直线平行。实现必须拒绝交点；独立测试确实拒绝。A=B 时正切商有 0/0，也正确拒绝，不由此否定原正弦等式。
- 368 页两个特殊展示式的扫描右端可辨为 +1；第二分子的字形可辨为 (3α−β)/2。由 367 页通式重算以及 90° 例子验证后，教学修复式的比值应为 −1，第二分子应为 3(α−β)/2。报告支持的是字形与数学一致式的冲突，不推断排字者或作者手稿责任，不称为正式历史勘误。
- 369 页逆向圆弦式右端是 b²，非零。b 表示“半段弧的弦长”，即圆弧中点到两端点的等长弦；它不是底弦长度的一半。当前单位圆例子中 b=1，而底弦的一半为 √3/2。
- 等长角平分线的代数因式分解在正边长、严格三角不等式下，由 c、a+b+c、正系数多项式及平方分母的正性推出差的符号等于 b−a 的符号。机器系数证书检查恒等式；上述定义域和正性推理必须另保留。

## 图形与输出检查

两幅 SVG 均以 XML 解析；未发现脚本、嵌入扫描、外部图片或外链资源。随后用环境中已有的 Inkscape 实际渲染并逐图查看：分角线图能区分内部、延长线、负有向参数以及选定射线；圆弦图中的近段、远段、弧中点及 b=PU=PV 标注一致，未见内容截断或妨碍阅读的遮挡。

- [分角线图实际渲染](evidence/independent-review/divider-domains.png)
- [圆弦图实际渲染](evidence/independent-review/equal-chords.png)
- [渲染命令、退出码及警告](evidence/independent-review/render.log)

最初尝试的无配置 Chromium 渲染因不能建立临时用户目录失败，未把该尝试算作成功；改用现有 Inkscape 得到退出码 0 的 PNG。Inkscape 的字体包装/桌面对象警告原样保留在脱敏日志中，实际成图已检查。没有安装软件或写入远程服务。

## 数值边界和 Notebook 验收

初次实跑记录保存在 [robustness-before.log](evidence/independent-review/robustness-before.log) 及 [inverse-robustness-before.log](evidence/independent-review/inverse-robustness-before.log)，均含当时实现文件的 SHA-256；修复后的实际结果见 [robustness-after.log](evidence/independent-review/robustness-after.log)。发现及修复如下：

- 正向弦段根先平方很小的归一化比例，导致可避免的下溢。分支重排后，near_segment(10²⁰⁰,1)=10⁻²⁰⁰、near_segment(10³⁰⁸,1)=10⁻³⁰⁸。
- 逆向弦段先计算 b/a，可能在最终结果可表示时中间溢出。改用 r=a/b 的重排后，remote_segment(10⁻³²⁰,10⁻¹⁰) 约为 1.000011132941258×10³⁰⁰，与独立 90 位 Decimal 参考一致。
- 二分函数现在拒绝非有限的内部采样值，不再把内部全部 NaN 的测试函数误报为数值根。
- 极端尺度的角平分线平方无法用浮点表示时，改为明确的 DomainError，不再泄漏零除或溢出异常；等腰平方差本身可表示为零时保留正确的零值。

[独立回归核查](evidence/independent-review/regressions.log) 对上述可表示根采用纯相对误差（绝对容差为零），另检查应拒绝的案例。这里不宣称任意有限浮点输入、任意极小角或任意尺度都已得到穷尽验证；近退化问题和极端尺度仍须遵守接口的数值容差及表示限制。

最终 [单元测试日志](evidence/independent-review/unit-tests.log) 为 40/40 通过。Notebook 为 27 个单元，其中 11 个代码单元；[独立执行日志](evidence/independent-review/notebook.log) 记录每格顺序执行与保存的 stdout/stderr 逐字匹配。独立运行器复制输入到临时目录，不导入作者的 Notebook 执行函数；代码共享同一命名空间，执行结束即清理临时副本。没有启动 Jupyter 内核，没有使用 nbclient，也没有宣称通过官方 nbformat 全量 Schema。与原脚本一样，本复核只对当前普通 Python 代码单元有效。

最终实现的 evidence/artifact-sha256.json 中 13 项文件哈希全部重新核对一致。独立证据另有 [文件摘要](evidence/independent-review/review-sha256.json)。本次未改动实现源码，修复由实现者完成；复核者只写入自己的测试、报告和运行证据。

### 重跑命令

工作目录为当前复现目录。以下均只用标准库，渲染单独使用环境中已有的 Inkscape：

```bash
python -m unittest -v test_sylvester.py
python evidence/independent-review/review_oracles.py
python evidence/independent-review/robustness_probes.py
python evidence/independent-review/verify_notebook_independently.py
python evidence/independent-review/verify_regressions.py
```

命令不含机器绝对路径、账号、凭据或远程写入。图像渲染命令及退出状态列在 render.log；初始失败尝试和警告没有被当作成功证据。

## 复核边界

没有用有限网格声称分类所有 n 的根，也没有核验所有可能的几何辅助构造。本次只支持已明确建模的方程、定义域、实例和输出的正确性。特别是，任何上述程序结果都不能推出 Sylvester 关于“所有纯几何证明必须间接”的普遍判据。
