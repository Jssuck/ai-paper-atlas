# I.46：独立数学与代码核验

## 审查范围与方法

本报告由未编写作者模型的独立审查者进行：分别检查一般集合推导、模型接口及输入校验，并写出独立逐对象真值oracle。源码、作者单测、穷举脚本、README和真实日志均在范围内；正文最终绑定见末节。没有远端操作，不以作者测试成功替代独立检查。

有限程序只验证明确模型和实现，不认证“善”“不等”等词的古代唯一语义，不证明经验事实，也不把现代空域/空情境边界强加给原文。

## 一般数学检查

### 适用域图

设 P⊆T⊆U，A=P，B=U−P，C=T−P，D=U−C。

- 任取x∈C，x∈T且x∉P，故x∈B；所以C⊆B。
- 任取x∈A，则x∈P而不可能在T−P，故x∈D；所以A⊆D。
- A∩C为空，因为同一个x不能既在P又不在P。
- x∈B∩D等于x∉P且x∉(T−P)。在x∉P的条件下，后一项等于x∉T，故B∩D=U−T。
- 同样B−C=D−A=U−T。因此两对外延相等当且仅当T=U；若T真包含于U，论域外于T的对象是严格性见证。这里“外于T”仍是U内对象，不是不存在对象。

这组论证对任意集合成立，不依赖穷举大小上限。

### 补集反序与字母重置

另设C⊆A⊆U，B=U−A，D=U−C。若x∈B而x∉D，则x∈C⊆A，与x∉A冲突，因此B⊆D。如果C⊊A，取y∈A−C，则y∈D−B，故B⊊D，反向D⊆B失败。A∩D=A−C，而B∩C为空。第二模型的字母意义与前一图不同，不能把前一图的C⊆B移到这里。

### 联合否定

F=U−(A∪B)表示既非A又非B；U−A才是单独对A的否定。当A、B恰互补，F为空。于是A∪F=U仅在A=U时成立，不能在一般证明中当作排中前提。空集本身不是错误；错误在于给它赋予了未经核实的互补关系。

### 量词和模态

“并非所有S是P”为存在x∈S且x∉P，与“所有S都不在P”不同。混合主项提供反例；空S时全称和全称否定都真，存在反例为假。能力示例采用现代可达情境：有可行走情境和有不可行走情境可同时成立；没有可行走情境不等于有不可行走情境。两个情境[True,False]已显示差别；零情境只用于实现边界测试。

## 代码审查与独立测试

未发现需要修正的作者源码错误。正文审查修正了将联合否定误称为“否定合取”的一句描述，改为否定析取；并澄清覆盖断言的极端边界、练习6的T≠U条件、练习15的空U退化以及数学数字标记与字符串API的区别。集合先完整物化、校验后计算，避免生成器重复消费和空主项短路绕过输入检查；严格区分bool和整数；非法论域元素、论域外元素及违反包含条件均被拒绝。运行检查使用显式异常，在优化模式仍生效。

独立程序[独立测试](independent_test.py)不调用作者的subsets进行主要枚举，而以每个对象的2/3/4状态构造oracle；测试作者API输出是否逐点符合期望。另覆盖联合否定的全部三对象双谓词真值组合、生成器与输入边界。

实际运行命令：

```sh
python3 independent_test.py
python3 -O independent_test.py
python3 -OO independent_test.py
```

三种模式各10项测试通过，真实日志：[normal](logs/independent-normal.log)、[-O](logs/independent-O.log)、[-OO](logs/independent-OO.log)。每模式分别核验：

|类别|独立范围|模型数|
|---|---|---:|
|适用域|U大小0至6，逐对象三状态|1093|
|包含反序|U大小0至6，逐对象三状态|1093|
|量词|U大小0至6，逐对象四状态|5461|
|可达情境|长度0至6的布尔序列|127|

不同Python模式不相加为更多数学模型。作者22项测试和穷举统计亦已核对；以上独立数量采用稍大的上限，并不等同于更一般的定理证明。

## 最终文件绑定

最终审查通过。下列SHA-256绑定本次实际审阅与实跑的字节；后续内容或排版修改须重审受影响部分并重绑定。

|文件（相对仓库根）|SHA-256|
|---|---|
|papers/ancient/aristotle-prior-analytics-i46.zh-CN.md|17a8e3dce29e883073f79878344da9283561fe0fc1c50071daf220f9c2a75e3f|
|reproduction/aristotle-prior-analytics-i46/README.md|ccab10c0a98839ee39942a2fc373486a96a73ddac1d1e3e02aa48979042ae2e6|
|reproduction/aristotle-prior-analytics-i46/model.py|dc7cb15c2fc5695ad3637518518a779c310f85c871855089f6a7475d6ac6c77e|
|reproduction/aristotle-prior-analytics-i46/test_model.py|763520afc3b27f6c229f3d2602ad8ef2e15eb894d38147d57ac38ddd51340310|
|reproduction/aristotle-prior-analytics-i46/run_experiment.py|2e220fe3fd715bfb48573613720c687c298424577c9ccca04863623b59a8c7ef|
|reproduction/aristotle-prior-analytics-i46/independent_test.py|3c2d0f5b3a4e95dc8e51d7d909ec58b49cea54fccdc95ba7f635dabe375c94ef|
|reproduction/aristotle-prior-analytics-i46/logs/environment.txt|37ba3748a8cae6b04199c9489b41fde843f709853fbb72ac247e1cabfbed5209|
|reproduction/aristotle-prior-analytics-i46/logs/experiment-O.log|1ba36d05da55e3ca944840de3ef1794fe3c47afa8a6cb4433df88f3eddcf75c2|
|reproduction/aristotle-prior-analytics-i46/logs/experiment-OO.log|1ba36d05da55e3ca944840de3ef1794fe3c47afa8a6cb4433df88f3eddcf75c2|
|reproduction/aristotle-prior-analytics-i46/logs/experiment-normal.log|1ba36d05da55e3ca944840de3ef1794fe3c47afa8a6cb4433df88f3eddcf75c2|
|reproduction/aristotle-prior-analytics-i46/logs/independent-O.log|8de3871afa96383acded391b44c8c81b8e457f003c637917b3dd78754f73e707|
|reproduction/aristotle-prior-analytics-i46/logs/independent-OO.log|5a80fa467bb88050a610a69d1baabec3f42f929581d723e5c18394d7bb5f1f42|
|reproduction/aristotle-prior-analytics-i46/logs/independent-normal.log|551deb7a938fc1483bbfa6d392cc5213fda0b99a204d2c801392d4ab56906602|
|reproduction/aristotle-prior-analytics-i46/logs/test-O.log|d2a0513c4e05b050e55c42eb2ef30bdecf077ccd986e5947979554555c6863d6|
|reproduction/aristotle-prior-analytics-i46/logs/test-OO.log|d2a0513c4e05b050e55c42eb2ef30bdecf077ccd986e5947979554555c6863d6|
|reproduction/aristotle-prior-analytics-i46/logs/test-normal.log|d2a0513c4e05b050e55c42eb2ef30bdecf077ccd986e5947979554555c6863d6|
