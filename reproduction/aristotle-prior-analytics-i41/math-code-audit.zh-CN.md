# I.41 数学与代码独立核验

## 结论与修正

独立检查正文第4–7节、全部数学练习和附件实现，**在所声明的现代外延/具名类族语义内通过**。未将此结论扩大为古代唯一解释或无限模型的实验验证。

发现并修正一处教学叙述风险：第6节先声明B包含于A，第三种情形却只给弱条件W。现明确“撤去上述B包含于A的声明”再讨论仅审查批次，避免读者误以为保留强前提时仍不能得到其已声明的内容。此修改已复读；没有发现需改作者源码的问题。

## 一般证明复核

- 全称链：任意C对象经C⊆B和B⊆A两步进入A；空C不提供存在见证。
- 特称链：同一C/B见证经强大前提进入A，不能升级为所有C。
- 弱条件恰当等价于合格候选类并集U包含于A，两个方向均有任意对象证明。
- 强条件推出弱条件；固定B、F后，对所有A强弱等价当且仅当U=B。必要性取A=U，若覆盖不足，漏掉的B对象反驳强条件。
- 若F是全幂集、含B或合格类覆盖B，强弱等价；文章没有把它错误说成必然不等价。
- 第5.2、5.3和5.5各反模型逐对象复核，均满足前提并具有声明的失败结论。第5.3成对模型正确区分“不保证肯定”与“证明否定”。

F是正文明确引入的现代教学参数。数学可行性不能证明古代语言实际采用这个类别库机制；来源判断见独立来源审查。图示角色未由程序复现，也未将所有视觉推理判为无效。

## 独立实现与真实执行

[独立审查脚本](independent_audit.py)使用整数位掩码逐对象真值表生成期望值，不调用作者的powerset/families枚举器，也不复用作者的集合包含方法生成期望值；作者Model只作为被测对象。正常及优化模式均有显式失败检查，unittest断言不会因优化而失效。

```bash
python3 independent_audit.py
python3 -O independent_audit.py
python3 -OO independent_audit.py
```

|模式|真实日志|结果|
|---|---|---|
|普通|[日志](logs/independent-normal.txt)|10项测试通过，退出码0|
|`-O`|[日志](logs/independent-O.txt)|10项测试通过，退出码0|
|`-OO`|[日志](logs/independent-OO.txt)|10项测试通过，退出码0|

每种模式独立核查16656个(A,B,F)模型、584组(A,B,C)，再对2120组(B,F)核验“对所有A等价”与覆盖的充要关系。得到弱真强假2602、覆盖10884、全称链84、特称链103、特称但非全称32，均与作者日志/README一致。模式之间是重复验证，不累加成更多不同模型。

测试包括空外延、空F、重复类别、一次性生成器冻结后重复调用、输入对象变动不反向改变模型、非连续对象编号、见证编号0、布尔/浮点/字符串/负数/非可迭代输入拒绝、越域拒绝，以及全部584组中所有不满足前提的链调用必须抛异常。程序使用显式TypeError/ValueError，不以assert充当输入检查。

有限枚举不替代以上一般证明。审查没有检验任意大输入性能、自然语言解析、现实样本覆盖、几何证明器或古代唯一语义。没有新增依赖。

## 验收绑定

以下SHA-256绑定本次实际复读的正文、根目录新条目、作者说明/源码/真实日志与独立脚本/日志；本审查文件自身不作递归绑定。若这些文件以后变化，应重新审查受影响部分。

|文件（仓库路径）|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-i41.zh-CN.md`|`bb601dc202c5bd848bb9597241b8eebfce88dd5b64f203bacf2036cf78d5dcb7`|
|`README.md`|`7e8dc9ef1c0d166c728118010277e59abd4166d2c425ab550934fe0138e3be1c`|
|`reproduction/aristotle-prior-analytics-i41/model.py`|`d0a76ac206c8059381cf9ac3cba2f4a6ff5aa5c689a9cac46aecc0cbd7e04612`|
|`reproduction/aristotle-prior-analytics-i41/test_model.py`|`59ea9d8f2bd45c4a2ac66f899cbc669aff9bcc1282ecd5415e3fa16c5b182c15`|
|`reproduction/aristotle-prior-analytics-i41/run_experiment.py`|`9ec84f4b9809fee354c68004798b0c361b3f8dded028dba4ad95a7fd14414d74`|
|`reproduction/aristotle-prior-analytics-i41/independent_audit.py`|`baca956f1317cdab68d13e672d0cbbc85365c39acf31dbd8e1fa8671494f9d9f`|
|`reproduction/aristotle-prior-analytics-i41/README.md`|`3c3eafaca96ff46ffead831b873e303b7baef709e714ad7aa6df91e5962592e9`|
|`reproduction/aristotle-prior-analytics-i41/logs/environment.txt`|`c104d030f6271653298d9516cfbb4a17ba453a8b36c0c4cca8c10d77f185ba58`|
|`reproduction/aristotle-prior-analytics-i41/logs/experiment-O.txt`|`a219c01e336cfbc71a6023bef94dd7a3c2b16f250c5460ff469877403cf9e3de`|
|`reproduction/aristotle-prior-analytics-i41/logs/experiment-OO.txt`|`63040d39d722385947c6fd148d5ba97bf49d345e2919e210e06946267a1d5638`|
|`reproduction/aristotle-prior-analytics-i41/logs/experiment-normal.txt`|`0744216bb1b2f6e6006d16c4141040c146e6cf7992af7a2c47dfcfbabe501959`|
|`reproduction/aristotle-prior-analytics-i41/logs/independent-O.txt`|`194f853145640bd7c97895dd926344612ab76fde406b65e4c8423f2e0ecf3a6b`|
|`reproduction/aristotle-prior-analytics-i41/logs/independent-OO.txt`|`079689097f186963ad6ceabf5cb2072dfc3554aba3e7823e82d6f1600ba02559`|
|`reproduction/aristotle-prior-analytics-i41/logs/independent-normal.txt`|`0e1820fb9edc89cac3c6561956b29d2c6350673e901205fe7dab07ac7d7f2ef5`|
|`reproduction/aristotle-prior-analytics-i41/logs/tests-O.txt`|`0818aef18948d1bd582cdb3b27cb22941218609d47f4a57616529c6142ec8935`|
|`reproduction/aristotle-prior-analytics-i41/logs/tests-OO.txt`|`f65bcaa96c24c9c8253e2c4f2f2869667d0699665f12df7436d8e90a9e108f0a`|
|`reproduction/aristotle-prior-analytics-i41/logs/tests-normal.txt`|`2fcd84902119ca5bf31bda1d8db32f70bb7900adf3bc6817ccbfe4b3d3814a88`|
