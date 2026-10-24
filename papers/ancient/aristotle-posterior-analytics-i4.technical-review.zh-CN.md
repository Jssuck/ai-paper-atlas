# 《后分析篇》I.4：独立数学与代码终审

审查范围为[正文](aristotle-posterior-analytics-i4.zh-CN.md)的现代教学重构及[复现](../../reproduction/aristotle-posterior-analytics-i4/README.md)，不是裁定古代术语的唯一语义。源文定位另由来源审查负责。本报告在最终正文修正后绑定内容哈希；任何后续正文或核心代码变化应重新核对。

## 结论与修正

通过本次有限范围审查。发现并修正正文6.4与练习12的“最大/最宽”措辞为**按包含关系的极大合格候选**，避免多个不可比较候选被误称最大元；第8节明确输出不认证首要解释主项。生产算法没有发现需要修复的错误。

## 逐项核查

1. 对象—时间全称式使用同一x、t，允许主项随时变化；时态覆盖与所有可能世界的模态必然性明确分开。
2. 违例等价于某位置主项真且谓项假，最低置位恢复的对象/时间与time-major编码一致。
3. 正文(a,b,c)两时刻案例用位图110011、010011独立执行，返回(c,t1)。
4. 空主项在全称检查中空真；候选类检查另排除空类，不以通过产生存在事实。
5. per se两个定义包含方向不等同类包含；三角形含线条不是三角形属于线的子类。
6. 第三种per se为主体声明，不认证查询中任意属性；第四种原因声明不由两列表相等生成。
7. 正整数奇偶以带余除法说明互斥与覆盖；必要择一不推出两个分支各自全称成立。
8. relative_partition只约束属内位置；属外双真不影响结果。空属通过仅为现代空真，不是历史存在论结论。
9. broadest_adequate输出所有非空合格极大类，保留同外延不同名及不可比较候选，不任意选择唯一对象。
10. 缺少更宽类会改变候选；极大外延候选不等于per se或first解释关系，正文与README都明确限制。
11. 三角形角和教学证明明确欧氏背景、非退化与平行线性质，没有使用等腰条件，不声称跨几何体系有效。
12. 必要结论不能一般倒推所有前提必要，正文保留科学解释与纯逻辑后承的差别。
13. 生产与独立测试使用unittest断言方法或显式RuntimeError；-O/-OO不删除检查。程序不依赖外部服务或个人数据。
14. 手算、附件规模和结果文件一致，有限枚举没有被称为一般定理或完整古代哲学复现。

## 实际运行证据

独立重新运行生产24项测试，在normal、-O、-OO均通过；生产枚举三模式均返回4096时态表对、512属内分割（216有效）、4096候选类组合，oracle差异0。

另写[独立检查源码](../../reproduction/aristotle-posterior-analytics-i4/audit/independent_check.py)，不调用生产exhaustive.run：用布尔元组重新编码两对象三时刻，检查4096表对；四对象分割检查4096组合（1296有效）；两对象四个有名候选类检查1024组合。还覆盖正文案例、零宽/空属、同外延与不可比、外部声明非证据、非法输入。共8项独立测试，在normal、-O、-OO均实际通过。枚举与边界测试都只是声明规模的证据。

运行命令（在复现目录）：

```sh
python audit/independent_check.py
python -O audit/independent_check.py
python -OO audit/independent_check.py
python -m unittest -v test_model
python -O -m unittest -v test_model
python -OO -m unittest -v test_model
python exhaustive.py
python -O exhaustive.py
python -OO exhaustive.py
```

[独立正常日志](../../reproduction/aristotle-posterior-analytics-i4/audit/checks-normal.log) · [独立-O日志](../../reproduction/aristotle-posterior-analytics-i4/audit/checks-O.log) · [独立-OO日志](../../reproduction/aristotle-posterior-analytics-i4/audit/checks-OO.log) · [环境](../../reproduction/aristotle-posterior-analytics-i4/audit/environment.json)。同目录production-rerun与enumeration-rerun三模式日志保存重新运行生产检查的原始输出。

## 最终内容绑定（SHA-256）

发布显示复核后，两条公式仅将间距命令改为quad、函数名字体改为mathrm；逐式核对量词、蕴涵、整数域和异或均未变。更新正文绑定；复现README的对象数、时刻数和位序乘法表达式另以代码格式包裹，防止星号被解析为斜体；数值、索引顺序及意义未变。核心代码与测试源码哈希仍一致，既有真实运行日志不作改写。

- `papers/ancient/aristotle-posterior-analytics-i4.zh-CN.md`：`17a0d3d86706976dd44c36c24a944068352a6e2f3cb55b84eec6c6c813082542`
- `reproduction/aristotle-posterior-analytics-i4/model.py`：`e735c6ce863e7b9d29c5895499f1d12c7918d44bf4d7262af14f0f27d6e7217a`
- `reproduction/aristotle-posterior-analytics-i4/exhaustive.py`：`39dff2895a796ee7666a915853b9975386add823aae2945b135628637bc5aa1b`
- `reproduction/aristotle-posterior-analytics-i4/test_model.py`：`4b85445c1d99775eef208e3993e4d7e00c025567b15eb6c1fef082b6ac206acc`
- `reproduction/aristotle-posterior-analytics-i4/README.md`：`f6a7928352d613bdc6a27f389785d67472e5bcf583a93396e3e729f2e234b041`
- `reproduction/aristotle-posterior-analytics-i4/audit/independent_check.py`：`b82a8478aea27bb3ad917d068a8e3c3dd2d19c692daa38fb366ef9668afe6bd5`

上述通过不替代实际GitHub数学渲染和远端内容核验，后两项由发布验证独立完成。
