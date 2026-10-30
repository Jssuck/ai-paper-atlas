# III.24 · 等底相似弓形的精确教学复现

这是现代坐标教学重构，不是欧几里得原文算法、一般几何证明、通用证明器或现代 AI 实验。原证将等长底叠合后，用 III.23 排除内外不重合，III.10 排除交叉，再用公共概念4由重合得相等。这里只对明确的有理参数做有限核验；不分发原文 PDF 或全文翻译。

## 模型、输入与非循环性

`Segment(a,k,mid,e,n)`：a 是正半底长，mid 是底中点，e 是沿有序底方向的单位向量，n 是指向选定半平面的单位向量。e、n 必须正交，但允许行列式为 ±1，因此覆盖旋转和反射的有理实例。所有数值只接受 int 或 Fraction，拒绝 bool 和 float。单位与正交检查是精确等式，不是容差。

局部端点为 (-a,0)、(a,0)，圆心 (0,k)，半径平方 a²+k²。弓形是圆盘与局部 y≥0 的交集。k>0、=0、<0 分别为大弓形、半圆、小弓形；不是把 k 限于非负。局部射线(-a,0)+u(1,t)取 t>0，第二交点 u=2(a+kt)/(1+t²)还必须严格为正。角测量须在选定开弧、不是底端点或圆内任意点。

对弧上 P，向量 PA、PB 的点积为 x²+y²−a²=2ky，绝对行列式为2ay，所以 cot(angle)=k/a。所容角在(0,π)，cot单射；精确比值不能取绝对值来混淆互补角。

`align_point_to` 仅要求等底 a 相同，以“源世界点→源局部坐标→目标世界点”定义刚体映射，不要求相似或相同 k。该映射保持距离，把两个有序端点与选侧对齐。`aligned_circle_matches` **随后**检查映射圆心等于目标圆心、半径平方相等。等底而 k 不同的输入可成功对齐底，却不能通过圆匹配检查；因此不把结论当作映射的输入条件。

`similar`比较 k/a，而 `coincides`检查同底端点集、相同选侧单位法向量、相同圆心与半径平方。一个弓形与其镜像可以相似且刚体可叠合，原位置却不重合。同一个非直径圆的另一侧则通常与原弓形角互补，不能将这两种操作混为一谈。端点倒序不改变点集，模型也明确核查这个分支。

## 文件、命令与真实实跑

Python标准库，无第三方依赖。进入本目录：

```sh
python3 run_all.py
```

该脚本先生成原创SVG，再按正常、`-O`、`-OO`运行Notebook生成、28单元测试、算例、Notebook回放；记录每条命令、退出码、实际环境和时间。三模式重复相同输入，不是三倍不同样本。验证逻辑不依赖会被优化移除的裸 assert。

- [geometry.py](geometry.py)：精确模型、刚体对齐和网格。
- [test_geometry.py](test_geometry.py)：28个测试，含退化、非法类型、镜像、底方向倒序、半圆、近等不等、非相似底对齐。
- [run_examples.py](run_examples.py)：a=2,k=3/2,P=(3/2,7/2)等可手算例子。
- [run_all.py](run_all.py)、[environment.json](environment.json)、[run-summary.json](run-summary.json)：运行入口、真实环境、统计。
- [logs/test_geometry-normal.log](logs/test_geometry-normal.log)、[logs/test_geometry-O.log](logs/test_geometry-O.log)、[logs/test_geometry-OO.log](logs/test_geometry-OO.log)：三模式单元测试。
- [logs/run_examples-normal.log](logs/run_examples-normal.log)：实际精确算例输出。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)、[create_notebook.py](create_notebook.py)、[verify_notebook.py](verify_notebook.py)、[logs/verify_notebook-normal.log](logs/verify_notebook-normal.log)：5代码格按顺序实际compile/exec并逐字回放，**不是Jupyter kernel执行**，execution_count始终null。未声称完整nbformat模式验证。技能默认helper未在环境找到，按其结构指南生成，无新安装。
- [diagram.svg](diagram.svg)、[make_diagram.py](make_diagram.py)：1040×460原创坐标示意图，浮点仅作显示，不参与精确计算。

每模式39配置（3半底长×13比值），156刚体放置（4框架/位置），936开弧测角检查，6552成员对应检查，39不等底等比例放大对照。所有对应的通过结论都仅针对这组输入。

## 独立技术核验

[独立检查器](independent_checks.py)不调用主模型射线取点函数，而从60组任意有理点反解圆心，再以另外书写的全局正交映射核对360次放置、1440对距离、7200次区域成员判定、360组非相似对照、5个正文算例和6项非法输入。normal、`-O`、`-OO`均通过，日志为[普通](logs/independent-normal.log)、[优化](logs/independent-O.log)、[双优化](logs/independent-OO.log)。这些仍为有限检查。技术审查发现world接口未对输入坐标拒绝float/bool；已统一使用精确坐标验证，并加入两个回归测试，故单测增至28项。

```sh
python3 independent_checks.py
python3 -O independent_checks.py
python3 -OO independent_checks.py
```

## 适用范围与失败边界

几何论证适用于实数欧氏平面；本实现只接受有理坐标与有理正交框架，所以不是任意实数刚体变换器。成员网格不是连续区域枚举。面积数值未计算，区域相等的解释来自等半径圆盘和对齐半平面的交集；有限样本本身不能证明区域相等。不存在训练数据、基线、泛化精度或性能比较。

零/负底、非单位/非正交框架、底端点作角顶点、错侧圆周点、未进入半平面的射线都明确拒绝。极小非零有理差保留，测试不会将10^-30差别当成相等。复现未形式化原文公设、刚体运动公理化或III.23全部综合证明。

## 来源与关联

实读III.24在线原文及其Guide：[Joyce, Book III Proposition 24](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII24.html)。完整书目、Heath/Fitzpatrick对照及一般证明见[中文正文](../../papers/ancient/euclid-elements-iii24.zh-CN.md)。原文与现代坐标推导分层，不把这份软件说成原书已有程序。
