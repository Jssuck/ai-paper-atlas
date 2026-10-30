# III.18 最小精确教学复现

这是原创有理坐标重构，不是古代证明器，也不以有限测试证明一般定理。给定圆心O、圆周点B、正半径r和任意非零直线方向v；**不先要求方向垂直**。原命题从相切推出半径垂直，本程序展示非垂直时怎样给出严格内部见证。

## 接口与数学范围

`certify(o,b,r,v)`仅接受整数或Fraction坐标，拒绝bool、float、非圆周点、非正半径和零方向。令u=B−O，q=u·v，s=v·v。垂足参数t=−q/s、垂足H=B+t v。返回字段包括q,s,t,H、H的圆幂及分支标签。

- q=0：H=B，整线幂为s t²。由正文的一般恒等式，直线没有内部点，只在B接触。
- q≠0：H的幂为−q²/s，严格小于零。直线进入圆盘内部，与相切假设矛盾。

标签tangent是在已验证圆周点和非零方向后、根据一般推导得到的分类，不是程序假设的输入前提。`verify`不调用构造器，独立核字段类型、精确键集合、H在线上、OH垂直方向、直接距离幂与严格符号。它检查受限结构化证书，不验证任意自然语言证明或未知几何图。

`line_power`直接算B+t v到圆心的平方距离减r²。有限抽样与解析恒等式区分：仅正文的一般推导覆盖所有实参数，日志只覆盖列出的有理数。射线与直线不混同：朝外射线可能始终不入圆，反向参数仍能给出内点，因而不能把半射线现象作为切线判据。

## 真运行与复查

Python标准库，无第三方安装。进入本目录后执行：

```
python create_notebook.py
python run_all.py
```

25单测在普通、-O、-OO模式均通过。每模式网格360构形：3个中心×3个半径×4个单位轴向×5个径向方向分量×2个切向分量。包含72切线分支、288内部见证和1800个幂恒等式值。单测另核径向穿心、反序与方向缩放、平移旋转、第二交点、非法输入及字段篡改。优化模式下仍用显式异常和unittest，不靠会被移除的assert保证正确。

命名例含切线、斜线、朝外射线但割线、穿心直线及三类拒绝。`logs/`逐条保存命令、真实stdout/stderr与退出码；`environment.json`记录环境，`run-summary.json`记录计数。独立审查可另加oracle与日志。

## Notebook及图

[五格Notebook](teaching.zh-CN.ipynb)由标准库compile/exec实际执行，另由`verify_notebook.py`顺序独立回放比对输出；**不是Jupyter kernel执行**。已阅读安装Notebook技能，但本机脚手架CLI不存在，因此用标准库构造nbformat4文件，未安装第三方依赖。再运行构建器会真实重新执行，而非填造输出。

[原创图](diagram.svg)展示r=3、B=(3,0)，斜线v=(1,1)的垂足H=(3/2,−3/2)幂为−9/2。图是单例，不能替代一般证明。正文原典字母F/C/G与此处O/B/H为不同标记系统。

[中文深读](../../papers/ancient/euclid-elements-iii18.zh-CN.md)；[Heath卷II](https://www.wilbourhall.org/pdfs/Heath_Euclid_II.pdf)；[Fitzpatrick双语版](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)；[Joyce III.18](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII18.html)。只发布自有代码、原创分析和检查后的运行证据，不附原书扫描或全文译文。
