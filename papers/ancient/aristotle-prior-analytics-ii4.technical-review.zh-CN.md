# 《前分析篇》II.4：独立数学与代码核验

核验日期：2026-10-23。审查对象为原创集合语义教学重构，不是对全部古代语义的形式认证。审查者与主文及模型作者分离，均为AI辅助流程；未声称有人类专家或证明助理认证。

## 核验方法及结果

1. **独立逐元素oracle。** [oracle.py](../../reproduction/aristotle-prior-analytics-ii4/independent-audit/oracle.py)以`all`/`any`逐个检验成员资格，独立写六式规格，不复用待测实现的集合包含判断。八类型全部255个非空子集与六式共1530项逐项对照，前提真假、全假/部分假/空真分类、结论与存在侧条件全部一致。[真实输出](../../reproduction/aristotle-prior-analytics-ii4/independent-audit/oracle.log)。
2. **保存结果及最小性。** 重新生成普查对象与`witnesses.json`完全一致；另遍历全部模型，核查每个所存见证不存在更小对象数或同对象数更前字典序的见证。这里的最小性仅限所声明的压缩模型及目标分类。
3. **独立重跑作者测试。** 普通、`-O`、`-OO`各22项通过；不覆盖或改写作者运行日志。审查日志：[普通](../../reproduction/aristotle-prior-analytics-ii4/independent-audit/tests-normal.log)、[-O](../../reproduction/aristotle-prior-analytics-ii4/independent-audit/tests-O.log)、[-OO](../../reproduction/aristotle-prior-analytics-ii4/independent-audit/tests-OO.log)。输入合法性使用显式异常，不依赖优化模式会移除的`assert`。
4. **六式一般证明。** Darapti/Felapton由C非空取见证，再沿两条前提传递；Disamis/Datisi/Bocardo/Ferison由特称前提本身给出见证。所有前提的C为主项；结论以B为主项。普通I换位不能误用于O。前两式省略存在条件各出现7个有限反例，补条件后为0；后四式无须额外C存在条件。0个有限反例不是一般证明，任意域保真依靠见证论证。
5. **分类与构造。** 全假表示相反全称成立，部分假表示主项内有满足者和违反者；两者都为假，不是概率真假。特称只记真/假。C外加入结论见证不改C上的前提分类，因此两全称的9种分类对和含特称的6种分类对可与真结论共存。这是存在性，不是“假前提必得真结论”。
6. **压缩正确性。** 对每种A/B/C成员类型保留一个对象，保持四种命题的反例和见证以及项存在性；分类也保持。适用范围不包括数量、关系、模态或经验自然类约束。255、218、240分别对应非空域、三项均非空、C非空，口径分明。
7. **章末边界。** 在材料蕴涵下，两条`P→Q`与`¬P→Q`的合取等价于Q；有两个满足赋值，并非矛盾。`¬Q→Q`也等价于Q。程序只验证现代真值语义，不将此冒充原文“必然推出”的唯一解释。

## 审查范围

代码无网络、外部服务、密钥或第三方依赖；日志仅含环境、测试和模型结果。实跑证据不能代替历史来源核验，来源版本与误印由[来源记录](aristotle-prior-analytics-ii4.sources.zh-CN.md)独立负责。

## 最终文件绑定

主文终审通过：逐个检查第4节全部集合例、第5节四式含假特称例及一般构造、第6节条件句推导、第7节两个否定前提反例、全部16题答案；与代码方向和存在约定一致。首段已显式补C非空，证据段界已与来源台账统一。无未解决的数学或实现问题。此结论限定于下列文件版本；之后修改需重新核验。

SHA-256绑定正文、来源、根目录说明及全部复现代码/README/真实日志；不递归绑定本审查与另一审查文件。

|文件|SHA-256|
|---|---|
|`README.md`|`496f418cd943bed340e27ad0a33f8575c95733485d7a283f37171e007c7f8ef7`|
|`papers/ancient/aristotle-prior-analytics-ii4.zh-CN.md`|`104c6efa42a443f3c693fdf4f14f6ab451a823f6c05e2dde63e165c55595a915`|
|`papers/ancient/aristotle-prior-analytics-ii4.sources.zh-CN.md`|`89024e325d82ad1e7095b36708de0def4113a86ad58daebf0d2b9fc4ee456d34`|
|`reproduction/aristotle-prior-analytics-ii4/README.md`|`a3e8bd4d5151579aa3fbc6cc7934574120be2f64974e4ee04a06ad7aef197c8d`|
|`reproduction/aristotle-prior-analytics-ii4/independent-audit/oracle.log`|`b598f57af7dc244c0258eafab0459a52e63943bc120ee67de546a8aa90aecfd6`|
|`reproduction/aristotle-prior-analytics-ii4/independent-audit/oracle.py`|`cde8bd94462f0369c39c0e4c9de4a728fa314f202c0f5bb0799bb92b181ca24a`|
|`reproduction/aristotle-prior-analytics-ii4/independent-audit/tests-O.log`|`57b76035259a4b70f24ed3069f368b75128e7d200764fc42195b108528662bec`|
|`reproduction/aristotle-prior-analytics-ii4/independent-audit/tests-OO.log`|`5a854bde808b77d2e158137e49adb6c638d38aaa5eb0af569c84c20586afd562`|
|`reproduction/aristotle-prior-analytics-ii4/independent-audit/tests-normal.log`|`38d29371b1628cfb3d4941db81053815861e881175311eedbcf12a47c41661ab`|
|`reproduction/aristotle-prior-analytics-ii4/logs/environment.txt`|`991ef804c941dd23ec8796a4b4632234030a1602df911cf0a1aeaa8c1a68fa31`|
|`reproduction/aristotle-prior-analytics-ii4/logs/model-O.txt`|`adf437beebfb239b6a2a9de28bb4b3ba7a81b2ef0017044e4a82ac2957d794e8`|
|`reproduction/aristotle-prior-analytics-ii4/logs/model-OO.txt`|`adf437beebfb239b6a2a9de28bb4b3ba7a81b2ef0017044e4a82ac2957d794e8`|
|`reproduction/aristotle-prior-analytics-ii4/logs/model-normal.txt`|`adf437beebfb239b6a2a9de28bb4b3ba7a81b2ef0017044e4a82ac2957d794e8`|
|`reproduction/aristotle-prior-analytics-ii4/logs/tests-O.txt`|`e6939b76388d0748d6cbb20f0d5a8804f908aa630eb22569f5e38ca5e2eabe9d`|
|`reproduction/aristotle-prior-analytics-ii4/logs/tests-OO.txt`|`90b63b255a825ed4055971bd649f66c1a7d5224872e5ce7f9609a966b5f3cb3c`|
|`reproduction/aristotle-prior-analytics-ii4/logs/tests-normal.txt`|`3778bf8d7495754b6396f2131a6702afaebd3644ef00ad191a5415210b315f50`|
|`reproduction/aristotle-prior-analytics-ii4/model.py`|`e67d34aec33928790767c080f198a9b5c4bbc4b6dbc32b88f97b45b39cda0bf2`|
|`reproduction/aristotle-prior-analytics-ii4/run.sh`|`db94e845101f0f1ade35bd878c326da08ee66584841dcf3ebad6fb7f0004a205`|
|`reproduction/aristotle-prior-analytics-ii4/test_model.py`|`1a205d6b4e2fb2ba1c263b2a64c0f8365bd07dbc344d11a886413fbc6939f132`|
|`reproduction/aristotle-prior-analytics-ii4/witnesses.json`|`bfba8b75d39434206911cddf6c25d035d2d51d782bdfb4224d334de196f1b28b`|
