# I.38 独立数学与代码核验

## 结论

修正一处“同外延意味着同真”的措辞后，正文的包含传递证明、改变中项／结论标签的反模型与教学代码一致。第二段新增的特有本性中项 F_g 链明确保留两条前提的真值责任，不把标签当本质计算算子。当前范围内未发现数学或代码阻断项。

本报告不裁定希腊异文，来源核验另见来源报告。认识谓词是不透明标签，不是认知主体的知识模态，没有内置因果或自然语言解析。有限验证不证明原章的唯一解释，不代替任意集合上的一般论证。

## 实际审查

- 逐读主稿、model.py、run_checks.py、test_model.py、复现README及原运行输出。
- 一般证明：任取C对象，依C包含于B进入B，再依B包含于A进入A。允许空主项，不自动给出存在见证；此推导不依赖有限枚举。
- 主稿单对象的错误结论标签反模型成立；错误中项的单对象及双对象非空反模型均成立。额外桥接作为新前提而非免费改写，界限正确。
- 完整标签参与结构匹配，端点方向和目标匹配均检查。形状接受与前提为真分开；形状拒绝不推出目标为假。
- 缺失外延抛KeyError而非被当作空集；域外元素、无效标签、非法边／证书类型受检查。输入集合被复制为frozenset。模型公开字典仍可被调用方修改，故此处只核文档所述构造与查询用法，不声称防恶意篡改、不可变安全沙箱或资源耗尽保护。

## 独立实跑

自有 independent_audit.py 使用整数位掩码与按位包含关系作独立oracle，不调用生产版subsets函数生成外延或判定包含。将结果逐项与Model.holds对照，再比较生产枚举汇总。

|项目|三种模式一致结果|
|---|---|
|三项模型／满足前提|585／85|
|四项模型|4369|
|偷换大项／中项反模型|185／235|
|限定与无附加限定两个方向反模型|45／45|
|API真值与独立位掩码对照|69904次|
|证书六个端点的全部标签组合|4096种|
|原单测重跑|各20项通过|
|相同外延但两结论皆假的回归|通过|
|check(False)不会被优化删除|通过|

正常、-O、-OO均实跑，结果分别见 [normal](logs/independent-normal.json)、[-O](logs/independent-O.json)、[-OO](logs/independent-OO.json)；单测独立重跑见 [normal](logs/independent-tests-normal.txt)、[-O](logs/independent-tests-O.txt)、[-OO](logs/independent-tests-OO.txt)。在本复现目录实际执行：

    python independent_audit.py
    python -O independent_audit.py
    python -OO independent_audit.py
    python -m unittest -v
    python -O -m unittest -v
    python -OO -m unittest -v

这些计数覆盖域大小0至3的所述解释与有限标签组合，绝非无限模型检查、自然语言准确率或全套三段论复现。

## 已修正问题

原稿“两个谓词同外延只能使两结论同真”可能把相同真值误说成皆真。作者改成“具有相同真值”。独立检查新增主项非空、两个谓词均为空的例子：两个结论同时为假，说明修正必要性。没有修改生产模型或测试来掩盖失败。

## 审查绑定 SHA-256

以下摘要绑定实际审过的文件，不把摘要当审查本身；报告自身不作循环摘要。相关内容再改需复核并更新。

    c2e05652b0332229091dd53ea85ac8a1398cfb274b805078364bf2adc0a4c5a5  ../../papers/ancient/aristotle-prior-analytics-i38.zh-CN.md
    25498c374ecd9034d36ed7b026ec0b07f942bc8aff24a1849737fbb0616f5828  model.py
    a0e2bf7d962981d13c270f3de73e41fff4fbf19041e1789ebaf8b3b9d3186699  run_checks.py
    b4db233b1f195c84dd18cb531a6d4a0d1d1a56b463b3c44acfb950133bd28059  test_model.py
    1ba70112a1193984e81b747a4a342040e21b913e9502ac83ba2740ddd21b6225  README.md
    4dc8d0da4c59580aa4f97e9b466f5725084a9f6427b2836657080d945785bcb3  independent_audit.py
    504f01ac053d15d48996a4f82855274d2dd90f7939afb793f821fef08f944971  logs/checks-O.json
    504f01ac053d15d48996a4f82855274d2dd90f7939afb793f821fef08f944971  logs/checks-OO.json
    504f01ac053d15d48996a4f82855274d2dd90f7939afb793f821fef08f944971  logs/checks-normal.json
    4fdbd0345875e1b97be7f5951a63f529af94c2cbeeedea4bdc8c99390c68515b  logs/environment.txt
    3796ff72fd891e2ba2e9556f403ca9322653301e0dcd2f0bac01112c2ab3f66f  logs/independent-O.json
    3796ff72fd891e2ba2e9556f403ca9322653301e0dcd2f0bac01112c2ab3f66f  logs/independent-OO.json
    3796ff72fd891e2ba2e9556f403ca9322653301e0dcd2f0bac01112c2ab3f66f  logs/independent-normal.json
    da7568024791af589fcce7ada3e5c658c4c8b39bf16de28f1a0c802656374df6  logs/independent-tests-O.txt
    e943ea68ecad93b30ae36e714d4d62a2b79ea5f8a73cf76d12ff60b872481bc6  logs/independent-tests-OO.txt
    e943ea68ecad93b30ae36e714d4d62a2b79ea5f8a73cf76d12ff60b872481bc6  logs/independent-tests-normal.txt
    da7568024791af589fcce7ada3e5c658c4c8b39bf16de28f1a0c802656374df6  logs/tests-O.txt
    da7568024791af589fcce7ada3e5c658c4c8b39bf16de28f1a0c802656374df6  logs/tests-OO.txt
    da7568024791af589fcce7ada3e5c658c4c8b39bf16de28f1a0c802656374df6  logs/tests-normal.txt
