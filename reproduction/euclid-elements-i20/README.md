# I.20 最小教学复现：延长、等腰与三角不等式

本目录是现代精确坐标教学核验，不是《几何原本》的完整形式化。原证从延长和等长截取出发，以 I.5、角的严格包含和 I.19 得到长边关系，再将共线段串接；代码的点积与根式比较另属现代核验，不能倒过来当作原作者证明。

## 执行与真实证据

在本目录执行 `python run_all.py`。仅使用 Python 标准库，无网络和新安装依赖。

- 普通、`-O`、`-OO` 三模式各36项测试、128份正证书、12组非法输入通过。
- [run-summary.json](run-summary.json)保存8条真实命令、开始时间、耗时、退出码；[environment.json](environment.json)记录实际环境；[logs/](logs/)保留输出。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)有6个代码单元，使用标准库 `compile/exec` 按顺序共享命名空间执行；**没有使用 Jupyter kernel，也未声称验证 Notebook 浏览器显示**。笔记本文件采用 nbformat 4，由本目录显式生成器创建。
- [SHA256SUMS.json](SHA256SUMS.json)不自含，不含缓存；加入独立审查后须刷新。

## 模型和边界

输入是三个有理坐标点，用 `point(int 或 Fraction, int 或 Fraction)` 构造。拒绝浮点、布尔、非有理扩域输入和共线三点。`Q` 只支持每次运算中一个共同非平方根号，不是通用计算机代数系统。

令 `u=B−A`、`v=C−A`、`t=sqrt((v·v)/(u·u))`，构造 `D=A−t u`。这一构型只需单个二次扩域；不直接把三个可能不同的平方根混进同一个对象。`AD²=AC²`，且 A 严格位于 B、D 之间。CA 是 CB、CD 的严格正线性组合，提供角内部关系的现代证据。

`angle_cmp` 通过点积的符号及经正量归一化的平方比较，比较普通无向角，允许角域[0,π]，拒绝零射线。不计算 `acos`。比较余弦的单调性属于现代解释，不假装原典使用余弦定理。

`sum_greater(u,v,w)`接受非负有理平方长度，比较 `sqrt(u)+sqrt(v)>sqrt(w)`：两边非负，平方等价于 `u+v−w+2sqrt(uv)>0`，由精确根式符号判定。它能展示退化的等号情形；几何构造仍拒绝退化输入。该函数不接受浮点或布尔。

`accepted`重建规范证书并比较严格JSON序列化：布尔、整数、浮点、元组、额外/缺失字段不能混同，证书绑定输入。**重放不是独立证明**；独立技术审查另从几何与代数条件核对。

## 文件

- [geometry.py](geometry.py)：构造、普通角比较、长度和比较、证书。
- [quadratic.py](quadratic.py)：精确单二次域算术，适配仓库既有原创教学代码。
- [cases.py](cases.py)：128个有理构型、12个退化输入。
- [test_geometry.py](test_geometry.py)：36测试，包含三顶点重标号、反射旋转平移缩放、极细三角形、类型与篡改。
- [WALKTHROUGH.md](WALKTHROUGH.md)：逐步推导与手算。
- [run_examples.py](run_examples.py)、[run_all.py](run_all.py)、[create_notebook.py](create_notebook.py)、[verify_notebook.py](verify_notebook.py)：可重跑证据生成流程。

有限有理样例不证明任意实数构型，更不证明任意几何空间。正文中的一般论证、原文依赖和其他范数的反例另行区分。见[中文深读](../../papers/ancient/euclid-elements-i20.zh-CN.md)。
