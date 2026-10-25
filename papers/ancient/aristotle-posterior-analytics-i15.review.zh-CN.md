# 《后分析篇》I.15：独立数学与代码审查

## 结论与范围

结论：本次冻结版本通过数学与实现核验。审查者独立阅读正文、源码、测试、运行脚本、复现说明与保存日志，并另行运行三个解释器模式；没有以作者的测试结论代替复跑。原典版本和章界由单独的来源审查负责，本报告不冒充校勘报告。

## 逐项检查

- Camestres、Celarent、Cesare的关系式与逐元素证明正确；No对称不等于All可换位。正文All的主项—谓项顺序与代码all_of的谓项—主项顺序已经显式区别。
- “不包含”不蕴涵“不相交”、两否定前提不足、第三格特称否定不推出全称否定，各反例均满足其声称的前提和失败结论。
- 两端无合格上属的反证保留否定关系已给定及前三格体系范围，没有变成任意现代逻辑的不可证明性结论。
- witnesses的准入规则是排除端项同外延候选的教学约定，不是科学属关系定义；添加补集改变词表搜索结果不等于找到独立科学原因。
- 代码使用unittest检查方法，无依赖会在-O中消失的assert语句。run.sh错误即停止，三模式日志和results.json可从所附命令再生。

## 独立实跑

在CPython 3.12.14下，从复现目录分别执行：

```sh
python -B -m unittest -v test_model
python -O -B -m unittest -v test_model
python -OO -B -m unittest -v test_model
python -B model.py
```

三个模式各10项测试全部通过。重新生成的JSON与发布results.json逐字一致；发布日志未被审查复跑覆盖。另用独立的整数位掩码实现枚举四元素论域，不调用model.py的关系函数，三个论式分别得到256个前提真赋值、110个全部项非空赋值和0个反例，与附件一致。每式总赋值数为16的三次方，即4096。

## 保留边界

本次认可的是默认四元素论域的结果、三元素第三格测试和正文的一般集合证明；不将有限枚举提升为历史科学直接性的证明。audit(n)的计数循环可改变论域大小，但附带的固定教学示例包含元素0、1、2、3，不是随n自动缩放的实例；若缩小论域，须另行调整并审查示例。本篇未声称已验证任意n的整个结果报告。未实现完整证明搜索、因果、本质或模态语义。

## 冻结文件 SHA256

以下哈希覆盖实际审查的最终字节；任何正文、代码、说明、环境或日志变更均需重新核验。哈希不代表已经完成远端发布或浏览器公式显示验证。排除自动生成的__pycache__。

|仓库路径|SHA256|
|---|---|
|`README.md`|`1c719f143876de51218e942204f16858695b6e13498938fcd2a611bd70ade350`|
|`papers/ancient/aristotle-posterior-analytics-i15.zh-CN.md`|`14455f11a210b2dbb63af06c8448c77b7aebbf248d0c143cf423480472693b64`|
|`reproduction/aristotle-posterior-analytics-i15/README.md`|`7168db50c5df34a0224cbd1ba70b45826e43ec27b3526407ed99ac08f6c98c8f`|
|`reproduction/aristotle-posterior-analytics-i15/logs/environment.log`|`6445f5f526b1c338bbd976271216034b2fa1727ddea98aa7e512ac38ea0c4c7e`|
|`reproduction/aristotle-posterior-analytics-i15/logs/tests-O.log`|`f770dba181a454447f32816091e8d55126db9b38af1b03a0bc96be23b278026e`|
|`reproduction/aristotle-posterior-analytics-i15/logs/tests-OO.log`|`9db9813af7532b6d5b1f802e96fcad5cf04c669803cc76c0e920b05220ed167a`|
|`reproduction/aristotle-posterior-analytics-i15/logs/tests-normal.log`|`015b1573c22713c944440d24b81d3b2f89732386f33619bee6b555f55a427951`|
|`reproduction/aristotle-posterior-analytics-i15/model.py`|`f10acb2c922c79cea2253786b93fe0c6301633c6c90c36c8f230f36eb093f5e7`|
|`reproduction/aristotle-posterior-analytics-i15/results.json`|`04686bc2e022795e13a47d7e969d5f71a7c22aba9c272ae18d6f82b7e6341be2`|
|`reproduction/aristotle-posterior-analytics-i15/run.sh`|`b5dccacc38ff28878adaef120eed2d458f66584affaf86544928ff3f04960437`|
|`reproduction/aristotle-posterior-analytics-i15/test_model.py`|`6de86b80cd49a0cbb8b8c81c4398c8802914efc11226bf2c1d3e850df07f1351`|
