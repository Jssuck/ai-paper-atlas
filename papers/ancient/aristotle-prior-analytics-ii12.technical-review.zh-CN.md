# II.12 独立数学与代码审查

## 结论与范围

**通过。** 对照本章四种归谬路线，审查正文逐步推导、12题答案、教学符号、存在条件和真实复现。作者与复现实现者之外的审查者使用独立显式集合程序；审查范围为所声明的一元、二值、实然教学语义，不裁定古代唯一解释。来源、章界及校勘由另份来源独审负责。

## 数学核验

1. 四种目标的内部第二格分别核为 O+U→O、E+U→E、I+E→O、U+E→E，谓项/主项及共同中项位置正确。每一推导保持同一见证，不把两个存在见证拼接。
2. 两个全称目标使用 U(C,B) 背景；两个特称目标以 I(C,B) 显式承担存在。将后者换成 U(C,B) 会在 B 为空时失败，单独补 B 非空足够，不必要求三个项存在。
3. 排除错误 E 假设只直接给 I，不给 U；正文正确区分局部撤除规则与原强背景本来蕴涵 U。弱背景的反例未冒充原强背景反例。
4. I 与 O 共真反例、非 E 不蕴涵 U、非 U 不蕴涵 E 均核对。第9节12题答案与正文符号一致。
5. 一般保真证明以任意满足背景的模型为起点；八类型代表构造独立于有限运行结果。正文没有把有限测试单独当作一般定理证明。

## 独立运行与交叉核对

- 独立程序不导入生产真值函数或模型枚举器。第一轮显式集合有标号域枚举：允许空项584模型、三项非空371模型，分别64候选；这是有界交叉检查。
- 第二轮独立枚举八种布尔三元类型的占用，以显式集合解释命题，对照生产全部128候选的内部和外部记录，共256条。有效性、前提满足模型数、反模型数、按基数和字典序选出的最小反模型全部一致。
- 11项具名检查全部一致；允许空项的有效路线4条、三项非空6条，与正文1/1/1/1及1/1/2/2一致。
- 独立程序普通、-O、-OO模式各6项测试通过；审查者另重跑生产12项测试成功，核验生产 SHA256SUMS 全部通过。生产三个模式的结果逐字一致。
- 运行证据见[独立说明及日志](../../reproduction/aristotle-prior-analytics-ii12/independent/README.md)、[生产重跑日志](../../reproduction/aristotle-prior-analytics-ii12/independent/production-rerun.log)。

## 修正闭环

初审发现命题三元素传入非字符串时可能抛出 TypeError，而非接口预期的 ValueError。已由实现者增加类型及长度前置校验，并加入 None/list 输入用例，重新运行三模式测试。数学输出未变，当前无待修技术问题。

## 最终文件绑定

以下 SHA-256 标识审查版本。修改正文、源码或测试后必须重新核验并更新绑定。

|文件|SHA-256|
|---|---|
|papers/ancient/aristotle-prior-analytics-ii12.zh-CN.md|4237847396421b40493452cfc57abc5488186d056b34152226e4b8762e4d49df|
|papers/ancient/aristotle-prior-analytics-ii12.sources.zh-CN.md|cd3f6508cfd9e9434db0024b1b43b9e62feaa12c37c8f3f426656de834bb8120|
|reproduction/aristotle-prior-analytics-ii12/reproduce.py|df37a019dd3d934ed27289f429c36013fdf2f799c63f8e4761310689dc7cb1c4|
|reproduction/aristotle-prior-analytics-ii12/test_reproduce.py|0433ed97d31d8b917a1372c61022e75ba301020982a712711f4d24278844979c|
|reproduction/aristotle-prior-analytics-ii12/run_all.py|9c5a8a7eebe25901906cd97168ea20ba03438d7beca10567677815011a2a8135|
|reproduction/aristotle-prior-analytics-ii12/independent/oracle.py|7f32922659554a315c4894d41431d9b6335bfdcdab212d43f4eea2b6b6b1e187|
