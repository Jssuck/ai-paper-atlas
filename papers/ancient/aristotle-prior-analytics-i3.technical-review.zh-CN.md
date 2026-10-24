# I.3：独立数学与代码审查

审查对象是[正文](aristotle-prior-analytics-i3.zh-CN.md)及[最小复现包](../../reproduction/aristotle-prior-analytics-i3/README.md)。本报告是原创技术核验，不以模型测试裁决古代唯一解释。

## 结论

在下列 SHA-256 对应的文件范围内，未发现阻止发表的数学或代码问题。完整阅读正文定义、一般证明、反例、数据说明与15题答案，并独立读取生产实现和测试。核验通过仅限明示现代语义及本文声明的实验范围，不认证古代完整模态体系。

## 逐项数学核验

1. **整句模态的E/I换位。** 两项交集逐情形对称，故E与反向E、I与反向I逐情形等价；对全称情形量词N或存在情形量词P应用等价替换成立。NI中的见证可随情形改变，正文未错误交换“所有情形/同一对象”的量词。
2. **全称到特称的存在条件。** NA加每个情形S非空，逐情形取见证，推出反向NI。论域非空、仅实际S非空均不足。PA在一个实现A且S非空的情形中就能取见证；正文把全情形非空和同情形存在均称充分条件，没有误称它们是某模型反向PI成立的必要条件。
3. **O的方向性。** 单情形真子集实例满足前向NO/PO，不满足逆向NO/PO。名称只是示例标签，不承担现实分类证据。
4. **否定作用域。** P(非φ)等于非Nφ，而不是非Pφ；正文真/假双情形反例正确。Nφ蕴涵Pφ依赖非空情形范围，定义已明示。
5. **严格整句偶然C。** CE仍对称，CA不一定弱化为逆CI，即使主项各情形非空。正文表格与测试使用的两个略有不同的w0谓项集合都产生A有真有假而I始终为真；二者均是有效反例，未混报为同一数据记录。
6. **实际主项de re。** 语义固定实际主项成员，对其谓项成员关系跨情形量化，逆向时实际主项变为原谓项。这种非对称定义下NI、NE、CO均可能换位失败。正文及附件明确展示失配，不把该模型当成原章所有规则的认证。全称de re C在空实际主项上空真已在正文与复现README补明。
7. **历史标签Q。** Q_O链的中间特称肯定换位是额外历史规则依赖，不由逐对象肯否互转单独推出。正文明确此点，也没有把Q_E不能简单换位夸大为没有任何逆向特称后果。该链不是一个未经给定模型的可靠性定理。
8. **练习及计数。** 15题答案与上述定义一致。4452模型是有标签枚举而非同构类，133560是规则槽位而非全都有真前提；守卫和前提数量已区分。结果不是概率、准确率或心理实验。

## 独立程序核查与真实执行

生产程序按世界位掩码枚举；审查器另按对象跨世界成员历史枚举，并使用集合包含/不交关系和真值计数，未导入生产语义函数、枚举器或其测试oracle。独立重算4452模型、30规则的60个计数字段，全部一致；22个首反例另逐一验证前提、守卫和逆向结论，均成立。

- 审查器5项测试在normal、-O、-OO各通过，三个结果文件逐字节一致。
- 另独立重跑生产18项测试，在三模式各通过；每次生产自带布尔矩阵oracle比较106848个语义结果无差异。
- 输入异常、重复情形、空词项、必要/可能/严格偶然、跨情形见证、双重换位和否定对偶都有针对性检查。生产使用unittest断言方法，不依赖Python优化后删除的assert语句。
- 审查器最初把固定解释的整句C恒假错误推广到空主项de re全称C，导致审查测试一次失败；已修正测试假设，不更改生产语义。所链接日志是修正后实际运行，不把失败记录冒称成功。

代码、命令、结果与日志见[独立审查附件](../../reproduction/aristotle-prior-analytics-i3/audit/README.md)。有限枚举不是一般证明；一般有效性依靠正文逐步论证。测试覆盖不等于已证明程序对所有任意输入正确，也不等于古代体系的可靠性或完备性证明。

## 最终文件绑定

以下哈希绑定本次已审查版本；若内容改变，应重审受影响部分并更新绑定。

| 文件 | SHA-256 |
|---|---|
| `papers/ancient/aristotle-prior-analytics-i3.zh-CN.md` | `e55c6ee542a39bc8a7ca57aeccad2324c5cc9730a8983ab6437792854fbb2153` |
| `reproduction/aristotle-prior-analytics-i3/README.md` | `174c4402e632848e80c2de048a0ed16a0ca510c5070945492cb7e3580a651a69` |
| `reproduction/aristotle-prior-analytics-i3/audit/README.md` | `dc1bd49d4c17ee74728214f78093c76ad6089c840012645bced41dd5a64ec608` |
| `reproduction/aristotle-prior-analytics-i3/audit/comparison.log` | `2cc2c954a82088ae938ca9aca19a95f0492692335d901a5a197a42b0ad6e232c` |
| `reproduction/aristotle-prior-analytics-i3/audit/independent_oracle.py` | `f67ca0f3c3c72d41800f8efe705c0d5de32fdd5b49970c2ebbdc92db27b9d549` |
| `reproduction/aristotle-prior-analytics-i3/audit/production-tests-O.log` | `7e324cc0f0236248f08de5043318d1031f9032573bdba610580e45f2601c8e94` |
| `reproduction/aristotle-prior-analytics-i3/audit/production-tests-OO.log` | `b1c194d16bef0dc876540b71829e08cd46c30044b92354f69805828be9c17f2f` |
| `reproduction/aristotle-prior-analytics-i3/audit/production-tests-normal.log` | `1eeee9db14b6ee3204b72731233db627a3906b90ef818be98ab7bf4a4eef4f2b` |
| `reproduction/aristotle-prior-analytics-i3/audit/results-O.json` | `cdc8da5d3445e374e0c2d1b0318f0ea93fa33a64308af22daf37fb17e721149e` |
| `reproduction/aristotle-prior-analytics-i3/audit/results-OO.json` | `cdc8da5d3445e374e0c2d1b0318f0ea93fa33a64308af22daf37fb17e721149e` |
| `reproduction/aristotle-prior-analytics-i3/audit/results-normal.json` | `cdc8da5d3445e374e0c2d1b0318f0ea93fa33a64308af22daf37fb17e721149e` |
| `reproduction/aristotle-prior-analytics-i3/audit/run.sh` | `e87291d70fa44e24ebeb32e02aad16fc997071fc169ee2e081a7e424c3b55e61` |
| `reproduction/aristotle-prior-analytics-i3/audit/test_oracle.py` | `58d2f631d7fdb20b2d101a124701549c25e6fbe581048de0c5a973757c3a334c` |
| `reproduction/aristotle-prior-analytics-i3/audit/tests-O.log` | `a29dbe9ad28423bd047009ed13c1c655ba35eb70559aff32bddfe26dfb7d21ba` |
| `reproduction/aristotle-prior-analytics-i3/audit/tests-OO.log` | `c3f9f4ec2f70b81c216813e072d929b1fc7718949da5506939cc27a3b0724afe` |
| `reproduction/aristotle-prior-analytics-i3/audit/tests-normal.log` | `0fb86161d0a0e8ec515deba1b574cc04873d706ad6d3a31531cb9740ef33888f` |
| `reproduction/aristotle-prior-analytics-i3/logs/environment.txt` | `2f9c798f2ca6d37d8ecd241c12b4102a1428f2e14bc90295ef622e4977526f2e` |
| `reproduction/aristotle-prior-analytics-i3/logs/results-O.json` | `c5cb5499b74e38ebdd83265fa04ba74d57e95e05efe7f6891048186122444f31` |
| `reproduction/aristotle-prior-analytics-i3/logs/results-OO.json` | `c5cb5499b74e38ebdd83265fa04ba74d57e95e05efe7f6891048186122444f31` |
| `reproduction/aristotle-prior-analytics-i3/logs/results-normal.json` | `c5cb5499b74e38ebdd83265fa04ba74d57e95e05efe7f6891048186122444f31` |
| `reproduction/aristotle-prior-analytics-i3/logs/tests-O.log` | `de86778003b44f081816bd33291362b2ddd6fbb4e17e07fb4abafcc32f057a9c` |
| `reproduction/aristotle-prior-analytics-i3/logs/tests-OO.log` | `ce2b57972d4f4fc91b1b7a3dd1ee754bdca06a9ca81d3eefac4a1649f9875255` |
| `reproduction/aristotle-prior-analytics-i3/logs/tests-normal.log` | `832e97a0efaacd467f3cda8a8084b3e443b81774915540bb3e82c56cf324685b` |
| `reproduction/aristotle-prior-analytics-i3/model.py` | `f06dfadb1beff808f149eb3ac8f502554be4ed05528c19410799f7bdbb89c0b4` |
| `reproduction/aristotle-prior-analytics-i3/results.json` | `c5cb5499b74e38ebdd83265fa04ba74d57e95e05efe7f6891048186122444f31` |
| `reproduction/aristotle-prior-analytics-i3/run.sh` | `8a6c6b6d4c4fed356c8117511ca644a99f74984705f741522400afb43b076997` |
| `reproduction/aristotle-prior-analytics-i3/test_model.py` | `ba3f37486530d2ec841105f0261b6e94b7881b1bcab4e4e8eef84504278a4e62` |
