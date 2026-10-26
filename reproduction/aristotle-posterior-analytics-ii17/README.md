# Posterior Analytics II.17：范围、同名与多条解释路径的最小模型

配套[中文深读](../../papers/ancient/aristotle-posterior-analytics-ii17.zh-CN.md)，原文范围99a1–99b8。这里全部是原创教学重构：Python没有运行亚里士多德的算法，也没有检验古代植物、动物长寿学说。集合外延相同不等于定义相同，更不证明互为原因。

## 文件与复跑

只需 Python 3 标准库，不安装第三方依赖，不访问网络。进入本目录执行：

```bash
python run_all.py
```

它顺序运行并保存真实 stdout/stderr 和退出码：

```bash
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python model.py
python run_notebook.py
```

- [model.py](model.py)：有限集合模型与正有理数比例演示。
- [test_model.py](test_model.py)：22项 `unittest` 测试；断言使用 `self.assert*`，不是会被优化删除的裸 `assert`。
- [run_all.py](run_all.py)：逐项子进程执行、保存日志、环境与SHA256清单；失败立即停止。
- [run_notebook.py](run_notebook.py)与[tutorial.ipynb](tutorial.ipynb)：5个普通Python代码单元，稳定唯一cell IDs。**实际使用标准库exec按顺序执行，不是Jupyter内核执行**；文件虽可由Jupyter打开，本次没有声称执行内核、widget或魔术命令。
- [environment.json](environment.json)：真实Python版本、平台、时间与依赖说明。
- [sha256.json](sha256.json)：除清单自身及缓存外所有配套文件的字节校验值。

## 模型与预期结果

### 1. 类别分别较窄不妨碍合起来等范围

设上位范围B={0,1}，两个类别D1={0}、D2={1}。两者各自严格小于B，但其并集等于B。改B为{0,1,2}而仍只列这两类，便缺少2。模型不要求类别互斥，也不会把“列举了几个类别”误当成“已穷尽所有类别”。空类别、空论域单独测试；对空族，Python的全称判断为真，不意味着现实中存在相应自然种类。

三元素论域下B、D1、D2共512种赋值；只在D1⊆B、D2⊆B时检查覆盖。64种并集恰为B，18种还满足两个类别各自严格小于B。64=4³：每个元素可以不在B，或只在D1、只在D2、两者均在。18=4³−2×3³+2³：排除D1=B或D2=B，再加回两者都等于B的情形。这个独立计数能帮助检查枚举程序。

### 2. 同一结果可有不同中项路径

模型前提D⊆B⊆A和E⊆C⊆A，结论D∪E⊆A。取A={0,1}、B=D={0}、C=E={1}，两路径均成立，但A既不包含于B，也不包含于C。知道属于A不足以决定属于哪一中项；这不等于已经证实B、C是真实原因，它们的解释角色仍需外部论证。

三元素论域五集合共32768种赋值，1000种满足前提，结论反例0，657种满足前提却不满足A⊆B。逐元素计数：元素不在A时只有1种合格配置；在A时(B,D)和(C,E)各有3种，故总数(1+3×3)³=1000。另加A⊆B仅剩7³=343种，差为657。

一般证明不靠枚举：任取x∈D∪E。若x∈D，经D⊆B及B⊆A得x∈A；若x∈E，经E⊆C及C⊆A也得x∈A。两种情况覆盖并集，故包含成立。有限运行只核验这个形式化的有限实例。

### 3. 外延不是解释方向

`extension_equivalence` 只检查集合是否相等；返回结果中的 `causal_direction`、`same_definition` 字段固定为 `undetermined`。这是明确的证据边界，不是程序成功推断了因果不可识别的一般统计定理。本章99a30之后关于A范围大于B的争议性段落，不能机械改写成“所有真正原因的外延必须严格小于结果”的普遍公理；模型特别保留A=B时包含链仍成立的测试。

### 4. 比例更项的正有理数演示

取a=2、b=4、c=3、d=6，a/b=c/d且a/c=b/d。一般正有理数证明是由a/b=c/d得ad=bc，再除以正数cd得a/c=b/d。代码使用精确`Fraction`，不靠浮点近似；对零和负值拒绝，是本教学论域的约束，不主张负数情形都不成立。还枚举1至5的四元整数，共625组，检查前提成立时结论成立。原文同时谈数与线段；这里不把有理数演示当作古希腊一般量比例论或无理线段的复现，也不从同一算式推出对象类型相同。

## 本次实际证据

- [普通测试日志](logs/tests.log)：22项通过，退出0。
- [-O测试日志](logs/tests-optimized.log)：22项通过，退出0。
- [-OO测试日志](logs/tests-double-optimized.log)：22项通过，退出0。
- [模型实跑日志](logs/demo.log)：上述有限计数、反例和比例输出，退出0。
- [Notebook执行日志](logs/notebook-exec.log)：5个代码单元执行成功，退出0。

没有数据集、训练基线或现代实验指标；测试数与有限模型数量不是科学解释准确率。这里不声称完整复现原文、穷尽历史解释争论或验证古代自然科学。
