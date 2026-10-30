# III.19 最小精确教学复现

原创有理坐标模型，不是古代尺规过程或通用证明器。输入圆心O、正半径r、圆周点C、非零切线方向v和非零候选方向w；输出整线C+tw经过O的参数及证书。**整线**与以C为起点的正半射线分别处理。

## 数学与接口

`certify(o,c,r,v,w)`接受整数或Fraction（拒绝bool和float）。先核C在圆周，令a=C−O；由圆幂恒等式P(C+tv)=|v|²t²+2(a·v)t，整线不含内点等价于a·v=0。这个等价来自正文的一般证明（对应III.18的现代必要条件），不是程序测几个点后推断相切。候选w必须与v正交。

二维平面内两个非零垂直于v的向量平行，故O−C平行w。程序算t=(O−C)·w/|w|²，并明确核C+tw=O。r>0保证t不为零。t正时正半射线到达O，t负时只能由反向延长到达O。此方向区别不可从原图默默省略。

`verify`不调用`certify`；它重核输入前提、精确键和字段类型，并直接检查中心等式、共线行列式、范数及射线标签。共享的输入验证是范围检查而非完全独立实现；独立技术审查另行编写oracle。证书不能认证未知圆心、无坐标图或自然语言证明。

## 运行

仅Python标准库，无安装依赖。从本目录执行：

```
python create_notebook.py
python run_all.py
```

28单测在普通、-O、-OO三模式均通过。每模式网格432构形：3中心×3半径×4有理单位方向×3切向缩放×4法向缩放；216向内和216向外射线，2160圆幂样值。样值是恒等式实现的回归检查，不是相切全称性质的来源。另有4命名例、3拒绝例；单测覆盖平移、旋转、方向反序/缩放、非法类型、零向量、非切线、非垂直及字段篡改。`logs/`保存命令、真实输出与退出码，`environment.json`记录非敏感环境信息，`run-summary.json`给出计数。

构建时曾在`test_fraction`写入多余右括号，首次语法检查失败，删除多余括号后重新编译并完成全部三模式测试；该错误不属于几何结论或运行结果，最终源码可直接复查。没有将失败执行冒称通过。

## Notebook与原创图

[Notebook](teaching.zh-CN.ipynb)五格通过标准库compile/exec真实执行，`verify_notebook.py`再次逐格回放比对输出。**未启动Jupyter kernel**。已读Notebook技能，检查发现本环境脚手架CLI不存在，所以以标准库生成nbformat4文件，未安装第三方软件。

[原创SVG](diagram.svg)以O=(0,0)、C=(3,0)、r=3说明法线：w=(−1,0)时t=3；w=(1,0)时t=−3。两条有向参数表示同一无向直线，只有向内正半射线到圆心。图只是一例，不能替代证明。

[中文深读](../../papers/ancient/euclid-elements-iii19.zh-CN.md) · [Heath卷II](https://www.wilbourhall.org/pdfs/Heath_Euclid_II.pdf) · [Fitzpatrick对照版](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)

公开内容仅自有代码、教学图、原创说明与实际检查日志，不含原书PDF或全文翻译。模型限二维正定欧氏坐标及有理输入，有限测试不是实数域一般定理的证明。
