# I.45：换位归约与存在条件的最小教学复现

这是《前分析篇》I.45的**现代集合模型和受限证明证书重构**，不是古代程序复原。原文解释、一般推导和历史边界见[中文深读](../../papers/ancient/aristotle-prior-analytics-i45.zh-CN.md)。

## 语义与检查范围

接口 `Proposition(kind, subject, predicate)` 始终把主项放第二字段、谓项放第三字段。三项限于 `S`、`P`、`M` 且单个命题两项不同：

- A(S,P)：S包含于P，允许S为空。
- E(S,P)：S与P无共同对象。
- I(S,P)：存在同时属于S和P的对象。
- O(S,P)：存在属于S但不属于P的对象。

E与I可简单换位；A只能在其**原主项非空**时换成I(P,S)，不能换成A(P,S)。O不提供换位规则。存在条件是调用者显式声明的背景，不由程序认证其经验真实性。

`first_figure`只接受Barbara、Celarent、Darii、Ferio的明确项位；`Step`逐行引用已存在的前提或结论，允许换位和这四种第一格规则。`verify`要求末行精确等于目标。`reductio`只支持一个临时假设，要求最终目标恰为其矛盾否定，且指定两行构成A/O或E/I的精确矛盾。它不是通用证明搜索器，不解析自然语言，不判定其他证明系统是否存在证明。

给出的8份直接证书为Cesare、Camestres、Festino、Darapti、Datisi、Disamis、Felapton、Ferison归入第一格；Camestres和Disamis在最后还需分别换位E和I结论。Darapti与Felapton显式要求M非空。另2份Baroco与Bocardo证书使用临时假设加Barbara得到与原O前提冲突的A命题，再解除假设。

另外检查7组呈现变换：Celarent→Cesare、Ferio→Festino、Darii→Datisi、Ferio→Ferison、Festino→Ferison、Ferison→Festino、Felapton→Festino。最后一组使用A限量换位，仅保证原前提蕴涵新前提，**不保证前提等价**，但目标O结论保持。其余6组只用E/I换位，前提等价。

程序明确拒绝给Baroco或Bocardo的O前提换位。该失败只说明所请求的规则不被允许；它不证明任意直接证明都不可能，也不否定这两式的有效性。两式的反证证书恰好展示另一种证明方法。

## 为什么是128个模型

每个对象只由是否属于S、P、M的三位成员类型区分。去掉000型，剩7型。每型只记录“有／无”，故共2^7=128个模型；其中三项全非空的有109个。至少一个M对象的模型有120个。

在所声明的一元A/E/I/O语言中，重复同型对象不改变包含、排斥或见证存在的真假；000型对象也不影响这些命题。对任意原模型按成员类型压缩、反向每个在场类型放一个对象，逐种A/E/I/O可证明真假保持。这个**类型压缩论证**才支持将这些模型作为该受限语义的代表，日志数字本身不是证明。允许全空扩张不要求现实论域为空：放入一个000型对象也得到相同真值。

它不覆盖关系谓词、模态、数量等于二、不同对象的身份条件、古代存在承担的全部解释，不能裁定原章的唯一历史语义。

## 文件与复跑

- `model.py`：语义、换位规则、第一格规则、逐行证书、模型枚举、明确的示范证书。
- `test_model.py`：21项单元测试，覆盖输入错误、存在条件、引用范围、布尔下标、生成器输入、换位非等价和两种反证。
- `run_experiment.py`：14式、换位、呈现变换及具体反模型的真实枚举。
- `logs/`：实际环境、命令、三种优化模式下的测试和实验原始输出。

仅Python标准库，无第三方依赖。在此目录运行：

```sh
python3 -m unittest -v test_model.py
python3 run_experiment.py
python3 -O -m unittest -v test_model.py
python3 -O run_experiment.py
python3 -OO -m unittest -v test_model.py
python3 -OO run_experiment.py
```

核心输入与规则检查使用显式异常，不使用会被优化删除的 `assert` 语句。单元测试的 `self.assert...` 方法不受该优化影响。输入迭代器先整体验证，不靠前提短路掩盖后续非法输入。

## 本次真实结果

每模式21项测试通过，枚举128个类型模型。14式共1776次满足各自存在政策的式—模型检查，零反例；其中Darapti和Felapton各只接纳M非空的120个，其余12式各128个。另2256次换位—模型检查零失败，8份直接及2份反证证书全部通过。这些口径不同，不相加伪装成更多独立模型。

6组E/I呈现变换各在128模型上前提等价。Felapton→Festino在120个M非空模型上原前提都蕴涵新前提，但只有112个模型两组前提同真同假，因此没有宣称一般等价。程序给出非法A简单换位、O换位、删除Darapti/Felapton存在假设的具体反模型；其中删除存在假设时三项全空便足够。

|模式|测试|实验|
|---|---|---|
|普通|[真实测试日志](logs/tests-normal.txt)|[真实实验日志](logs/experiment-normal.txt)|
|`-O`|[真实测试日志](logs/tests-optimized.txt)|[真实实验日志](logs/experiment-optimized.txt)|
|`-OO`|[真实测试日志](logs/tests-double-optimized.txt)|[真实实验日志](logs/experiment-double-optimized.txt)|

[环境和执行命令](logs/environment.txt)与日志共同界定本次执行。修改源码后必须重跑，不能把这些旧结果冒充新运行。程序没有测量现代AI系统，也不以小实验证明所有数学定理。
