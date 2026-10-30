# III.17 最小精确复现

这是原创教学重构，不是古代工具的完整模拟、任意实数求交程序或一般定理证明。原文的外点构造使用中心E、外点A、轴上原圆点D、辅助圆交点F、接点B。现代圆上点分支与内点可行性分析另外标识。

## 模型和接口

`geometry.construct(r,d,center=(0,0),axis=(1,0),side=1)` 接受正有理半径r、非负有理距离d、有理中心及有理单位轴向。只接受Python int/Fraction，不接受bool/float。外点d>r还要求h=sqrt(d²−r²)为有理数；返回E,A,D,F,B和切线方向。side取±1给出镜像分支。

以E=(0,0)、轴向(1,0)说明：A=(d,0)，D=(r,0)，F=(r,±h)，B=(r²/d,±rh/d)。这些公式构造F在辅助圆、B在原圆；验证器另外核半径、垂直、径向缩放和SAS所需边长。`verify`不调用构造器、不只比较预存输出。它仍是这个结构化模型的证书检查器，不是古代证明自动化。

圆上点d=r时，使用过A且垂直半径的方向，单独返回boundary证书，不建立退化的DEF三角形。d<r被拒是数学不可行域；例如r=1,d=2被拒则只是有理根实现范围限制，该外点在欧氏几何中当然可作切线。两种拒绝不能混淆。

`line_power(c,t)`直接计算B+t·direction的圆幂。通过证书后，正文的一般推导给出幂为t²乘方向长度平方；有限日志只核所列参数，不替代对所有实数t的证明。构造输出不以切线条件作为输入筛选。

## 真运行与重跑

Python标准库，无第三方依赖或安装。先进入本目录，依次执行：

```
python create_notebook.py
python run_all.py
```

28单测在普通、-O、-OO三模式运行；每模式324构形、648双分支证书、3240幂值核查。六组毕氏长度对×三种缩放×三个中心×六种轴向，含平移、旋转、镜像。示例含三外点分支、一圆上点及两类拒绝。单测还含零半径、负距离、非单位轴、非法分支、类型错误、零方向、缺键、多键及点位篡改。有限网格不覆盖无理坐标或任意实数。

`logs/`保存实际命令、stdout/stderr和退出码，`environment.json`及`run-summary.json`记录环境与计数。测试使用unittest和显式异常，优化模式不会删除关键核验。独立技术审查与其日志另存本目录。

## Notebook与图

[五格Notebook](teaching.zh-CN.ipynb)由标准库compile/exec真实顺序执行并由`verify_notebook.py`独立回放比对输出；**不是Jupyter kernel执行**。已读取安装Notebook技能，但其本机脚手架脚本不可用，因此使用符合nbformat4结构的本地构建器，未安装第三方软件。Notebook metadata明确执行方式。

[原创示意图](diagram.svg)取r=3,d=5，蓝色原圆、灰色辅助圆，两条红色镜像切线。图只示意一例，不证明任意外点构造。原文标签沿用Heath/Fitzpatrick，文字标签略偏移以清晰显示，所有数学坐标以代码为准。

正文与来源：[中文深读](../../papers/ancient/euclid-elements-iii17.zh-CN.md)；[Heath卷II](https://www.wilbourhall.org/pdfs/Heath_Euclid_II.pdf)，印43–44；[Fitzpatrick双语版](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)，印88–89。这里只公开原创代码、解析和真实日志，不附原书全文或扫描。
