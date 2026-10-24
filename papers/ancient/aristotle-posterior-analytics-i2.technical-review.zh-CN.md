# 《后分析篇》I.2：独立数学与代码核验

本报告由未编写生产程序的审查者实际读取[最终正文](aristotle-posterior-analytics-i2.zh-CN.md)、生产源码、结果及说明，并执行自己的边界与枚举检查。审查对象是现代教学重构的内部正确性，不认证古代学说全部正确，也不认证现实因果知识。

## 结论与修正

最终版本通过本报告所列范围的核验。正文已明确“全部或某些”原理与程序“每个前提严格更高”加强政策不同；概率算例限定为固定分量p，避免“任一”为析取的歧义；定义空外延核验由本次独立脚本实际补充。最终正文、代码、结果字节摘要见末表。排版复核后仅在加粗冒号标记后加入空格；逆向移除这些空格可精确还原先前已审正文的摘要，技术内容与生产代码均未变，原真实运行日志继续适用，未声称另有重跑。

## 数学检查

1. 第5节蕴涵定义与modus ponens的一般语义证明正确，前提实际真与形式有效性分开。
2. 固定真值结构而改变额外解释关系E，确实说明仅有该形式语言的蕴涵信息不足以识别E。正文正确限制为扩展结构的教学论证，并未把它升级为真实因果领域的普遍不可能定理。
3. 假前提、真结论例不反驳保真有效性；同真值而双向蕴涵也不生成任何解释方向。
4. U、D都为空且论域非空时，全称双条件真而存在式假；独立脚本核验大小1、2、3的论域，正文的任意论域构造才是一般理由。
5. 不可公度补证依赖既定欧氏几何与整数最简比、奇偶性质；奇数平方仍奇的桥梁写明，推导没有用有限小数代替无理性证明。
6. 均匀四种真值组合中合取概率1/4，固定分量p概率1/2；这是另一度量语境的算例，正文未宣称它直接否定古代知识规范。
7. 先后/熟悉/原因/真假并未在代码中合并；元数据来源是外部声明而非程序的事实发现。
8. 六项原文要求被描述为必要要求，不是自动充分认证器；程序始终返回scientific_knowledge_certified=False。此False意为不予认证，不是证明对象必然没有知识。
9. 第一与直接、引理与基础的层次有区分；有限搜索失败没有被偷换成不存在更先根据。
10. 定义/假设分类明确预设“直接起点”，False表示否认存在仍属假设，None才是不作存在断言。

## 代码与实际运行

生产代码使用8个赋值的真值集合mask。entails用交集与补集，独立审查用由二进制字符构造的集合差计算，并独立比较counterworlds。生产exhaustive.py是作者自检算法，不冒充本报告的独立审查。

实际执行命令（在复现目录）：

```sh
python3 -m unittest -v test_model.py
python3 -O -m unittest -v test_model.py
python3 -OO -m unittest -v test_model.py
python3 audit/independent_checks.py
python3 -O audit/independent_checks.py
python3 -OO audit/independent_checks.py
```

- 生产18项测试在三模式均通过。
- 独立6项测试在三模式均通过。
- 每模式检查65,536个单前提mask对，6,561对有效，反世界集合与有效性均无差异。3^8计数来自每世界允许三种(p,q)组合。
- 每模式另核4,096个双前提情形（mask限0–15），不是宣称覆盖全8世界所有双前提三元组。
- 每模式另核1,024种双前提元数据组合，只有全部10开关为真时通过加强政策；每种仍未获科学知识认证。
- 独立检查覆盖三种空外延论域、空前提有效性、非法mask及存在断言正负两种极性。断言使用unittest，不受-O移除。

证据：[独立源码](../../reproduction/aristotle-posterior-analytics-i2/audit/independent_checks.py)、生产复跑[normal](../../reproduction/aristotle-posterior-analytics-i2/audit/production-normal.log)/[-O](../../reproduction/aristotle-posterior-analytics-i2/audit/production-O.log)/[-OO](../../reproduction/aristotle-posterior-analytics-i2/audit/production-OO.log)，独立核验[normal](../../reproduction/aristotle-posterior-analytics-i2/audit/independent-normal.log)/[-O](../../reproduction/aristotle-posterior-analytics-i2/audit/independent-O.log)/[-OO](../../reproduction/aristotle-posterior-analytics-i2/audit/independent-OO.log)。

## 限制与发布检查

程序是标准库教学程序，不是对任意不可信输入开放的验证服务。优先级/确信级按说明使用整数序数，未宣称全面做所有字段类型防御；领域适切性、现实真值、初始性、直接性、必然性与主体认识都没有被自动认证。有限枚举不代替一般证明，也不测量古代或现代人的心理。

本次审查的源码、说明与日志未见密码、密钥、私人对话或未许可原文全文；发布时应排除__pycache__等缓存。远端提交、链接和GitHub实际公式显示由发布核验另行完成，本报告不以本地阅读假称远端视觉验证通过。

## 最终字节绑定（SHA-256）

| 文件 | SHA-256 |
| --- | --- |
| `papers/ancient/aristotle-posterior-analytics-i2.zh-CN.md` | `97a4828f2676f7bd0f845b630a46f3192cda4451d6444ef1735e17420f31ace6` |
| `reproduction/aristotle-posterior-analytics-i2/model.py` | `b46f5513696db3b0ee03eb41bb6c959c0763d5466ebcbd5abf591faef82af255` |
| `reproduction/aristotle-posterior-analytics-i2/test_model.py` | `15f7b5d7604593c3d4c1c81213a68a7124160e342807a12fb986d792f91c7afd` |
| `reproduction/aristotle-posterior-analytics-i2/exhaustive.py` | `5afe075aeb40a11d22457217374d24a30ae813fb871933fc58c8a0e0f9fa4f68` |
| `reproduction/aristotle-posterior-analytics-i2/README.md` | `8b233d79b41c7b18ecedccf1eed60ff4fc8e56320628e2f96cc6b6fda9a8270c` |
| `reproduction/aristotle-posterior-analytics-i2/results.json` | `281f12362ef054fee65f4e46b28342a75b03713b88cadf737e59880d667f93ad` |
| `reproduction/aristotle-posterior-analytics-i2/audit/independent_checks.py` | `72faa424cff0692f0ec0e0f3787d24bf9ae767f3c877d648b9e3219eda7c168b` |
