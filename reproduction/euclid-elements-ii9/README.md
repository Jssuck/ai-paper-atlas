# II.9：同一条AF的两条平方和路线

原创、有限的精确教学核验，不是古代几何的机器形式证明，也不是现代学习模型的完整复现。仅Python标准库，无网络、无额外依赖安装。

## 模型与前提

单位基下取 A=(0,0)、C=(h,0)、B=(2h,0)、D=(h+d,0)、E=(h,h)、F=(h+d,h-d)、G=(h,h-d)。严格 h>0、0<d<h，因此A-C-D-B共线、F在EB内部、G在EC内部。

h,d是基系数；如果基向量长度不是1，实际长度要乘基长，所有平方量要乘基长平方。原点可平移，两基必须非零、正交、等长。旋转、反射、等比例缩放均支持；斜基或不等长基不能当成保持直角和等腰的坐标变化。

- 四个直角等腰三角形：ACE、ECB、EGF、FDB。
- 另外两个直角：AEF和ADF。
- 四个I.47等式：AE²=AC²+CE²，EF²=EG²+GF²，AF²=AE²+EF²，AF²=AD²+DF²。
- 需要的桥接：GF=CD、DF=DB。
- 默认h=5,d=2：AE²=50、EF²=8、AF²=58、AD²=49、DF²=DB²=9，2(AC²+CD²)=58。

这不是先用目标等式筛选合格输入；构造和证书检验先确定点、直角与等长关系，随后才比较两条平方和路线。

## 接口与限制

`construct(h=5,d=2,origin=(0,0),u=(1,0),v=(0,1))` 返回仅含 `points` 的七点证书。`verify(c,h,d,origin,u,v)` 接受同一组外部参数，检查标签、点坐标、直角、等腰和四条平方等式，返回 `squares`、`routes`、`lhs`、`rhs`、`basis_norm_squared`。坐标和参数仅接受int或Fraction；拒绝bool、float、字符串和非法容器。生产逻辑使用显式异常，不依赖可被-O删除的assert。

`normalized_segments(h,t)` 接收有符号中点偏移，0<abs(t)<h；t<0时返回交换端点的标志与d=abs(t)。它只给出规范化数据，不冒充在原坐标中已经画出左半图。原始AD=h+t、DB=h-t，交换二者不改变平方和。调用者再用返回的h,d生成右半规范图。几何输入不接受t=0、中点重合、端点、外分；恒等式在某些边界仍成立是代数扩展，而非本构图已经覆盖。

验证器用同一规范构造复核点，有同源局限，不是任意七点图的定理证明器。独立技术审查应另行生成外部点证书、独立计算平方量。精确有理数避免浮点误差，有限网格与篡改测试不能证明所有实数输入的一般定理；一般证明见中文正文。

## 执行与证据

本目录运行 `python run_all.py`，七条真实命令与退出码见 `run-summary.json`：

- `python -m unittest test_geometry -v`
- `python -O -m unittest test_geometry -v`
- `python -OO -m unittest test_geometry -v`
- `python run_examples.py`
- `python create_notebook.py`
- `python verify_notebook.py`
- `python draw_figure.py`

20单测×三模式均通过。其中grid单测含64个构形；覆盖有理分点、平移、旋转、反射、非单位基、左半规范化、点篡改、标签错误、非法参数和容器。四算例包含右半、左半规范化、有理偏移与接近端点。

[Notebook](teaching.zh-CN.ipynb) 含五个代码格，标准库逐格compile/exec并保存真实stdout；新命名空间回放与保存输出逐字相同。**未启动Jupyter kernel**，execution_count为null，不能据此声称内核执行。文件使用nbformat4结构，代码格保留顺序与唯一id。

[原创SVG](figures/ii9-two-routes.svg) 从经过验证的七点证书绘制，不复制源书图像。环境版本在 `environment.json`，真实日志在 `logs/`，只保存命令、结果和退出码，没有账户字段或本地绝对路径。重新运行只更新本地证据，不自动发布。
