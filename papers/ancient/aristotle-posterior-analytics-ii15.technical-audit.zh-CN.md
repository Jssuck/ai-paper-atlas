# 《后分析篇》II.15：独立技术终审

审查日期：2026-10-26。审查者独立于正文与复现作者；检查完整正文、源码、测试、Notebook及已保存日志，并在隔离副本真实复跑，不改写发布目录原日志。

## 1. 绑定对象

|对象|完整 SHA256|
|---|---|
|[最终完整正文](aristotle-posterior-analytics-ii15.zh-CN.md)|`2c8e2819d49d307ae912f83ce8a36ad4140248ec0edcc978eceaeb0b755624c8`|
|[model.py](../../reproduction/aristotle-posterior-analytics-ii15/model.py)|`cd0c8690ae00839113afaa1bb52360d2035750d27e4e48ed2b6902c1c4ba128f`|
|[tutorial.ipynb](../../reproduction/aristotle-posterior-analytics-ii15/tutorial.ipynb)|`843678fdbc829235e3189456ce9559462a0bd2d7ea44321eedf7dbfe5cd73ef3`|

上述正文包括所有章节与练习，而非只哈希公式片段。发布前若正文有任何字节修订，本绑定须重新审查更新。

## 2. 数学与解释检查

- 共享中项的两次全称推导正确；正文明确每个主体仍须自己的小前提，若结论性质不同仍需相应大前提。没有由中项同名直接跳到结论。
- 集合手算例和前提失败但结论仍真的反例成立；空类全称真不被当作存在证据。
- 在有效且一致的登记表上，标识相等推出函数值相等；属同不推出同项。正文把这套等价关系明标为现代教学重构，未归给原作者作为互斥完备分类。
- 种性质不能上推全属再下传其他种，所给两元素反例有效。
- 条件链合成证明与任意有限长度的归纳证明成立；L假、W假、F真正确反驳逆向。形式有效没有被用来认证古代月亏、天气、水文前提。
- 分类、解释与蕴涵的区分保留。程序的可达性不是因果识别；循环拒绝只是本证书规范，不驳倒动态反馈系统。

## 3. 源码和真实执行

独立在副本执行 `python run_all.py`，五个子进程退出码均为0：

|操作|独立复跑结果|发布证据|
|---|---|---|
|`python -m unittest -v`|20个测试方法通过|[tests.log](../../reproduction/aristotle-posterior-analytics-ii15/logs/tests.log)|
|`python -O -m unittest -v`|20个测试方法通过|[tests-optimized.log](../../reproduction/aristotle-posterior-analytics-ii15/logs/tests-optimized.log)|
|`python -OO -m unittest -v`|20个测试方法通过|[tests-double-optimized.log](../../reproduction/aristotle-posterior-analytics-ii15/logs/tests-double-optimized.log)|
|`python model.py`|exact及包容性属同True；三对generic；同名异义unrelated；链正向True、逆向及自身False|[demo.log](../../reproduction/aristotle-posterior-analytics-ii15/logs/demo.log)|
|`python run_notebook.py`|3个代码单元顺序执行成功|[notebook-exec.log](../../reproduction/aristotle-posterior-analytics-ii15/logs/notebook-exec.log)|

测试计数为方法数；三对历史现象在一个方法的subTest中，并未夸大为额外测试方法。复跑耗时与原日志可以不同，不要求时间戳逐字相等。发布[SHA256清单](../../reproduction/aristotle-posterior-analytics-ii15/sha256.json)的12个文件逐字哈希全部吻合。

`Problem.validate`核域、所需条件和标识；同key不同声明被拒绝。`classify`的generic分支实际意为同属但非exact，`shares_genus`保留exact也属同的包容关系。`Chain`检查未知节点、重复节点、环和人为level方向，再用搜索检查可达性。无路径返回False，未知节点抛出错误；两者不混同。

Notebook cell IDs唯一，运行器明确使用标准库`exec`而非Jupyter内核；没有将内核、交互前端或magic兼容性列为已验证。普通、`-O`及`-OO`三模式均通过，必要输入检查使用显式异常而不是会被`-O`移除的assert。

## 4. 保留的边界及结论

本程序适用于有效结构化教学输入，不是任意不可信Python对象的安全验证器；登记的属、类型、条件和level仍由人负责。它不验证经验真假、同义词发现或真正因果方向。递归环检查与逐边扫描适合小图，不承诺无限深图或大型图规模性能。正文的一般证明由逻辑论证支持，不由20个测试代替。

**结论：通过本次有限教学范围的技术终审。** 未发现阻断发布的数学、代码或日志不一致；没有宣称完成现代物理实验、自然因果理论或Jupyter内核复现。后续修改必须重新绑定完整正文与受影响附件。
