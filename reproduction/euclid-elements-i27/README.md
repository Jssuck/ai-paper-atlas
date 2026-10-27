# I.27：相等内错角的精确有限核验

[中文精读](../../papers/ancient/euclid-elements-i27.zh-CN.md)的原创教学附件。程序在二维欧氏有理坐标模型中直接计算前提和结论，**不是 I.16 反证的形式化内核，不是全部《几何原本》的复现**；有限样例不能证明一般定理。

## 输入、模型与接口

输入只含 `E,F,A,D` 四个点，每点是二项列表。坐标只接受规范有理数字符串，例如 `"0"`、`"-3"`、`"2/5"`；拒绝数字型、布尔型、非规范 `"2/2"` 以及额外字段。E、F 是横截线上的不同交点；EA 与 FD 是被检验的两条无限直线，A、D 指明各自射线方向。

记 t=F−E、u=A−E、v=D−F。要求 cross(t,u) 与 cross(t,v) 非零异号，保证 A、D 在横截线异侧以及两个角均不退化。程序比较角 AEF 与 EFD 的精确指标：分别为 dot(u,t)/abs(cross(u,t)) 与 dot(−t,v)/abs(cross(−t,v))。这是非退化普通角的余切；保留正、零、负号，避免锐角和钝角被平方混淆。

[geometry.py](geometry.py) 重新计算两射线方向行列式为零、v=−λu 且 λ>0，横截偏移 cross(t,u) 非零。故两条方向平行且不重合的直线不相交。详见[教学推导](WALKTHROUGH.zh-CN.md)。此欧氏坐标证书不检验双曲模型，也不替代原文借 I.16 排除左右交点的证明。

`make_certificate(data)` 只为满足全部前提的输入生成证书。`verify_certificate(expected_input, certificate)` 必须接收调用者独立持有的预期输入；重算整份证书并逐字段、逐类型比较。另一合法输入的证书、真假值冒充整数、额外或缺失字段、篡改计算值一律拒绝。输入 SHA-256 只是内容标识，不是签名，不能代替输入绑定。安全性不覆盖资源耗尽、任意Python对象、自定义映射或形式化算术可信性。

## 实跑

仅 Python 标准库，无第三方安装。在此目录执行：

```sh
python3 run_all.py
```

- [test_geometry.py](test_geometry.py)：29 项测试，在普通、`-O`、`-OO` 三模式均通过；算法不靠可被优化删除的 assert。
- [results.json](results.json)：252 正例 = 7 斜率 × 3 高度 × 3 射线尺度 × 4 相似变换（恒等、90°旋转、反射、有理缩放平移）；并非随机抽样。6 类负例均直接调用生成器并确认抛出 ValueError，而非仅比较空证书。包括同侧相等普通角、异侧不等角、互补非等角、零横截线、零射线、重合直线。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)：6 个代码单元的真实输出。执行器在独立 Python 进程内按顺序共享命名空间，使用标准库 `compile/exec`，**不是 Jupyter kernel**，不声明 nbformat 完整模式验证或浏览器渲染；stderr 合并捕获后存入输出流。已安装技能的本地脚手架路径不存在，故依其结构指引由随附标准库脚本生成，未安装新组件。
- [run-summary.json](run-summary.json)、[environment.json](environment.json)、[logs](logs/)、[notebook-check.json](notebook-check.json) 提供真实命令、退出码、环境和输出。
- [SHA256SUMS.json](SHA256SUMS.json) 标识附件内容；修改后须重跑，不能沿用旧证据。

本核验只覆盖有理坐标输入与声明的模型。它不能凭样例验证“所有无限延长均不相交”；一般不交性来自正文代数推导与原几何证明，而非枚举延长距离。
