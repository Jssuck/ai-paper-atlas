# II.23 独立技术审查

**结论：通过本次限定范围的技术核验；未留未解决的数学或实现问题。** 本审查不代替来源独审及发布后的远端、链接、数学显示验证。

## 1. 独立方法与实际范围

审查者完整阅读本篇正文、七道练习答案、生产源码、测试和复现说明；另读 Jenkinson《前分析篇》Book II第23节及注97–99，视觉阅读 Owen印230–231正文和232续注。未把集合语义误作原典自身的算法。来源书目见[来源台账](aristotle-prior-analytics-ii23.sources.zh-CN.md)。

逐项检查了覆盖与观察的元素证明、分类不是最小传递必要条件、第三格的非空见证、剩余部分等价式，以及对全部A量化的覆盖必要充分性。取A=C的反向证明成立；它不声称单个全称结论偶然为真时也必须有覆盖。两对象非空反模型的最小性证明成立。所有七题答案与相应前提一致。

## 2. 发现、修正与复审

初稿第9节第4项称程序直接核验剩余部分等价式，实际生产代码核验的是失败定位集合等式。虽可从其空集条件联系理论等价，实跑对象仍须准确。已要求改写；最终正文明确直接比较集合等式，并区分理论联系。修改后复读通过。没有通过改动计数或放宽标准来掩盖差别。

## 3. 真实运行与独立对照

- 独立oracle不导入生产代码；生产采用位掩码，oracle用组合生成的集合与逐元素成员判断，并列出违反全性质转移的扩张。
- 正常、`-O`、`-OO` 三种模式均实际运行oracle与比较器；各比较4681个三集合世界的5类规则汇总（23405次规则评估）、341个全A量化配对和6个具名反模型，全部一致。
- 再以逐元素允许模式的闭式计数独立检查：完整前提3^n、最小传递4^n、弱前提5^n、非空特称5^n−4^n、失败定位前提6^n、全世界8^n，对n=0..4求和。结果分别与121、341、781、440、1555及4681匹配；弱前提中440个全称结论失败。
- 亲自重跑生产的11项单元测试，正常、`-O`、`-OO`均通过；显式异常验证与`unittest`方法不会因优化移除。输入上限检查拒绝布尔值、负值、非整数和过大值。
- 独立运行脚本及日志见[独立审目录](../../reproduction/aristotle-prior-analytics-ii23/audit/README.md)。环境仅标准库；没有联网数据、随机抽样、付费服务或新安装。

有限检查不是一般定理证明，也不是动物学实验或统计准确率。一般结果由正文任意元素证明和构造反例负责。所有数学关系固定同一论域；程序的空论域只是软件边界，不是古代语义断言。

## 4. 审查绑定的最终 SHA-256

以下摘要绑定已阅读与核验的文件。任何相关内容变更须重新核验并更新绑定；摘要不是电子签名。路径均相对于仓库根目录。

| 文件 | SHA-256 |
| --- | --- |
| `papers/ancient/aristotle-prior-analytics-ii23.zh-CN.md` | `e2970b1402b4ff149cd20162113b378cee0fe454e991b78372f6a97293c0c41e` |
| `papers/ancient/aristotle-prior-analytics-ii23.sources.zh-CN.md` | `aa0a5200a556f5ab5f5b50a1cd7a6867dfc131519c5429337cca9242d3f50aa3` |
| `reproduction/aristotle-prior-analytics-ii23/README.md` | `3fe32494b3e0c6e16c271dbfaf99695ae665025d0ba5e6d4eb24f3b1feb289d2` |
| `reproduction/aristotle-prior-analytics-ii23/audit/README.md` | `326d922d4533d5aba59c6b88ef6cb7f340efdda5bd8770510962f47dc2299c09` |
| `reproduction/aristotle-prior-analytics-ii23/audit/compare_production.py` | `6d4d18c0176a0dac16cdaa020349148084539cccab083e1f3e89e82cd4437e34` |
| `reproduction/aristotle-prior-analytics-ii23/audit/comparison-O.json` | `a1ace9dbad97d969ef0130c09f96691f099f90497cb64998b7831ea3cd6d644c` |
| `reproduction/aristotle-prior-analytics-ii23/audit/comparison-OO.json` | `9fc7d36fa89da9304019a5e7490180e76be6b78322cc68c3899559784a078a27` |
| `reproduction/aristotle-prior-analytics-ii23/audit/comparison-normal.json` | `f8d288e55b1bfb077ebc7f0e02d856aa178a0761ead5108f98c4b68a8fd80d67` |
| `reproduction/aristotle-prior-analytics-ii23/audit/independent_oracle.py` | `20dd2db349fcb372d4fdf993cd6f22e0bf11a6aeabe5f74078abfbd1881ba32c` |
| `reproduction/aristotle-prior-analytics-ii23/audit/oracle-O.json` | `c1f2562b83ddef75b1e1b9e5b331b9deb8887e66e0030b02d02636fb1406af76` |
| `reproduction/aristotle-prior-analytics-ii23/audit/oracle-OO.json` | `c1f2562b83ddef75b1e1b9e5b331b9deb8887e66e0030b02d02636fb1406af76` |
| `reproduction/aristotle-prior-analytics-ii23/audit/oracle-normal.json` | `c1f2562b83ddef75b1e1b9e5b331b9deb8887e66e0030b02d02636fb1406af76` |
| `reproduction/aristotle-prior-analytics-ii23/audit/run-audit.sh` | `8d41cbc7203b223de62220ee92119683a537ea8d0cc999ed235a3b0551cdbca4` |
| `reproduction/aristotle-prior-analytics-ii23/induction.py` | `558e506e68a675b207e060c38e987d425822a5ddb604edf63da4432efb65d86a` |
| `reproduction/aristotle-prior-analytics-ii23/results/comparison.log` | `7803eafe6a94e9b5978c9c2c410e30dd3cf861272175cd18e9e57099cb31d4b7` |
| `reproduction/aristotle-prior-analytics-ii23/results/double_optimized.json` | `61bb67c21dc9b9a20a7f851d626427926739bfdfa6a094bf96fd9697ee53c76f` |
| `reproduction/aristotle-prior-analytics-ii23/results/double_optimized.tests.log` | `a37d32743b037d138d387533b01fe8402cde9158d610c871a3ef11e574cfd639` |
| `reproduction/aristotle-prior-analytics-ii23/results/environment.txt` | `f16e93876fc1e36ecfdce27d32d9a8e5f9b0c7f186f8c7f02e303a3de67e3617` |
| `reproduction/aristotle-prior-analytics-ii23/results/normal.json` | `61bb67c21dc9b9a20a7f851d626427926739bfdfa6a094bf96fd9697ee53c76f` |
| `reproduction/aristotle-prior-analytics-ii23/results/normal.tests.log` | `1c57caa4f96939416d7e6463b7d795649d91d0d9367d7443a572968daa1fb40f` |
| `reproduction/aristotle-prior-analytics-ii23/results/optimized.json` | `61bb67c21dc9b9a20a7f851d626427926739bfdfa6a094bf96fd9697ee53c76f` |
| `reproduction/aristotle-prior-analytics-ii23/results/optimized.tests.log` | `1c57caa4f96939416d7e6463b7d795649d91d0d9367d7443a572968daa1fb40f` |
| `reproduction/aristotle-prior-analytics-ii23/run.sh` | `68827bc50644c680dc1f35d0a5542ebf57969da6d54ad492a3a7f60a3252bbe2` |
| `reproduction/aristotle-prior-analytics-ii23/test_induction.py` | `eae49224ed54a85b5d346b8057180ceea67f9f28f3f654352daf0fa376d62adb` |
