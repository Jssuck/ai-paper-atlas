# I.36：独立数学与代码核验

## 结论和审查范围

对修订后正文及当前教学实现，未发现未解决的数学或规则实现错误，允许在本文限定范围内作为教学附件发布。审查独立于主文作者及模型作者，未修改模型源码；新增独立验证程序。此结论不代替来源专审、远端提交核验或GitHub公式实际显示检查。

实际阅读主文全部论证与练习，检查`model.py`、`test_model.py`、`verify.py`、`run_checks.py`和复现README，并目视Owen印160末–162的本章正文及译注。来源版本和章界的完整复核另见[来源审查](../../papers/ancient/aristotle-prior-analytics-i36.source-audit.zh-CN.md)。

## 数学逐项意见

1. 知识见证与其对象的槽位保持正确。S(w)与R(w,g)只能直接推出关于g存在知识，不推出S(g)，也不单凭这两条推出非S(g)。正文同时给出正反独立性，避免把“不蕴涵”误作“蕴涵否定”。
2. 类包含到投影的实例化、两个“有属／是属”大前提的区分正确。共同知识见证与逐对象分别存在未混淆；共同存在不被误说成唯一存在。
3. 生成与笑的符号例被明确处理为条件论证。投影与原类排斥支持否定归类；仅无自环不够，正文两对象反模型确实保留前提并否定错误结论。
4. 神例只得到差集见证和非包含，因此非同一；未增强为不交或反向非包含。加入共同成员的反模型正确。
5. 任意论域上的投影单调性证明、逆命题反模型、交集单向包含证明及反向反模型均正确。空类允许，不误添存在假设。
6. 五条实现规则均保真。证书可靠性可对步骤数归纳；它只相对于给定真实前提成立，不保证材料真实性、相容性、完备性或自然语言翻译正确。代码依赖引用必须向后，已排除布尔值充整数。

## 审查要求与修正

初审建议：正文7.3原先概述逐规则可证明，但未全部展开。作者已补`project`、`instantiate`、`transitive`、`exclude`、`difference`五项一般理由，特别明确空类、排斥输入顺序与差集结论强度。终审重读新增证明通过。没有要求或实施模型算法修正；不能把说明补足记录成发现并修复了不存在的代码缺陷。

## 独立程序与真实结果

[独立脚本](independent_audit.py)采用整数位向量与两张独立有向关系矩阵计算期望值，而非调用被审实现的`extension/true`生成期望结果，也不复用原作者`verify.py`的量词oracle。枚举一对象和两对象论域、两个任意原子类、两个任意关系；使用两个原子、两种一层投影及一项二层投影的五表达式。规则输出可再增加一层，仍以独立位运算解释。

三模式均真实执行成功，且结果逐字段相同：

- 4112个模型，423280次语义比较；
- 401796个真前提规则实例，全部结论成立；
- 12856次单调性／交集单向包含的有限实例检查；
- 24项格式、伪造结论、错关系、错见证、负数／向前／布尔／浮点引用、未知解释及非法模型输入全部抛出预期`Invalid`；
- 8个独立反模型通过，覆盖原附件五类错误，额外包括无自环不足、投影交集逆向失败及单调性逆向失败；
- 独立复跑原13项单元测试，在正常、`-O`、`-OO`模式均通过。

复跑命令（在本目录）：

```sh
python3 independent_audit.py
python3 -O independent_audit.py
python3 -OO independent_audit.py
python3 -m unittest -v
python3 -O -m unittest -v
python3 -OO -m unittest -v
```

原始输出：[正常oracle](independent-logs/normal.json)、[优化oracle](independent-logs/optimized.json)、[双优化oracle](independent-logs/double-optimized.json)、[正常测试](independent-logs/normal-tests.txt)、[优化测试](independent-logs/optimized-tests.txt)、[双优化测试](independent-logs/double-optimized-tests.txt)、[环境和命令](independent-logs/environment.json)。不含私人路径、账户或密钥。

## 范围和剩余限制

有限枚举不是一般定理证明，也未穷举任意语法深度或更大论域。Python递归表达式验证未声明对恶意超深结构提供资源限额；它是本地教学程序，不是公开网络服务或不可信代码沙箱。证书核验信任前提，不自动进行事实核实；模型求真则采用完整有限解释，不是开放世界知识库。固定关系的槽位不能通过改名、反转或词形归一化偷偷改变。本文没有认证神学、心理学或符号系统的经验前提。


### 发布显示增量修正

发布核验阶段报告复现README中部分紧邻中文标点的普通行内数学未渲染。作者将该文件全部行内数学定界改为GitHub支持的反引号包裹形式；独立复核实际新文件，并将这些定界符逆变换后计算摘要，精确恢复此前已审README的SHA-256。因此本次变化仅是行内数学标记，不改变文字、公式、算法或运行结果；新README摘要已更新如下。实际远端显示终态仍由发布流程另行确认，本审查不冒充浏览器视觉核验。

## 终审文件绑定（SHA-256）

以下为本次终审读到并核验的实际文件。若被绑定文件变更，应重新核查受影响部分，不得沿用本记录声称新版已审。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-i36.zh-CN.md`|`bb59922072cbf440d2fcb892d1bd7816b02e01ae363b1cf330e712dd718fdbc5`|
|`reproduction/aristotle-prior-analytics-i36/model.py`|`c0e87d3ac4ca79d4c1fe5e7eac87286d6e7fa0fae4d60dbaa51466a8cca52df1`|
|`reproduction/aristotle-prior-analytics-i36/test_model.py`|`90e6138d8caa3a72f5d67eda1cc882278d866780ffc69e3c4b261abd3933b372`|
|`reproduction/aristotle-prior-analytics-i36/verify.py`|`2c44824f65f13186501f0d60a8b251964f8d12b5329ed7261fa83552161b692f`|
|`reproduction/aristotle-prior-analytics-i36/run_checks.py`|`c9fbdc996aeb50645e6ae16a57926fcb25d560d13ca7da68b43be9f7d89956aa`|
|`reproduction/aristotle-prior-analytics-i36/README.md`|`43ce6b1fbee41d3f65cb0fafac230528120e1d47a48d16e7e48ac1b906dd7511`|
|`reproduction/aristotle-prior-analytics-i36/independent_audit.py`|`eb8fac16c3971ffcdade17774aa69d544b1321952fe5b96425208920aa2f8820`|
