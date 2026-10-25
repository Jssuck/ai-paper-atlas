# I.34 最小教学复现：候选发现与证书检查

对应《后分析篇》I.34，89b10–20。本目录是原创现代有限模型，不是原文算法、真实天文实验、心理速度测量或完整复现。古代三例是解释中项的发现；代码只检查给定外延关系，不能认证因果、必然性或知识。

## 定义与一般推导

`verify_middle(U,A,B,C)`分别检查主体非空、C⊆B、B⊆A、C⊆A。证书要求前三项成立。取任意x∈C，先得x∈B，再得x∈A，故C⊆A；这是适用于任意集合的一般证明。非空C是本例关于实例主体的显式政策，不是全称命题自身的存在含义。空C的两个蕴涵与结论可真而证书拒绝；空B不能覆盖非空C。域外元素抛出ValueError。

`eligible_middles`只筛选调用者提供的候选字典，不搜索所有语言表达、不排名、不输出唯一原因、不测量“瞬间”。`sun_lit`和`singleton_fit`同时通过；后者只是单例拟合，暴露外延检查不能识别真解释。省略合格候选会返回空列表，不能据此断言无解释。扩大域或修改外延必须重新验证。

从C⊆A和B⊆A反推C⊆B无效：令A={moon,panel}，B={panel}，C={moon}即可。社会例也不能升格为普遍律：交谈者未必借钱，共同敌人不保证友谊。它们是教学反模型，不是对原文具体人物事件作历史否定。

## 运行

Python 3，全部依赖为标准库，不安装软件。进入本目录：

```sh
python run_all.py
```

该命令真实运行并保存：

```sh
python model.py
python -m unittest -v test_model
python -O -m unittest -v test_model
python -OO -m unittest -v test_model
python run_notebook.py
```

[源码](model.py) · [测试](test_model.py) · [Notebook](tutorial.ipynb) · [顺序执行器](run_notebook.py) · [批运行器](run_all.py) · [环境](environment.json) · [SHA256清单](sha256.json)

[演示日志](logs/demo.log) · [普通测试](logs/tests.log) · [-O测试](logs/tests-optimized.log) · [-OO测试](logs/tests-double-optimized.log) · [Notebook执行日志](logs/notebook.log)

Notebook已按序执行四个纯Python代码单元并保存输出，执行器为CPython标准库exec，**不是Jupyter内核**；不支持magic、display协议或widgets。已读取安装技能；其helper/附属资源未能取得，因此沿用既有Notebook结构改写，而未安装第三方内容。

三对象域穷举8³=512组三集合；C⊆B⊆A且C非空共4³−3³=37个证书，均有C⊆A。计数理由：每个元素可在C、B\C、A\B、U\A四种互斥层中；C空时只剩三种。穷举不能替代上方一般证明，也不能证明古代全部认识论。14项unittest在普通、-O及-OO模式各自实际执行，断言采用unittest方法，不会被优化删除。实际证据以附带日志和环境为准。

sha256.json排除自身以避免递归哈希；run_all.py重新执行会刷新日志中的真实耗时及相应摘要。运行时间不是认知速度指标。
