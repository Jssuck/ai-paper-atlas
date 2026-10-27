# I.19 最小教学复现：大角、大边与三分排除

本目录只覆盖 Euclid I.19 的现代教学核验，不是《几何原本》的完整形式化，也不把有限样例当成一般证明。原文的几何依赖 I.5 与 I.18 仍须阅读和重建；代码不能凭一个命题标签替代证明。

## 运行

无需安装依赖，不访问网络，在本目录执行：

```sh
python run_all.py
```

运行器以实际解释器路径执行普通、`-O`、`-OO` 三模式的测试和样例，再生成和执行 Notebook。八条真实命令、时间及退出码见 [run-summary.json](run-summary.json)，环境见 [environment.json](environment.json)，原始输出在 [logs/](logs/)。本次每模式34测试、87正证书、12非法输入全部通过，优化模式结果相同；Notebook六个代码单元采用 Python 标准库 `compile/exec` 顺序共享命名空间执行，**未使用 Jupyter kernel**，也不声称浏览器渲染过 Notebook。

## 三层模型，不相互冒充

1. **几何输入与独立量值核验**：`inspect_triangle` 接受非共线三点。坐标只能是整数（不含布尔）或有理数字符串，禁止浮点和非有限输入。普通角限定在零与平角之间，通过向量的点积和叉积比较余切；判断过程不取浮点平方根或反三角函数。
2. **历史论证的关系摘要**：`build_certificate` 仅接受 β=ABC 大于 γ=BCA 的题设。记录“若 AC=AB，则 I.5 迫使 β=γ”和“若 AC<AB，则交换标签后的 I.18 迫使 β<γ”两个被排除分支，余下 AC>AB。记录是读者检查依赖的摘要，不是一个内置古代定理证明器。
3. **抽象假设实验**：`infer_side` 在有限关系标签表中删除与已知大角矛盾的分支。`total=False` 加入不可比较标签，说明去掉全序后不能从“非等且非小”推出“大”。这是假设分析，不声称普通线段事实上不可比较。

`verify_certificate` 重建规范记录并逐字符比较规范 JSON；区分 `true`、`1`、`1.0`，拒绝浮点、元组、额外键、缺键与篡改。它是教学证书一致性检查器，重建证书不能算独立的定理证明。独立测试另外直接验证代数恒等式、关系排序及非法输入。

## 文件导航

- [geometry.py](geometry.py)：有理输入、角比较、证书、有限关系消去。
- [cases.py](cases.py)：87个题设成立输入与12个非法/不满足题设输入。
- [test_geometry.py](test_geometry.py)：34项测试，含正负角布局、平移缩放、类型混淆和输入绑定。
- [run_examples.py](run_examples.py)：三模式一致的样例及假设删除结果。
- [WALKTHROUGH.md](WALKTHROUGH.md)：符号、手算例、恒等式和方法边界。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)：六格已执行教学笔记；[verify_notebook.py](verify_notebook.py)说明实际执行方式。
- [SHA256SUMS.json](SHA256SUMS.json)：本目录文件清单（不自含，不含缓存）；独立审查加入后须刷新。

## 证据边界

87份证书只覆盖选定有理输入，不能据此证明任意实坐标或所有古代几何模型。精确算术避免舍入误判，但并不消除建模假设。代数恒等式是现代欧氏坐标事实，不是原文的三分反证。浮点近似或正弦定理均未参与判决。对应[深读正文](../../papers/ancient/euclid-elements-i19.zh-CN.md)另述一般证明与原典证据。
