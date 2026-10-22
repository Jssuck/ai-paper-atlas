# I.37：独立数学与代码审查

## 结论与范围

已实际阅读深读正文全部论证、实例和12题答案，以及`model.py`、`test_model.py`、`run_checks.py`、复现README；目视Owen印162本章正文与注3–5，确认现代模型没有被冒称为原段算法。来源和版本细节另由[来源审查](../../papers/ancient/aristotle-prior-analytics-i37.source-audit.zh-CN.md)核验。

对修订后文件，在已声明的教学范围内，未发现未解决的数学或实现错误。此结论不是古代体系完整性、自然语言翻译唯一性或生产安全认证，也不代替远端提交与实际公式显示核验。

## 数学逐项核对

1. 同一完整中项的包含传递证明正确；允许空项，不凭全称包含捏造存在。代码另测空论域，正文已标为非空主设定之外的边界扩展。
2. 两标签单对象反模型正确反驳删限定与反向删限定；两集合同时含对象又排除“不能推出肯定所以能推出否定”的错误。u标签不被定义为对所有方面全称量化。
3. 合取引入与消去保留同一对象。两不同见证不能直接合并的二对象反例成立。
4. 否定整个合取等价于至少一项否定，不能分别推出每项否定；补一个肯定事实后推出另一项否定的反证正确，且已明确经典二值语义。
5. 全称包含分配到交集的双向逐成员证明正确，不需要主项存在；正文手算表和练习答案与定义一致。
6. 第4.6节的步骤归纳是检查器设计的一般条件论证，而非现有程序功能。程序仅检查两条原子包含边及一个结论的结构，既不认证事实，也不搜索桥梁。
7. 不透明复合词的外延由输入独立给出，没有从字面自动推出交集或部分性质。范畴标签用于完整身份，不是古代范畴的完整本体论。

## 初审意见与实际修正

- 原回归脚本使用`assert`，优化运行会删除核验。作者已改用显式`check`和异常，使正常、`-O`、`-OO`均执行检查；审查者独立复跑三模式并比较输出一致。这是执行证据修正，不是发现集合定义错误。
- 主文先只写P与k，代码有name/category/aspect三个字段。主稿已明确P对应前两字段、k对应第三字段；代码允许显式混标签组合，正文只需要同标签子语言。不同标签的组合仍是同一对象域上的集合运算，不自动证明词义相容。
- 正文非空域与程序额外空域测试已分开。证书要求完整中项相同，不要求所有端点同方面；显式跨方面包含边可以传递，拒绝的是未经桥接偷换中项。
- 手算段落中的“整体合取”已改为“整个合取”，避免与整体标签u混淆。

## 独立实跑

[独立脚本](independent_audit.py)以整数位向量计算预期外延、存在和包含；不调用被审`extension/includes/some`生成期望值，不复用原回归脚本的期望计算。四个原子分别覆盖相同方面的两个名称、同名不同方面、同名不同范畴。语法样本为28个原子/否定/合取/嵌套组合。

正常、`-O`和`-OO`三模式真实执行，三个独立JSON结果逐字段相同：

|核验范围|实跑计数|
|---|---:|
|论域大小0–3，四谓词全部赋值|4369模型|
|表达式外延与独立位向量比较|122332|
|存在判断与独立位向量比较|122332|
|原子包含与独立位向量比较|69904|
|真前提包含链实例|83776|
|包含对交集分配实例|279616|
|三条边组合的证书结构检查|4096|
|格式、缺键、越域和非法表达式拒绝|17|
|具体反例与边界检查|10|

四谓词模型数为1＋16＋256＋4096。这里计的是对选定对象域大小的全部赋值，不是全部表达式或全部模型。10个具体检查包括删方面、擦范畴、两个否定强度反例、不同见证、空域不生成存在、接受结构不保证前提真、拒绝证书但结论可真及明示跨标签边被接受。其一般理由仍以正文证明为准。

此外，独立复跑作者修订后的回归脚本，三模式JSON一致并与作者`checks.json`一致；18项单元测试在三模式均通过。真实日志见：

- [独立正常模式](logs/independent-normal.json)、[优化模式](logs/independent-O.json)、[双优化模式](logs/independent-OO.json)；
- [回归正常](logs/independent-regression-normal.json)、[回归-O](logs/independent-regression-O.json)、[回归-OO](logs/independent-regression-OO.json)；
- [单元正常](logs/independent-tests-normal.txt)、[单元-O](logs/independent-tests-O.txt)、[单元-OO](logs/independent-tests-OO.txt)。

重跑命令（在本目录）：

```sh
python3 independent_audit.py
python3 -O independent_audit.py
python3 -OO independent_audit.py
python3 run_checks.py
python3 -O run_checks.py
python3 -OO run_checks.py
python3 -m unittest -v
python3 -O -m unittest -v
python3 -OO -m unittest -v
```

有限测试不证明一般数学定理，也不验证任意深度表达式、恶意输入资源限制、自然语言解释或事实真实性。`Model`接口是教学用内存对象，不是不可变安全边界；调用者仍应负责不在解释过程中擅改其公开映射。

## 终审文件绑定

以下SHA-256由审查时实际文件生成，不包含本审查文件自身，避免自引用。全包交付摘要另由发布检查生成；后续若修改下列内容，需重新核对并绑定。

```text
21d9d02d68d2b0d40d51f03aae792efc6e0eb27d1a9ef0204e45af4466988732  ../../papers/ancient/aristotle-prior-analytics-i37.zh-CN.md
4f359bf2cac7f57657d2c33fcf423be9c6a6caa9af742a0db05b58d5a6265ee5  model.py
8777392b303f1308168556255051f383bb7bcd207a91b10d33bd5c4abb53159f  test_model.py
32a7797ce678526df4533a289091234de395982621863ea2c3ab57ba840f6fab  run_checks.py
f06fae946472390db6be81be878889a1e53ee55c2e5b59bc605e3819b87fd9e4  independent_audit.py
76215d92a22aee3fef528c91a5e0730773ad139e9281b89b72094ea0ea713262  README.md
b63863ed15c8015cb71f805879f9f48ca982c4fbb1156539c0a1ed7483c46743  logs/independent-O.json
b63863ed15c8015cb71f805879f9f48ca982c4fbb1156539c0a1ed7483c46743  logs/independent-OO.json
b63863ed15c8015cb71f805879f9f48ca982c4fbb1156539c0a1ed7483c46743  logs/independent-normal.json
ce5da080461e7c3b87649f519ebf678a2230b8630c485ce84c9ffa605a1cc69d  logs/independent-regression-O.json
ce5da080461e7c3b87649f519ebf678a2230b8630c485ce84c9ffa605a1cc69d  logs/independent-regression-OO.json
ce5da080461e7c3b87649f519ebf678a2230b8630c485ce84c9ffa605a1cc69d  logs/independent-regression-normal.json
5572b6cdfc112c27990cc1fa4d4de9bd3564c663214eae51adbfe39795108fe1  logs/independent-tests-O.txt
5572b6cdfc112c27990cc1fa4d4de9bd3564c663214eae51adbfe39795108fe1  logs/independent-tests-OO.txt
5572b6cdfc112c27990cc1fa4d4de9bd3564c663214eae51adbfe39795108fe1  logs/independent-tests-normal.txt
```
