# III.4 独立技术审查

结论：通过。审查日期2026-10-29。此报告针对下列哈希，不把有限测试称为一般证明或古典公理形式验证。

## 1 数学与正文

逐项检查了否定合取与逐项否定的区别、两次III.3的非直径/非零方向条件、原图角包含关系和同侧射线教学补足。第4节正确区分逻辑逆否先得“至少一条直径”，然后由共同中点唯一性推得交点为圆心及两直径。平面方向独立时的两行消元正确；重合弦不能代替两条约束。

正文五组构形与第10节答案一致。独立手算核验D平方距离25、E参数5/13、EB²=10、ED²=128/5及BD中点(−9/10,27/10)，另核都不平分、单直径及正文所用正交双直径。有限精确实现与一般实坐标代数论证分层清楚；近似残差不推出精确圆心的警告合理，没有声称完成误差分析。

初审发现正文§7误写“给定交点”。已修为输入圆心/半径平方/四端点，并以行列式计算交点和参数；与函数签名一致。实现非平行有理直线交点，不是通用圆线求交器或图像认证。

## 2 源码和独立真实运行

独立脚本[independent_check.py](independent_check.py)从10个有理圆周点的四点组合选交叉对角线，采用直线方程的独立交点计算和中点算术建立期望字段，再做三组缩放、平移与反射。atan2只用于测试输入的圆周排序，所有验证期望和相交计算保持Fraction精确运算。

每个normal/-O/-OO模式：630合法证书，其中465个满足原命题两非直径范围、18个为共同中点；13230个字段/布尔整数混淆篡改全部拒绝，68个非法输入及29个畸形证书全部拒绝，7组正文手算通过。独立结果见[normal](logs/independent-normal.json)、[-O](logs/independent-O.json)、[-OO](logs/independent-OO.json)。这不是穷尽全部输入。

原24单测也在三模式独立重跑通过，分别见[normal](logs/review-tests-normal.log)、[-O](logs/review-tests-O.log)、[-OO](logs/review-tests-OO.log)。输入拒绝bool/float、非规范有理字符串、非正半径、非同圆端点、零弦、平行/重合弦、端点相交；验证不依赖会被优化移除的assert。JSON规范比较正确区别布尔和整数；证书不能自行声明适用性。两直径被接受为扩展模型案例，但theorem_applies明确为false。

所有独立实际命令、返回码及解释器版本存于[independent-commands.json](logs/independent-commands.json)。未安装第三方包，未进行外部数据写入。

## 3 Notebook和原创图

Notebook五格顺序compile/exec的独立只读重放与保存stdout完全一致，execution_count均为null。见[回放日志](logs/review-notebook.log)。明确非Jupyter kernel，不声称nbformat完整schema验证或Jupyter界面测试。

原创SVG经Inkscape渲染成PNG并实际目视：左图精确呈现单平分两非直径，右图双直径，文字/端点标号清晰、未截断；圆心用O，正文原文标号用F，图注已说明。右图斜直径与正文§5.3正交直径是不同但同类合法例。GitHub最终公式与图像显示仍应由发布验收单独完成。

## 4 审查绑定

- `papers/ancient/euclid-elements-iii4.zh-CN.md`：`f8169a29ca2e74dfc9313e1f52a1ec06728b4e68f7981d3132debb1fd9e04ced`
- `reproduction/euclid-elements-iii4/geometry.py`：`ce5454fbd863e47353225b4b1c90e6828ac818f7ca53fc4dda7da65fafc9be9e`
- `reproduction/euclid-elements-iii4/test_geometry.py`：`926e95cbe60cef6288eac091c6be0c691b165404dc81cede1fe80bddd4d52894`
- `reproduction/euclid-elements-iii4/teaching.zh-CN.ipynb`：`4035a261126a362c552dec66efabd0068ba303dced81f449c7edf6a5dedac7aa`
- `reproduction/euclid-elements-iii4/README.md`：`5072d49aecadc1f5040c66793c17258a0dee3e68d5ef9f2364fbe0fb695514b4`
- `reproduction/euclid-elements-iii4/independent_check.py`：`e0d1ca9da11093404a5291f5fa2edef88fe34ae4550adabc5b5eaad8dfcb110b`

## 5 显示格式修正复核

最终正文第6节将矩阵写法改为两条标量线性方程，避免Markdown处理矩阵换行转义。已逐式复核：两行系数仍为v、w，行列式仍为Δ=v_xw_y−v_yw_x，Δ非零推出e=0；与原数学论证等价，未修改源码、算例或实验结果。以上正文哈希绑定此修正版；GitHub实际显示由发布验收另行核查。
