# II.27：独立技术核验

## 结论与边界

**技术终审通过。** 已逐节核对最终正文第4–10节证明、反例、14项练习及答案、复现README与实际输出；无需数学修订。发布前补齐README相对链接和独审链接，并纳入下表。

本审查针对原创教学重构，不认证历史医学例子或相面假说。审查者与正文/生产复现作者分离，实际读II.27全章70a3–70b38的Jenkinson转录，检查三格推理、卷末条件方向与可识别性。有限枚举不代一般证明；未使用经验数据或人格分类器。

## 独立实现与真实执行

生产实现用整数掩码；独立 `audit/independent_oracle.py` 使用布尔向量及逐对象量词，未导入生产实现。普通、`-O`、`-OO`各独立重算4681模型×7路线=32767组前提/结论。对比生产七路线的28个聚合/首反例字段及多数/映射模型全部指定字段，均一致。每模式另有5项独立单元测试通过，其中一项测试5种故意损坏结果被拒；三份oracle结果逐字相同。

生产未导出逐世界布尔证书，本审查不声称32767条生产中间结果被逐项比较。聚合比对不能单独排除相互抵消错误；代码阅读、独立反模型、一般证明和单测作为补充。

## 数学与实现核查

1. 第一格任取C成员沿C到B到A，集合包含传递成立；第三格从非空C选共同见证。空C不能提供存在结论。
2. 第二格双肯定的A={0,1}, B={0}, C={1}两前提真结论假，非空项仍失败。不能推广为一切第二格无效。
3. 第三格原例仅保证特称；A=C={0}, B={0,1}阻止全称越界。该反例与原文批评的目标强度吻合。
4. 卷末A=B强条件蕴涵B⊆A，但第一格结论本身不需要反向包含。原文C严格窄于B的情形包含在程序C⊆B弱化核验中，且单测明确严格情形。
5. 仅A⊆B不足倒推；A={0}, B={0,1}, C={1}给非空反模型。标签“迹象”不能替代方向前提。
6. 2×2匹配仅排除既定全局双射；全同真行不能识别，分离行在假设内留下一个候选，新行可排除两个候选。没有从观察样本证明未观察对象，更没有推出因果或身体—人格真实性。
7. 9/10合成例只有多数与全称的逻辑区别，二分之一不是古代eikos的数值定义；模型计数也不是自然频率。
8. 代码范围0–4包含空域压力测试，解释不归给Aristotle；全部子集带标签枚举，不除同构。优化模式检查使用unittest与显式异常，未依赖裸assert。

## 实跑证据

见[独立核验说明](../../reproduction/aristotle-prior-analytics-ii27/audit/README.md)、[独立源码](../../reproduction/aristotle-prior-analytics-ii27/audit/independent_oracle.py)、[独立测试](../../reproduction/aristotle-prior-analytics-ii27/audit/test_oracle.py)和该目录各模式JSON/日志。生产18项测试三模式均通过。仅运行低成本有限形式实验，不宣称完整复现全部原典。

## 最终文件绑定

以下SHA256绑定审查实际读取的最终文件；哈希不是经验正确性证明，任何内容修改后需重新审查或确认纯格式变化。

| 文件 | SHA256 |
|---|---|
| `papers/ancient/aristotle-prior-analytics-ii27.zh-CN.md` | `6d76b138a5cd6bc8294cd0ea971609f7c9ff490a8ed64fd05abc4452a7b5c683` |
| `papers/ancient/aristotle-prior-analytics-ii27.sources.zh-CN.md` | `49de28ffc525ceb025e45f4e80c3d9a3dd74e6c1903f030e7c23504f9510099c` |
| `reproduction/aristotle-prior-analytics-ii27/README.md` | `9b4f2d531d4f920afc0eb76815d5e7b0bbd442a3257799bf9eb65108dbfd98cc` |
| `reproduction/aristotle-prior-analytics-ii27/audit/README.md` | `79c885ea5d83ee5e240af0879babbb07e4c94af721bb131f1d13efd378376330` |
| `reproduction/aristotle-prior-analytics-ii27/audit/comparison.log` | `104ecf76a0efd9b22ccdcec117801ddbdd7392db356493073b183bdb7f9263b7` |
| `reproduction/aristotle-prior-analytics-ii27/audit/independent_oracle.py` | `05dd498dac9199f718009a9cd2d9bc8c224499a7fd3ae00eb23c0da8b3ece309` |
| `reproduction/aristotle-prior-analytics-ii27/audit/oracle-O.json` | `e3b0fd639e859d0aec777c6166ed0a40bcd53ce25c6b6a6a3936409026acd6f0` |
| `reproduction/aristotle-prior-analytics-ii27/audit/oracle-OO.json` | `e3b0fd639e859d0aec777c6166ed0a40bcd53ce25c6b6a6a3936409026acd6f0` |
| `reproduction/aristotle-prior-analytics-ii27/audit/oracle-normal.json` | `e3b0fd639e859d0aec777c6166ed0a40bcd53ce25c6b6a6a3936409026acd6f0` |
| `reproduction/aristotle-prior-analytics-ii27/audit/run.sh` | `b4ee184b6e5287cbdb82dc1d724c4f580501d042f41a0cb2ccca3146461b7fbd` |
| `reproduction/aristotle-prior-analytics-ii27/audit/test_oracle.py` | `a00ff8a5c574584f88940d09ddc7bc99d6771fd3839535a1d63f21ec902dff89` |
| `reproduction/aristotle-prior-analytics-ii27/audit/tests-O.log` | `c0d2e2ba0a27bebfe838c57ee357c55c9685cf722c9919d78f9faf42b8c6a525` |
| `reproduction/aristotle-prior-analytics-ii27/audit/tests-OO.log` | `27cf02ab8dcf778bc1c10f47d5770dfb6f7c2cb0247f9155b7132c2ee8b59cd2` |
| `reproduction/aristotle-prior-analytics-ii27/audit/tests-normal.log` | `e70c8f18d10d95a962f03f201d696bed75a45bf23a402892524f31f156e75410` |
| `reproduction/aristotle-prior-analytics-ii27/environment.json` | `0d89f4fcedef9898f35f0505cd8f697a9c6f56a5d0e65b59aec056652d4ba557` |
| `reproduction/aristotle-prior-analytics-ii27/logs/comparison.log` | `6d02a0d946ab2bc240f37a3a936f78c861fa1ebdb694de6b3ad37d28045e10d5` |
| `reproduction/aristotle-prior-analytics-ii27/logs/results-O.json` | `e2030cb92a905b83eb64c0359e6e5e3d0ed7b4e44820002f7c5e99ccb15825c5` |
| `reproduction/aristotle-prior-analytics-ii27/logs/results-OO.json` | `e2030cb92a905b83eb64c0359e6e5e3d0ed7b4e44820002f7c5e99ccb15825c5` |
| `reproduction/aristotle-prior-analytics-ii27/logs/results-normal.json` | `e2030cb92a905b83eb64c0359e6e5e3d0ed7b4e44820002f7c5e99ccb15825c5` |
| `reproduction/aristotle-prior-analytics-ii27/logs/tests-O.log` | `ed724e435a57ddbe38415d0ced35cfa654d74751cf7aa876e947e2b29e9e0ed7` |
| `reproduction/aristotle-prior-analytics-ii27/logs/tests-OO.log` | `91bef6c80d599e47ae6444d8f30143f1ef09c1bd54762a8aa48f4fdbf0e8b2ea` |
| `reproduction/aristotle-prior-analytics-ii27/logs/tests-normal.log` | `8f223c8ee55fe053e6f8fcf598c47e8460a5dbbb8fa3472dfd8a7f1ff6963c14` |
| `reproduction/aristotle-prior-analytics-ii27/run.sh` | `2d037a853ac3dc6908c63734d75bbec060f341c8d7a7f8f36993724c4bc4ef06` |
| `reproduction/aristotle-prior-analytics-ii27/signs.py` | `5f8f21cface0c2392c800db37d12d774b4de66f41f8e3c75d0f0e0912685f85f` |
| `reproduction/aristotle-prior-analytics-ii27/test_signs.py` | `2323b6b4c20f0824b65adbf4b10689b64fa61be638e216a589c635a80e9786c2` |
