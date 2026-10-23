# I.44 独立数学与代码核验

## 结论和边界

对本次声明的现代二值教学模型，数学推导与实现一致，未发现需要修正的数学或代码错误。本核验不裁决古代能力／科学命题的真实语义，不认证对话双方的同意，也不把有限模型核验视为一般数学证明。来源与章界由独立来源审查处理。

## 数学逐项复核

1. 开头桥为非P蕴涵非S，在经典二值语义中等价于S蕴涵P。从桥与非P推出非S有效；删桥后P假、S真是反模型。反向P蕴涵S不能代替原桥，仍有同一反模型。
2. 若Γ与H没有共同模型，则每个Γ模型都否定H；反过来，若每个Γ模型否定H，就没有Γ与H的共同模型。这是一项对任意赋值的语义论证，不依赖程序的两原子限制。
3. Γ本身无模型时蕴涵空真。代码允许这种情况，正文和README均揭示其不能构成关于H的独立可靠反驳。临时H撤除不等于背景Γ也撤除。
4. 从假设非C导出矛盾先得到双重否定C，经典语义再得到C；正文不把该步无条件推广到其他逻辑。
5. 平方奇偶引理对任意整数成立：奇数写成2k+1，其平方仍奇。最简正分数的平方等式使分子分母皆偶，与互素条件矛盾。最简条件、正分母和几何桥梁明确；原章简略例子和本文补证分开。

## 实现检查

作者采用真值行集合。独立检查改用整数位掩码作预期值，并另行构造双背景情形，而非仅重复作者的单背景实验。

- 4096组前提一／前提二／结论真值集合，逐个比对蕴涵和首个反赋值。
- 4096组背景／假设／结论证书，检查精确否定和内部无模型两条件；81组通过。
- 4096组双背景／临时假设，核对撤除结论与内层不相容的等价。
- 空原子表仍有一个空赋值，空前提和不一致前提分开；一次性生成器冻结后可重复使用。
- 布尔值与浮点行号拒绝，先检查所有前提再求交，不因前一个前提为空而跳过后续非法输入。
- 作用域标签只核验调用者提供的标签不重复，不能认证隐藏推导或来源。对同公式改名、背景本身矛盾的测试证实并揭示这一限制。
- 以除法余数独立核验−512至512的1025整数奇偶；用欧几里得算法独立复算1至64的4096分数对，其中2519互素，平方等式无解。仍不据此声称无界算术定理已由实验证明。

## 真实运行

独立10项测试在正常、-O、-OO模式全部通过，日志包含实际命令和原始输出：

- [正常模式](logs/independent-normal.txt)
- [优化模式](logs/independent-optimized.txt)
- [双优化模式](logs/independent-double-optimized.txt)

另实际复跑作者18项正常模式测试及实验，统计一致。作者三模式日志也逐项检查。独立脚本使用unittest断言方法及显式退出，不依赖被优化移除的assert语句。独立源码为[independent_check.py](independent_check.py)，环境沿用[环境记录](logs/environment.txt)。

程序核验的是有限语义条件，不是逐行三段论推导证书。4096等数值属于不同实验口径，不应相加包装成更多历史结论或一般数学保证。

## 最终文件绑定

以下SHA-256绑定本次实际核验的正文、实现、说明和日志。后续任一文件变更均需重新审查相关内容并更新绑定；本表不包含自身，避免循环。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-i44.zh-CN.md`|`b9f2ed7bb0eb2e0fb48719f16f675df7fb6de8d9075c5f1b1ee1d870b4d8731b`|
|`reproduction/aristotle-prior-analytics-i44/model.py`|`824b92e93be3513a8228224ab3e5afa2102a9e9253eb0deddd6d9b1576c6d9c6`|
|`reproduction/aristotle-prior-analytics-i44/test_model.py`|`0f945cc04d0475ff7b0c726fd86965af64ee90f5f81ea4204b757f9153968b9f`|
|`reproduction/aristotle-prior-analytics-i44/run_experiment.py`|`87ddae0f5bd6121595f024c946c6b318e22c9c8337bc96a336b9f432c27e9862`|
|`reproduction/aristotle-prior-analytics-i44/independent_check.py`|`1153e7e5bebd51a8288d33f95cd9dbbe9dd1a68e0295fecb33203b49e195ff7f`|
|`reproduction/aristotle-prior-analytics-i44/README.md`|`91fa621f80a46647e25657e0375251c3262e70fbd6e69aaad9b63eb1a14bcd81`|
|`reproduction/aristotle-prior-analytics-i44/logs/environment.txt`|`f68d22aa3ab6962429cbb751e07349f14efe8678c940d467e0379b2fd47e9e99`|
|`reproduction/aristotle-prior-analytics-i44/logs/experiment-double-optimized.txt`|`2c2ffe63d6abeb55a2309402385df533dec45cec49071d5924a1342c682d05d7`|
|`reproduction/aristotle-prior-analytics-i44/logs/experiment-normal.txt`|`2c2ffe63d6abeb55a2309402385df533dec45cec49071d5924a1342c682d05d7`|
|`reproduction/aristotle-prior-analytics-i44/logs/experiment-optimized.txt`|`2c2ffe63d6abeb55a2309402385df533dec45cec49071d5924a1342c682d05d7`|
|`reproduction/aristotle-prior-analytics-i44/logs/independent-double-optimized.txt`|`d82c0791b63d85576c6f55bb310af7d4e369a47574733a68a5072e3b644d0448`|
|`reproduction/aristotle-prior-analytics-i44/logs/independent-normal.txt`|`f7e3fd5bf8e2c4552d4824eb68f1d879a032a0f7ece49cf2120269b03c21b365`|
|`reproduction/aristotle-prior-analytics-i44/logs/independent-optimized.txt`|`c1db63c008e608d62fd61d96e6378285651499375a8b85993b63a2b05458786e`|
|`reproduction/aristotle-prior-analytics-i44/logs/tests-double-optimized.txt`|`777f093b54441752a4073fd6d3fe35e2049391ff05b4f28f6dd43063881feea7`|
|`reproduction/aristotle-prior-analytics-i44/logs/tests-normal.txt`|`777f093b54441752a4073fd6d3fe35e2049391ff05b4f28f6dd43063881feea7`|
|`reproduction/aristotle-prior-analytics-i44/logs/tests-optimized.txt`|`777f093b54441752a4073fd6d3fe35e2049391ff05b4f28f6dd43063881feea7`|
