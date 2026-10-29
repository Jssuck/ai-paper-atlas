# II.10：向外延长与共同的AG平方

原创、有限、精确的教学实验，不是古代几何的机器形式证明，不是现代学习模型的完整复现。只用Python标准库，无网络、无依赖安装。

## 输入、图与量纲

单位基下取A=(0,0)、C=(h,0)、B=(2h,0)、D=(2h+t,0)、E=(h,h)、F=(2h+t,h)、G=(2h+t,−t)，严格h>0、t>0。D在B外侧，G位于D下方；E、B、G共线且B在中间。F不是II.9中的相交点，本条相交点是G。

允许原点平移及非零、正交、等长的有理基u,v，包括旋转、反射和统一缩放。h,t为基系数，非单位基下真实长度乘基长，平方乘基长平方。斜基、不等长基不保持这里的直角等腰结构，必须拒绝。

- 四次I.47：AE²=AC²+CE²；EG²=EF²+FG²；AG²=AE²+EG²；AG²=AD²+DG²。
- 关键桥接：AC=CE=CB、EF=FG=CD、DG=DB。
- 默认h=3,t=2：AE²=18、EG²=50、AG²=68；AD²=64、DB²=4、AC²=9、CD²=25。
- 验证器另外检查ACE、ECB、EFG、BDG、AEG、ADG六个直角。先核点与几何资格，随后比较平方关系，不以目标等式筛选输入。

坐标直接给出交点，只是教学核验。原文为何能把EB与FD延长相交、为何交点位于指定方向，需要正文的第五公设及角关系论证；有限坐标试验不能代替该论证。

## 接口和拒绝边界

`construct(h=3,t=2,origin=(0,0),u=(1,0),v=(0,1))` 返回仅含`points`的七点证书。`verify(c,h,t,origin,u,v)` 接受同组外参数，检查容器、标签、精确点、直角、等长、四次平方关系，返回`squares`、`routes`、`lhs`、`rhs`、`basis_norm_squared`。

只接受int或Fraction，拒绝bool、浮点、字符串及非法容器；生产校验用显式异常，不依赖可由-O移除的assert。h=0、t=0、负参数均拒绝；在t=0代数等式仍成立，不表示退化三角形已被这个构图覆盖。t可任意大，不把II.9的内分条件误搬到II.10。

点核验依赖同一规范构造，存在同源错误的局限；它不是任意七点图的证明器。独立技术审查应另行生成外部证书并独立计算平方和，不能仅重复调用construct。精确有理数消除浮点舍入，但有限测试不证明所有实数情形。

## 边径数：明确另一个层级

`side_diagonal(steps=8)` 从(s,d)=(1,1)起，输出(s+d,2s+d)及差值d²−2s²的符号翻转；步数只接受1至1000整数，不接受bool。每一步采用本条的h=s、t=d：AC=CB=s，DB=d，CD=s+d=s'，AD=2s+d=d'，故d'²+d²=2(s²+s'²)。移项得到d'²−2s'²=−(d²−2s²)。

这是现代精确整数旁支教学，不能据八步实跑声称证明一般递推、最优逼近或历史归属。其一般代数推导和史料边界见正文。不能把CD设为s同时把AC设为s+d，那会违反CD=CB+BD。

## 执行与证据

在本目录运行`python run_all.py`。七条真实命令和退出码见`run-summary.json`：

- `python -m unittest test_geometry -v`
- `python -O -m unittest test_geometry -v`
- `python -OO -m unittest test_geometry -v`
- `python run_examples.py`
- `python create_notebook.py`
- `python verify_notebook.py`
- `python draw_figure.py`

20单测×三模式通过；grid测试含64构形。覆盖正有理输入、平移、旋转、反射、非单位基、极短/极长外延、标签/坐标篡改、容器和标量拒绝及八步边径递推。四算例为默认、有理参数、反射缩放、近退化但仍严格正外延。

[Notebook](teaching.zh-CN.ipynb)五格经过标准库compile/exec执行，保留真实stdout；新命名空间回放输出逐字一致。**未启动Jupyter kernel**，execution_count为null；不能据此声称内核执行。nbformat4.5，所有单元有唯一id。

[原创SVG](figures/ii10-exterior-routes.svg)取自已验证七点证书，不复制源书图像。环境版本在`environment.json`，命令结果在`logs/`，无账户或本地绝对路径。重新执行只更新本地证据，不自动发布。
