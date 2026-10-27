# Euclid I.22：三边构造的精确教学复现

本包是原创的现代坐标教学重构，不是 Euclid 原证的形式化认证。输入三条正有理边 `a=FK`、`b=GK`、`c=FG`，在固定基边 `F=(0,0)`、`G=(c,0)` 上构造两个镜像顶点。它验证给定有限样本，不能用测试数量代替一般存在定理、圆连续性或原典证明。

## 运行

只使用 Python 标准库，不需网络或安装依赖。在本目录运行：

```sh
python run_all.py
```

真实命令和退出状态见 `run-summary.json`、`logs/`；环境见 `environment.json`。同一检查分别在普通、`-O`、`-OO` 模式运行，输出结果逐字相同。关键断言使用显式异常或 `unittest` 方法，不会被优化模式删除。

当前实跑：每种模式 36 项测试、444 份正证书、15 个非法输入；正证书包含两个方向及缩放样本，绝非444个互不等价的三角形。`results-normal.json` 另记录非有理高度证书数。8条子命令全部退出0。

## 输入与接口

- `construct(a,b,c,orientation=1)`：返回标准化 JSON 证书。整数、分数字符串、`Fraction` 可以输入；浮点数、布尔数、零和负边拒绝。`orientation` 必须是整数 `1` 或 `-1`，不接受 `True`。
- `classify(a,b,c)`：三边先验证为正，再按固定圆心距离c分类：`two_intersections`、`external_tangent_degenerate`、`internal_tangent_degenerate`、`separate`、`contained`。
- `verify(certificate,a,b,c,orientation=1)`：重新计算并逐项比较规范证书，绑定输入和方向。仅接受严格JSON子集；布尔与整数、整数与浮点、列表与元组不能混用。不支持任意等价书写，例如把字符串`3/2`改成`6/4`也会拒绝。这是证书格式校验，并非“等价数学表达式”通用判定器。
- `Quad(p,q,d)`：表示 `p+q√d` 的单二次域算术，只实现本构造需要的加减乘。不同d拒绝混合；`rational_value()`要求根式系数已经归零。它不自动把平方数根式化简，不是完整代数数库。

## 文件

- `geometry.py`：输入、交点分类、单二次域、构造与证书验证。
- `cases.py`：边长1至6的严格三角形，分别按1与2/3缩放，两个镜像均执行；非法/退化输入表。
- `test_geometry.py`：36项单元与回归测试，包含输入绑定、镜像、近退化、投影落基边外、证书篡改和严格类型。
- `run_examples.py`：确定性有限样本与三个教学算例，写入三模式结果。
- `create_notebook.py`、`verify_notebook.py`：构建并实际顺序执行六格Notebook。
- `teaching.zh-CN.ipynb`：已保存真实标准输出。执行方式是标准库 `compile/exec`，不是 Jupyter kernel、浏览器执行或 notebook 渲染验证。
- `WALKTHROUGH.md`：推导、算例与边界。
- `SHA256SUMS.json`：除其本身与缓存以外的公开文件摘要；新增独立审查附件后须刷新。

已读取安装的Notebook技能。其模板助手未在当前执行器文件系统找到，使用公开 nbformat 4 JSON 结构手工创建小型Notebook，未安装软件。Notebook内容和输出均经实际顺序执行，不声称用过不可用的助手或内核。

## 不涵盖什么

不处理任意实数输入、不构造重合圆（c=0不属于三条正边），不处理三维空间或非欧几里得几何，不认证尺规操作的物理误差，不机器证明圆交点存在公理。退化相切虽然有一个公共点，却不生成非共线三角形；返回分类不代表原命题允许退化。固定基边的两个镜像解不等于宣称绝对位置唯一；相合意义的唯一性属于另一论证层。
