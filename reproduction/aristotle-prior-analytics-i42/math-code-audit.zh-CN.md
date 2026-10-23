# I.42：独立数学与代码核验

## 结论与范围

在正文明确声明的一元集合语义、三格布局和两种存在政策内，独立核验通过。未发现需要改动作者源码的数学或实现错误。此结论不认证前提的现实真实性、唯一古代语义、自然语言解析或完整证明助手。

核验分别检查一般证明与有限运行，不能用测试通过替代任意论域的论证。

## 一般数学论证

1. 第二格的两个端项可分别复制到不相交的对象集合，保持各自与中项M的成员关系。A/E的违例存在性与I/O的见证存在性均保留。若S为空，且需要反驳A，可加一个独立S对象，按小前提A/E决定是否进M，不进P。因此两前提可真而端项肯定结论假。各项非空时，复制保持非空；允许空项时正文给出了补点分支。这一论证不允许额外背景如S=P被偷偷加入。
2. 第三格所有前提都以M为主项，在M外增加S非P对象可破坏A，增加S且P对象可破坏E，不影响前提或已有见证。
3. 七类型压缩保持四类命题真值和各项非空性。每个出现的非零S/M/P类型留一个代表；若全空，仅保留一个000对象使论域非空。对象数量变化不影响此受限语言，但会影响带数量约束、关系或模态的扩展语言，不能无条件推广。
4. 第五节第一格AAA、第二格EAE的逐对象证明成立；局部大项/中项随目标变化。E前提换位后的第一格记录是另一表示，不与原第二格标签矛盾。
5. 128支持集和全项非空109支持集的计数正确。有效式按政策各格4或6，包含弱化式，不冒充统一传统基本式数量。候选格是存在有效路线的集合，不是给定前提的有效性证书。

## 独立实现与真实实跑

[independent_check.py](independent_check.py)不调用作者命题求值函数来生成期望值，另写逐对象all/any语义、格布局和成员类型生成器。它对每一个式比较反模型有无，并用独立求值复核作者返回的见证。另检查四对象模型的类型压缩、重复成员类型与非连续对象编号、混合证明、存在政策和异常输入。

每种 normal、-O、-OO 模式：

- 独立8项测试全部通过；重跑作者16项测试全部通过。
- 独立45504次模型—式检查，128与109规范模型计数一致。
- 4096种四对象三项赋值的压缩检查，共147456次命题真值比较。
- 混合证明4096种赋值，其中125种前提真，后果无失败。
- 分类器只判断布局而不判断有效性的边界明确，错误第一格EEE仍可获得格标签，但反模型使其结论失败。
- 非法格、类型、政策、空论域、越域成员、布尔/负对象编号与不合法节点均被拒绝；一次性生成器被稳定冻结。校验不依赖优化时消失的assert。

实跑命令（在本目录）：

```bash
python3 independent_check.py
python3 -O independent_check.py
python3 -OO independent_check.py
python3 -m unittest -v test_model
python3 -O -m unittest -v test_model
python3 -OO -m unittest -v test_model
```

证据：[独立normal](logs/independent-normal.txt)、[独立-O](logs/independent-O.txt)、[独立-OO](logs/independent-OO.txt)；[作者重跑normal](logs/review-author-normal.txt)、[作者重跑-O](logs/review-author-O.txt)、[作者重跑-OO](logs/review-author-OO.txt)。这些是真实运行记录，不是对任意数学定理或全部历史解释的实验认证。

## 审查绑定

以下SHA-256绑定审查时实际读取的正文、作者文件及运行证据。后续内容变动须复核；本审查不自我哈希。

|文件|SHA-256|
|---|---|
|papers/ancient/aristotle-prior-analytics-i42.zh-CN.md|d8c568c871214ae7153702306cae4fa2faaf6e65b7c9328a9d8a2c28adddeb6c|
|reproduction/aristotle-prior-analytics-i42/README.md|97b9e359f1aa3b8001841ca5c5067a4d8d8fe0b18cfc84900447796f33e09080|
|reproduction/aristotle-prior-analytics-i42/independent_check.py|0ed7ffd0c4d52fcbeadaece651c073dbd6ec7c1e9c344ddd5d6c526de306f8ed|
|reproduction/aristotle-prior-analytics-i42/logs/environment.txt|3302d391167e43861a9b18f0792951c572d0783c249e23e7afa7ebd93d4d40fd|
|reproduction/aristotle-prior-analytics-i42/logs/experiment-O.txt|2ad95f9deb50faece797416064ea5ed227aa5e188bc5209e53474480b4b9a3b6|
|reproduction/aristotle-prior-analytics-i42/logs/experiment-OO.txt|90fd344608ffa37cb616c93bc1d2816a3be73d98aaab9860a58bfa05245de544|
|reproduction/aristotle-prior-analytics-i42/logs/experiment-normal.txt|36b8026dcd5006daf1b6e0d6328b6188d22e169635101fdadca9b7ab1ca18b91|
|reproduction/aristotle-prior-analytics-i42/logs/independent-O.txt|e8352751ad7aeacfabab887e02e5452df5287c695dfd4dc6bf20b11a7e63de47|
|reproduction/aristotle-prior-analytics-i42/logs/independent-OO.txt|0bc9cd0711fc3e7726d4f0b48418b66849cb241bd744b600906ee1853d5ba1ab|
|reproduction/aristotle-prior-analytics-i42/logs/independent-normal.txt|97a0250839b6c58d503e35da159252b25138d92ff7143b677bd2721d8044aa30|
|reproduction/aristotle-prior-analytics-i42/logs/review-author-O.txt|1366cb818234af6027810c8c9405bb98764a0269712d6cd34c6e3211fd139fb3|
|reproduction/aristotle-prior-analytics-i42/logs/review-author-OO.txt|7d548f3d2e45d663f514ef05fd66dfb8fc36d6a7ab703c03ba07027f16b521ca|
|reproduction/aristotle-prior-analytics-i42/logs/review-author-normal.txt|751a7b4925c0a0cd3143bf009ed34eb96c94a59aabdf3eb1f5efcedaa7532fed|
|reproduction/aristotle-prior-analytics-i42/logs/tests-O.txt|a4c61d73663321348ca1c1ce22e7ba7a234c95a8bbfb1f1905c5ecd171e0a113|
|reproduction/aristotle-prior-analytics-i42/logs/tests-OO.txt|4daee8c57b726ac3d2752caee35cfb5fc5671e6627df1048d4b7dc7f129c7481|
|reproduction/aristotle-prior-analytics-i42/logs/tests-normal.txt|d0834a71040e5dbeda685457c012d92fd9d39428502bee41d7d810c274b6e5ca|
|reproduction/aristotle-prior-analytics-i42/model.py|149da58e3235366b87c098a55d8157c828da157407776d52782b29f3f394e3ee|
|reproduction/aristotle-prior-analytics-i42/run_experiment.py|1991b04c257a4cc25d85de05d5847f8fde0279b0eea289fdd19af9de7e3e02a8|
|reproduction/aristotle-prior-analytics-i42/test_model.py|93d4057025b8a78a37a28b903b2dd66fa9e0b6eee2eb1f3d65a1c0fbf1cdc36c|
