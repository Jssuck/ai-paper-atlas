# II.3 独立数学与程序审查

审查日期：2026-10-23。结论：下列 SHA-256 版本通过独立数学与程序核验；本记录不替代独立来源校读或 GitHub 实际显示检查。

## 范围与结论

逐项检查四个模式的谓项/主项方向、保真证明、全假与部分假条件、空项规则、正文算例和16道练习。Cesare/Camestres 全称结论与 Festino/Baroco 特称否定结论一致；特称证明保留必要的存在见证。正文把56a34文本疑难与教学修复区分开，没有让模型声称裁决古代原稿。外部文献的版本事实由另行来源审查承担，本审查只验证对应逻辑关系。

发现并修复一处范围措辞：原先“任意大小模型”可能误称低于最小见证基数也能实现混合状态，现改为“这些组合在所声明语义中可实现的一般证明”。最终版本已复核，未见剩余阻断性数学错误。

## 独立方法与真实结果

不只调用作者的测试作为证据。独立脚本用 `all` / `any` 的逐对象量词定义真假，用另一套位掩码支持枚举得到分类计数，再逐项对照保存的 `witnesses.json`；每个保存见证重新核验分类、结论与最小基数。

- 独立支持枚举：255个非空论域类型支持；要求 M、P、S 都非空时218个。两种政策下所有计数和全部最小见证一致。
- 另枚举标号论域大小1至4的4680个模型，允许多个对象具有相同成员类型；检查全部四种命题和九种有序项对。共168480次真假、分类与压缩保持性的对照通过。
- 独立重跑作者21项测试，普通、`-O`、`-OO`三模式均通过，退出码0。原作者日志未被这次重跑覆盖。
- 两个全称模式的9格、两个特称模式的6格由正文独立构造支撑；程序检查与其一致。四式无“两真前提、假结论”。

独立脚本与[真实输出](../../reproduction/aristotle-prior-analytics-ii3/logs/independent-review.txt)已保存。复跑命令（在复现目录运行）：

```sh
python independent_check.py
python test_model.py
python -O test_model.py
python -OO test_model.py
```

独立脚本使用审查断言，须用普通 Python，不要以 `-O` 或 `-OO` 运行它；作者的生产语义验证与 unittest 测试不依赖可被优化删除的断言。独立脚本加载模型只为对比，预期计数和量词真值计算没有调用作者的 `evaluate`、`classify` 或 `census`。

## 证明边界

八类型压缩保留区域是否为空，因而保留 A/E/I/O 及混合状态；有限类型支持枚举与一般压缩证明分工明确。压缩不能保留计数约束，不能自动推广至模态、多元关系或经验词项事实。218的容斥计算与代码一致；最小见证指该外延语言中的对象数，不指古代自然语言最佳例子。

## 最终文件绑定

以下哈希覆盖正文、复现说明、作者代码/测试/命令、独立脚本及真实证据；审查文件不自哈希，以免循环。任何绑定文件改动均须重新核验。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-ii3.zh-CN.md`|`ab84636d6f02c8133dcdbce20288139f4dce61c5b7d1ca7fa1f22644df1a6c5c`|
|`reproduction/aristotle-prior-analytics-ii3/README.md`|`a81804335128407b8d82024d6dc6e6cf41197c2d24fcb725c8b2517297ec6585`|
|`reproduction/aristotle-prior-analytics-ii3/independent_check.py`|`92418bf38272f696edf11defb4169de0f4e8e744c31546ad649c4866c353f4a7`|
|`reproduction/aristotle-prior-analytics-ii3/logs/environment.txt`|`5cab1399044883727f9577895e8bb0b08d075ffc16a4727c8f41f18a54a8bffd`|
|`reproduction/aristotle-prior-analytics-ii3/logs/independent-review.txt`|`51805ab8c36c104ff92a156188785ba16d1d94b44d11867bd3dc9bda75973914`|
|`reproduction/aristotle-prior-analytics-ii3/logs/model-double_optimized.txt`|`3dc45b1a44ef5a8f96c1ad5cb3f8f7c7fb071c1605d56bdc25c8dd5cd214b349`|
|`reproduction/aristotle-prior-analytics-ii3/logs/model-normal.txt`|`a2658d242470b27a963b35442c83db49ffbe3e503028d0590239fde2184623a4`|
|`reproduction/aristotle-prior-analytics-ii3/logs/model-optimized.txt`|`3b41255e17d5e55402010832a3244685c0e0a2b8c364cf51a9587b9a76b73c7f`|
|`reproduction/aristotle-prior-analytics-ii3/logs/tests-double_optimized.txt`|`64f984c414089ff109f0676866b9529bd2cc2c6ca434d03f505830736cf631fa`|
|`reproduction/aristotle-prior-analytics-ii3/logs/tests-normal.txt`|`8882ff1f2c69072578a65be9685293903031c71dc61cbf705edeb612a3278da0`|
|`reproduction/aristotle-prior-analytics-ii3/logs/tests-optimized.txt`|`fac1b3a1547665b8fbbeed565d8fc5b3099df34440942ab302c29a2fff5d025d`|
|`reproduction/aristotle-prior-analytics-ii3/model.py`|`0af78a140b0abf4b6af997037d3112f3d18c034bbcb01522676e96991d71dbc6`|
|`reproduction/aristotle-prior-analytics-ii3/run.sh`|`d339d34f054f413cb3d0613f19dd6cbaa8cecbf52aba02a61a9bac83d24d5de2`|
|`reproduction/aristotle-prior-analytics-ii3/test_model.py`|`061ee283c84902856d968ab5891f8d9f2f082ca574871e32d75b6e49f2b09e5a`|
|`reproduction/aristotle-prior-analytics-ii3/witnesses.json`|`2b9a2cc217ce217905b1ad8f7e7de5497056cc4055dc39250aac62dec5acf570`|
