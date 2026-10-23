# I.45：独立数学与代码审查

## 审查对象及隔离方法

本审查独立于正文撰写和作者复现。审查者阅读正文证明、`model.py`、`test_model.py`、`run_experiment.py`、复现说明与真实日志；独立文件 `independent_check.py` 不调用作者的模型生成器来生成其测试样本，也不使用作者的真值函数来计算期望值。它枚举大小0、1、2、3的对象域及其三个任意子集，共585个赋值，以集合包含、交与差另行实现四种命题，然后与作者函数交叉核验。

独立运行不意味着没有使用作者接口：证书接受和拒绝测试有意调用作者检查器，被比较的语义期望由独立实现给出。有限核验不是一般证明，也不是古代解释的权威裁决。

## 数学检查

- A/E/I/O统一用主项在前。E和I换位保真且双向；A限量换位须有原主项的存在前提，只是单向信息削弱。O不可一般换位。
- 第一格四式、第二格四式、第三格不需要附加存在的四式均有效；Darapti与Felapton另须中项非空。空中项使其两全称前提成立而特称结论失败，已显式测试。
- Camestres须把经第一格所得E结论换位，Disamis须把I结论换位。只更换字母、忽略原目标方向是不合格的归约。
- Baroco/Bocardo的临时假设必须恰好是目标的矛盾命题。作者证书使用第一格Barbara产生与原特称否定冲突的全称命题，再解除该临时假设。检查器拒绝错误的解除目标。
- 拒绝O换位不证明任意算法或证明体系无法处理对应有效式。两个特称前提也可由不同见证满足，不能据此拼出同一端项见证。
- 七种非全零成员类型的压缩适用于本教学语言，因为四种命题仅检测类型是否出现，不检测重数或三个项之外的对象。该理由是一般的语义论证；128次或585次实跑不是这个理由的替代物。

## 代码、输入与真实运行

作者的输入检查不用可被优化模式删去的assert；引用索引排除bool、负数、未来行，证书输出必须与所调用规则计算结果一致。存在前提和生成器输入会物化后验证，不因短路漏查未知项。此检查器仅处理S/P/M三个不同命名项，并非通用一阶逻辑证明器。

独立13项测试在normal、`-O`、`-OO`各运行一次，均通过。每模式完整评价192个格—式组合与585个对象赋值，共112320次式—模型检查；另有14040次作者真值函数与独立实现的比较。独立检查还验证8份直接证书、2份归谬证书，并测试错误换位、缺失存在条件、未来引用、伪造输出与错误假设解除。

命令（在此目录执行）：

```sh
python3 independent_check.py > independent-normal.log 2>&1
python3 -O independent_check.py > independent-O.log 2>&1
python3 -OO independent_check.py > independent-OO.log 2>&1
```

作者21项测试及实验日志另行读取并复核：每模式128个类型模型，109个三项全非空模型，14个具名式共1776次满足存在政策的式—模型检查；2256次换位检查。1776并非14乘128，因为Darapti、Felapton各只接纳120个中项非空模型。2256为E/I的1536次加有主项存在条件的A限量换位720次。Felapton到Festino的前提变换只有单向蕴涵，不声明等价；120个接纳模型中112个前提真值相同，与限量削弱的性质一致。

原文、一般证明、程序规格和有限观察分别陈述。没有把测试通过称为证明助理认证或完整复现整部《前分析篇》。原文来源与适用勘误另见来源审查。

## 最终文件绑定

正文第3–8节的一般证明、两个弱化前提反模型、两条归谬、16题答案和第10节统计已逐项审读，无剩余数学错误。以下绑定是审查完成时的SHA-256；任何后续修改须复核并重绑定，不把旧审查自动套用于新文件。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-i45.zh-CN.md`|`048acd44efa774ccb8e5ab9c4e8d03f51d0429ffb857f731fe36d5d86cdc7b2b`|
|`reproduction/aristotle-prior-analytics-i45/README.md`|`4e0d7503c9053701aed35919395f37c447ff98d466f446b6bd47223eec992c62`|
|`reproduction/aristotle-prior-analytics-i45/independent-O.log`|`521962bc4efd938912e31a6ffa501e3cdf8da31550235e2b51632176488fd49d`|
|`reproduction/aristotle-prior-analytics-i45/independent-OO.log`|`da90baeb4db85313fcf05b6129cafd1e5a81377b2c7d09d9baee8cb96a2f7f50`|
|`reproduction/aristotle-prior-analytics-i45/independent-normal.log`|`da90baeb4db85313fcf05b6129cafd1e5a81377b2c7d09d9baee8cb96a2f7f50`|
|`reproduction/aristotle-prior-analytics-i45/independent_check.py`|`e3d701c11a9c2f6a2cb90299ddb3b4a33b9e9553175358a70cab9dacaa02a871`|
|`reproduction/aristotle-prior-analytics-i45/logs/environment.txt`|`3e6087ca8b0d512f9bdfc884161a9c3221de51ac8374412590e7ee1d93524c4e`|
|`reproduction/aristotle-prior-analytics-i45/logs/experiment-double-optimized.txt`|`51a10ecb26390b591effeb9d9fdd54e3cb859d650eab4edf9b2b9e749f621008`|
|`reproduction/aristotle-prior-analytics-i45/logs/experiment-normal.txt`|`51a10ecb26390b591effeb9d9fdd54e3cb859d650eab4edf9b2b9e749f621008`|
|`reproduction/aristotle-prior-analytics-i45/logs/experiment-optimized.txt`|`51a10ecb26390b591effeb9d9fdd54e3cb859d650eab4edf9b2b9e749f621008`|
|`reproduction/aristotle-prior-analytics-i45/logs/tests-double-optimized.txt`|`63b32ef46767ffe6d4aff14208ca3f64ed806c1971a33cffc2de5268480e214f`|
|`reproduction/aristotle-prior-analytics-i45/logs/tests-normal.txt`|`b6de14203907c132f6635096744f7ec4ccdded1e01f8e6ebbdb97625eb4a5159`|
|`reproduction/aristotle-prior-analytics-i45/logs/tests-optimized.txt`|`0adb77bff06ef624140f3c0dc055fdc3f85da6c57312a9ca0007f9b702994dfd`|
|`reproduction/aristotle-prior-analytics-i45/model.py`|`4f95662647265924cc94f7964fb9e69873b3fcfb395a4de07fa75e0bbab49353`|
|`reproduction/aristotle-prior-analytics-i45/run_experiment.py`|`d3f68b085870655d47541fa60c6a1bba3da53d894383f0c0fa1a4fdfa5dc8c48`|
|`reproduction/aristotle-prior-analytics-i45/test_model.py`|`de577cb70632401e3042b684db2340a483805a8f12b8fa2b9fcd22b126e9707a`|
