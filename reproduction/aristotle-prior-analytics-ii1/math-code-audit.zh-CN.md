# 《前分析篇》II.1：独立数学与代码审查

## 结论与范围

**通过。** 独立检查正文的一般论证、显式反模型、证明依赖解释、程序规则及输入边界，未发现需要修正的数学或程序缺陷。本记录针对现代集合语义下的教学重构，不将有限枚举当作一般定理证明，也不以代码正确性裁定古代文本的唯一解释。来源层级另见正文旁的来源核验记录。

## 一般证明核查

1. E换位由交集交换律成立；I换位使用同一见证。A转I必须另有主词非空条件，不能从包含关系凭空生成见证。空类反例确实满足A却不满足逆向I。
2. 全称肯定限制由包含传递性成立；全称否定限制由子集与不交关系成立。正文对任意集合的逐步证明独立于程序中的有限论域。
3. 第二格Cesare的证明：若对象属于C而且属于B，由C包含于A可得其属于A，与A和B不交矛盾。对子中项E的相同推论仅需E包含于A及原不交前提，不需要C包含于A。两项原前提的分别删除反模型，支持的是相对于原前提对的必要性，不是全局唯一证明。
4. 特称Darii把同一交集见证沿包含关系传递；任意缩小含有该见证的类可能丢掉见证。正文给出的非空子类反模型有效；改成另一子类又可恢复肯定，故亦不能无条件推出否定。若额外确保子类与中项相交，恢复肯定的论证成立。
5. O换位失败的两边非空反例正确。章节语境下的结论计数没有被夸大为“O命题没有其他逻辑后果”。换位等值前提不构成独立知识来源的说明，与现代语义蕴涵、具体证明树和最低支持集的区分一致。
6. 16道练习的答案与上述存在条件、限制方向及依赖范围相符；没有把短程序的能力扩展为完整亚里士多德逻辑系统。

## 独立程序方法与真实实跑

新增独立审查脚本 [`independent_check.py`](independent_check.py)。它以整数位掩码计算四种命题，不调用作者的模型枚举器来产生期待结果；再与作者集合实现、统计函数和证明树逐一比较。正常、`-O`、`-OO` 三种模式均实际运行，每次10项 `unittest` 测试通过：

```sh
python3 independent_check.py
python3 -O independent_check.py
python3 -OO independent_check.py
```

真实输出分别见 [normal](logs/independent-normal.log)、[-O](logs/independent-O.log)、[-OO](logs/independent-OO.log)。优化模式没有关闭 `unittest` 的断言方法。本次未安装包、未修改作者源码；作者18项测试和实验输出亦已检查。

覆盖范围：

- 0至3对象论域中全部585个三项集合模型，独立重算各统计；四种命题另与集合实现逐对比对。
- 七条支持的推理规则在585个模型中逐一检查，共4095个规则／模型组合；检查内容是“所有叶前提成立时结论成立”，不声称4095例都满足前提。
- 四个示例树在1024个五项集合、二对象模型中检查，共4096个树／模型组合，同样使用条件健全性判据。
- 三对象、四集合的4096种组合另查包含链和见证恢复条件。
- 检查伪造结论、非法证明父项类型、派生标签、错误存在前提、未支持O换位及非法特称限制被拒绝；检查负数／布尔论域大小、非法元素、缺失项及空项名等边界。

独立重算结果如下；各行有重叠，不能相加解释成互异模型数量。第三项集合D即使未出现在某一性质中也仍参与585个模型的计数。

| 项目 | 数量 |
|---|---:|
| 全部模型 | 585 |
| A且主词非空的换位适用例 | 174 |
| E换位适用例 | 259 |
| I换位适用例 | 326 |
| A全称限制适用例 | 85 |
| E全称限制适用例 | 85 |
| O逆换位失败反模型 | 174 |
| 非空子类丢失特称见证反模型 | 26 |
| 无存在条件A转I失败反模型 | 85 |

## 证明依赖与适用边界

四棵示例树的叶标签集合均与逐树结构一致。`dependencies()`返回的是**所给合法树实际使用的叶标签**，不是在全部可能证明中求得的最小支持集。标签是调用者元数据，重复标签会合并；独立测试特意使用同名的两个不同前提并验证这一行为。因此调用者需使用独立标签，不能把标签去重等同于证明前提等值或独立性。

健全性审查对应有限、合法构造的证明树和程序已列举的规则；不声称完备性、全局最小证明搜索或对任意恶意对象图的支持。以上一般论证才是跨任意论域的依据，有限测试只能发现实现错误和展示具体反例。远端链接及GitHub视觉公式检查由发布环节另行完成，本记录不冒充已经验证远端渲染。

## 最终文件绑定

SHA-256如下，绑定已核验正文、复现说明、源码和真实日志。审查记录不对自身建立循环哈希；任一被绑定文件改动后应重新核验、更新绑定。

| 文件（相对仓库根） | SHA-256 |
|---|---|
| `papers/ancient/aristotle-prior-analytics-ii1.zh-CN.md` | `e712e9114ed33dbdede1868d83331e5f4ecb9a806dbe4e166238c8025ba6e880` |
| `reproduction/aristotle-prior-analytics-ii1/README.md` | `8eaa5f5e3529a78da9ad16c04fa364b07fdcf8ad21ba679720c430cffff9ddd7` |
| `reproduction/aristotle-prior-analytics-ii1/model.py` | `0ed06e86bab4d7becd6e4c190c74be541d540ca8370247265b5f41fd9d072e51` |
| `reproduction/aristotle-prior-analytics-ii1/run_experiment.py` | `15cd0c042808403638ccf3e4ba293a283e8260a66ae325459e6c3c7c71043265` |
| `reproduction/aristotle-prior-analytics-ii1/test_model.py` | `a857ad99954c0f27c90faea2aa24271dc3ea1b2657b58b11196efe65dee2b12a` |
| `reproduction/aristotle-prior-analytics-ii1/independent_check.py` | `e027b5abcc3ff7dd901ffd18095a3e32184a92aec2823ea64d1d247a40e1d5e3` |
| `reproduction/aristotle-prior-analytics-ii1/logs/environment.log` | `9dd14fd7fd5941b976b60b0a1d74c632b0dcf46bb4b53d6d6eccba798349128d` |
| `reproduction/aristotle-prior-analytics-ii1/logs/experiment-O.log` | `b07fb061c665892e378b71b5e0c643f9dc05ee664696ba84bf70066a6f0e5582` |
| `reproduction/aristotle-prior-analytics-ii1/logs/experiment-OO.log` | `79c9ea509abacbff4abb51dd9ae70dedea7e285f2a98537104d12d8748f53fe0` |
| `reproduction/aristotle-prior-analytics-ii1/logs/experiment-normal.log` | `b3961061d2c8c6333e1b325b4c30d5513a34981c029e3a2f93b5ef6655bc499e` |
| `reproduction/aristotle-prior-analytics-ii1/logs/independent-O.log` | `f3114b50efb0d362e55008a0b445d4a31d3fcd2c117ac7c0a39d22f8d173b48d` |
| `reproduction/aristotle-prior-analytics-ii1/logs/independent-OO.log` | `da553445b232af55f846a1992c92c7d7ade2e87c497d7b31ff4170fbda13a27d` |
| `reproduction/aristotle-prior-analytics-ii1/logs/independent-normal.log` | `30793de7ed4a0c5cc00f098bb59054d18a8a008f35460e4a694bb141498e5cda` |
| `reproduction/aristotle-prior-analytics-ii1/logs/tests-O.log` | `56f1eedacdb65c6743673a9e4953b7b4cbe9ab348b6b2b33708b69bb8cbd932d` |
| `reproduction/aristotle-prior-analytics-ii1/logs/tests-OO.log` | `98d2a90f8a45d247e6ffcd3ff6ace5237c6604e2f65b3f00c241da0346187932` |
| `reproduction/aristotle-prior-analytics-ii1/logs/tests-normal.log` | `bbd3d1f266567841d281c551c0e8ed0eb5322a17ff4e3356f2d1a723be0f3dc0` |
