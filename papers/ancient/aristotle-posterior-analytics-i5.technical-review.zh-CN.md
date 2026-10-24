# 《后分析篇》I.5 独立数学与代码审查

## 结论与范围

**通过（修正后最终稿）**。审查完整正文、生产模型、测试、运行脚本与日志，并实际独立重跑。这里的通过是数学教学与有限程序规格核验，不是对古代全部文本解释、本质论、现实因果或首要知识的认证。

发现并已复核修正一项实质错误：原正文与练习把从ad=bc到a/c=b/d的除数写为bc，应为cd。当前第6节及练习7已一致改成cd，正有理数前提保证c、d不为零。源码与复现README原本采用正确比例关系，无须改动。

## 数学检查

1. 覆盖引理正确：任取目标元素，覆盖给出所属子类，再应用该类全称前提得到属性。允许重叠、空子类，且不要求每类有限。正文采用目标等于并集的充分条件；代码采用目标包含于并集的较弱覆盖要求，同时检查整个供给并集为真，仍足够推出目标为真。
2. 遗漏元素反例有效；供给类太宽时证书可能失败而目标仍真，代码与README明确区分。
3. 三角形分类讨论的形式有效性，与作为共同主项的解释知识是不同任务。正文没有把原文批评误写成分类讨论失效。
4. 同外延标签不固定本质或解释作用；程序保留名称差异及空类，没有输出“真正本质”。
5. 平行线补全保留欧氏同平面、同截线、适当内错角位置等条件，不把任意相等角误当充分条件。
6. 比例交换在正有理数域正确。修正后的乘bd、除cd步骤可直接一般证明，有限运行不替代该证明。浮点、布尔、零负数被拒绝，Fraction输入准确计算。
7. 支持集是外部声明的充分路线，不是程序读取完整证明后验证的依赖。无路线不推出目标假；有路线不认证声明正确。正文和附件均限定这一点。
8. 删除铜制、等腰限定是给定几何论证的条件检查，不是物理拆除；正文保留固定欧氏背景，也未把一份证明未用条件升格为所有证明均不用。
9. 练习答案与例子一致；数值范围、测试计数与真实结果一致。当前模型不测性能、不用统计数据集，也没有声称复现古代一般量理论。

## 独立运行

独立脚本：[independent_check.py](../../reproduction/aristotle-posterior-analytics-i5/audit/independent_check.py)。在复现目录运行：

```bash
python audit/independent_check.py
python -O audit/independent_check.py
python -OO audit/independent_check.py
python -m unittest -v test_model
python -O -m unittest -v test_model
python -OO -m unittest -v test_model
```

实际CPython3.12.14标准库执行。每个模式6项独立unittest通过；另重跑23项生产测试，各模式通过。独立测试用unittest断言，不使用会被优化删除的assert语句。

每模式的独立检查：

- 4096份覆盖报告的全部8字段逐一与set实现比较；512份外延证书，零差异。
- 512组双路线支持/保留输入，不只生产枚举的单路线64组；逐标签成员检查零差异。
- 512组具名候选输入，包含同外延及空类；零差异。
- 从分子分母1到3形成7个不同正有理数，2401个四元组，以分子分母整数交叉积独立判定两比例式；175个等式真，零差异。
- 每个比例参数位置的越界输入与零对象域等边界测试通过。
- 生产枚举实际重算并与results.json一致：4096覆盖、64支持、1296整数四元组、86个比例前提真；各差异/反例0。

独立日志：[normal](../../reproduction/aristotle-posterior-analytics-i5/audit/check-normal.log)、[-O](../../reproduction/aristotle-posterior-analytics-i5/audit/check-O.log)、[-OO](../../reproduction/aristotle-posterior-analytics-i5/audit/check-OO.log)。生产重跑日志：[normal](../../reproduction/aristotle-posterior-analytics-i5/audit/replay-normal.log)、[-O](../../reproduction/aristotle-posterior-analytics-i5/audit/replay-O.log)、[-OO](../../reproduction/aristotle-posterior-analytics-i5/audit/replay-OO.log)。所有日志来自实际命令；耗时只是此次运行记录，不是基准测试结果。

## 最终显示修订复核

覆盖公式仅删除量词i后用于排版的间距命令，保留括号内子类包含关系。将该间距命令还原后SHA256与上一已审正文完全一致；当前公式仍表达同一覆盖引理，数学结论及全部源码未变。复核通过，以下正文哈希已更新。此复核不冒称本人完成浏览器显示验收。

## 最终文件绑定

下列SHA256绑定本次核验对象；后续正文或代码改动需重新审查。公式网页实际显示由发布验收另行检查，本审查不冒称已检查远端渲染。

| 文件 | SHA256 |
| --- | --- |
| papers/ancient/aristotle-posterior-analytics-i5.zh-CN.md | `21338503d487b2c7de9d1e2e2acfac362c98f2500fa354c3f8825ef67e193a51` |
| reproduction/aristotle-posterior-analytics-i5/model.py | `9ee0c844af589a14424dab4853a1716f997e4ca84304f28937ce354375df3d62` |
| reproduction/aristotle-posterior-analytics-i5/test_model.py | `eed1c5c7577781b340e0eacc238d96a9074312e2af732cda2eb6af333bfbdadd` |
| reproduction/aristotle-posterior-analytics-i5/run.sh | `faa48e59ddc3fee8e32af10b4f0ef37d1923d14842ad8e92c9d930f6537237af` |
| reproduction/aristotle-posterior-analytics-i5/README.md | `33f572c485946f302c6dab31c5b96f5c4860fba1656e30de3ba91700be6c3c13` |
| reproduction/aristotle-posterior-analytics-i5/results.json | `23d046ed6e0993889f4a67db640badb4f6e501030831ba019417b12d5f430a2a` |
| reproduction/aristotle-posterior-analytics-i5/audit/independent_check.py | `15a32bb39b65617915d5db6c4bff71109dd5da9e35c829bd3eaa1312539245d9` |
