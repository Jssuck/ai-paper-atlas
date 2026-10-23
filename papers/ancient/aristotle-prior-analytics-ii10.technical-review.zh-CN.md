# 《前分析篇》II.10：独立数学与代码审查

## 审查角色与范围

本审查者未编写被审正文及生产求值器 `check.py`，独立重建六个第三格式和结论替换的24条路径。来源校读另见[独立来源审查](aristotle-prior-analytics-ii10.source-audit.zh-CN.md)；本报告不把程序结果当作古文版本证明。

审查对象是[深读正文](aristotle-prior-analytics-ii10.zh-CN.md)的现代一元集合重构及[复现目录](../../reproduction/aristotle-prior-analytics-ii10/README.md)。没有审查古代唯一语义、全书、自然语言解析器、模态逻辑或现实中的原因知识。

## 数学核验

1. **方向和表项：** 正文U与代码A都表示“主项包含于谓项”；第三格中项C，AC为大前提、BC为小前提。六式及12条矛盾替换结果逐一核对，没有把II.9的字母角色搬来。
2. **一般证明：** 肯定三式的新E(A,B)排除A/B共同对象；否定三式的新U(A,B)使B中对象全部进入A。正文逐个保留前提再选任意对象或存在见证，所得分别与六式表一致。Disamis、Bocardo标作教学补全，不冒充原文逐式展开。
3. **存在条件：** Darapti、Felapton依赖C非空，其他四式从特称前提取见证。空C时全称所得仍成立，但不能把它与目标全称句的不相容当成无条件事实。这与“所得有效”和“目标被反驳”两个指标分开一致。
4. **失败反例：** 正三式用共同的非空模型保留原结论I和替换O；负三式用另一个共同非空模型保留O和替换I。两个原前提同时真，故两种保留方向均不能反驳，且不是空项漏洞。
5. **强度边界：** Datisi、Disamis的O不能无条件升级成E；Ferison的I不能升级成U；Bocardo的O不能升级成E。正文四个实例逐个代入为真反例，并纳入独立检查器。
6. **不能过度概括：** 指定目标方向的AEIO均不必然，不等于完全没有后果。Darapti反对替换保留AC可有反向O(C,B)；生产结果另外输出反向形式，测试覆盖此边界。
7. **证明依赖：** 两前提分别可反驳意味着两个条件背景，而非一次把二者同时宣告为假。第4节一般诊断式必须保留原推导存在假设。章末格位表为结构路线，不是任意背景有效性的保证。
8. **模型压缩：** 三个一元谓词产生八种真假类型；U/E只约束某类对象不存在，I/O只约束其存在，故同类型对象数目不影响该语言真值。有限枚举仍不能自行证明超出模型语言的古代解释；正文的一般见证推导承担任意集合层面的论证。

## 独立实现与真实实跑

审查者编写[独立检查器](../../reproduction/aristotle-prior-analytics-ii10/independent_check.py)，**不导入生产求值器**，用逐对象量词 `all` / `any` 和布尔三元组重建真值，独立生成占据类型。生产程序用集合包含、交集和差集。两者共享待检验的明确数学定义，不声称这种差异足以排除所有共同建模错误。

核验内容不止PASS标记：逐一比较全部背景数、反驳反例数、目标及反向四式后果、六式原推导；重放结构化证据中的全部首个共存反例，核集合编码。生产 `results.json` 重新生成，与保存版本逐字一致；另重新执行生产12项单元测试通过。

实际执行：

```sh
python3 independent_check.py > independent-normal.log
python3 -O independent_check.py > independent-O.log
python3 -OO independent_check.py > independent-OO.log
```

[normal日志](../../reproduction/aristotle-prior-analytics-ii10/independent-normal.log)、[-O日志](../../reproduction/aristotle-prior-analytics-ii10/independent-O.log)、[-OO日志](../../reproduction/aristotle-prior-analytics-ii10/independent-OO.log)均通过：

- 72个替换路径—政策组合，18个原式—政策组合，40个首个共存反例重放；
- 6个原式统一共存实例，4个不可升级实例，1个现代故意错换项的反例；该错项示例**不归为Owen印本错误**；
- 允许空项、仅C非空、三项均非空的模型数分别为255、240、218；真正反驳路径数分别8、12、12（每政策共24条）；
- 每个保留前提与替换命题组成的背景均有模型，没有依靠背景不相容而真空成立的路径。

独立检查采用显式异常，不使用会被优化删除的裸 `assert`。生产单元测试用 `unittest`；12项测试也在normal、`-O`、`-OO`三模式运行。核对非法掩码、布尔/浮点输入、范围、命题种类及政策名的防护；这不是对任意外部恶意对象的安全审计。无第三方依赖、网络或随机过程。

## 结论与边界

数学建模、逐步证明、实例、练习答案及运行结果在声明的语义范围内一致。没有发现需要改变生产数学算法的错误。来源转录、实际GitHub公式渲染和远端发布状态另由相应核验负责，本地审查通过不等于发布已经完成。

## 核验版本

以下SHA-256绑定实际审查的文件字节；不是Git提交ID。后续修改正文或源码时须重新核对相关内容。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-ii10.zh-CN.md`|`62af05dd3807013a492f561d2a8147ac8f1b9bfcb121616d5542477771bc312d`|
|`reproduction/aristotle-prior-analytics-ii10/check.py`|`d77c75bc82d86b1503ce6036205bbb744633943a1ba96719aa1dd90e17f26731`|
|`reproduction/aristotle-prior-analytics-ii10/test_check.py`|`c05c18f31ce882be43db59f9ca74d1fd30e84913bf1cef4f64bc1eb3c4b31282`|
|`reproduction/aristotle-prior-analytics-ii10/run.sh`|`f085258350f3686716143110c757a0a9c5d447c3adbcff7590512e661697f9c6`|
|`reproduction/aristotle-prior-analytics-ii10/results.json`|`ee32731da861718172dd8f1f567655fbe356ddef863169ca4545f777f16c96c3`|
|`reproduction/aristotle-prior-analytics-ii10/independent_check.py`|`106b40a76abee85b0533a582fd3e3645cbf6129dd6b9cc78996c52b44647a9bb`|
