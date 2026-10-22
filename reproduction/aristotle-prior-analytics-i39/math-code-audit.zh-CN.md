# I.39：独立数学与代码核验

## 结论与修订

对本文的现代受限模型，未发现需要修改实现的数学或代码错误。发现并修正了一处正文与API表述不够精确的问题：原始名`Atom`与定义引用`Ref`是两个带类型的命名空间，相同字符串并不等于同一符号；定义构造检查所有引用存在且无环，但原子是否具有外延在被求值时检查，而不是构造定义表时全面认证。正文第5.2、8节已按实现澄清。

本审查不把程序验证当作自然语言同义认证，不把古例的“不是属”当作集合不交；历史字词与版本由另附来源审查负责。

## 一般数学论证

1. **外延替换。** 第6.1节对表达上下文归纳：相同集合与固定集合取交相同，相对同一论域取补相同；因而项外延保持，AEIO的包含、交、差的真假随之保持。适用语言明确排除认知、模态及引语上下文，不从同指称推出任意语境可替换。
2. **定义扩展。** 第6.2节使用有限无环依赖关系的拓扑次序，为任意原始解释构造唯一的定义解释；逐层唯一性成立。任何旧语言反模型可扩展且旧真值不变，所以这是保守扩展。带类型名称避免原始谓词被短名覆盖。
3. **终止与可靠性。** 依赖层级下降配合有限子树结构保证抽象展开终止；按层级及项结构归纳证明展开保真。展开结构相同仅为充分证书，不完备；合取交换律的拒绝示例正确。Python实现仍受递归栈、内存与展开大小限制，抽象终止不是任意规模输入都可实际执行的承诺。
4. **反模型。** 单向包含替换、单样本共外延、同名不同义中项均有明确集合赋值并满足所述真假。第7.1节手算交集与补集正确；其中包含传递的一般证明与三个对象例子分开，没有以枚举代替证明。
5. **存在政策。** 现代AEIO允许空论域和空项，A/E空真、I/O需见证。代码与正文一致；未将此政策归给古代原章。

## 独立求值，而不是重复调用同一个展开器

原`run_checks.py`以同一实现展开前后进行回归比较，不能独自成为独立语义验证。因此另写[独立检查程序](independent_audit.py)：

- `holds`直接沿**未展开的原定义和项树**逐对象求布尔值，不调用`Definitions.expand`或`Model.extension`。
- AEIO oracle用逐对象的全称/存在布尔条件求值，不使用生产实现的集合包含、交、差判断。
- 在全部大小0–3的三原子模型中，取9个项（包括引用、嵌套、别名、交换次序及复合否定），比较生产求值与oracle。
- oracle只针对预构造的合法有限输入；输入验证由独立边界测试直接调用公开API检查，不把oracle内部短路误当作生产验证逻辑。

## 真实运行结果与命令

在本目录执行，Python版本及平台见[环境记录](logs/environment.txt)：

```sh
python independent_audit.py --tests
python independent_audit.py
python -O independent_audit.py --tests
python -O independent_audit.py
python -OO independent_audit.py --tests
python -OO independent_audit.py
```

|检查|正常、-O、-OO每模式结果|
|---|---|
|独立边界单测|12项全部通过|
|论域大小0–3的三原子模型|585个|
|9项外延与逐对象oracle比较|5265次通过|
|9×9项对、AEIO四式真值比较|189540次通过|
|三模式枚举JSON逐字比对|一致|

边界单测包括：同字符串Atom/Ref分离；空主项与空交左支不会吞掉缺失原子错误；未使用定义中的缺失引用与循环也被拒绝；缺失原子的检查时点；布尔值不冒充整数；负整数和重复元素的集合政策；映射不可直接修改；非法AST；结构证书不完备；显式失败检查不会在优化模式下消失。

真实日志：[正常测试](logs/independent-tests-normal.txt)、[正常枚举](logs/independent-normal.json)、[-O测试](logs/independent-tests-O.txt)、[-O枚举](logs/independent-O.json)、[-OO测试](logs/independent-tests-OO.txt)、[-OO枚举](logs/independent-OO.json)。这些结果是有界实现核验，不是第6节一般定理的证明、自然语言同义精度测量或古代唯一语义的认证。

## 最终文件绑定

以下摘要绑定实际核读版本；报告自身不参与自哈希。所有摘要采用SHA-256。

- `papers/ancient/aristotle-prior-analytics-i39.zh-CN.md`：`43105808b6533d0cac0c03dcdbccab51c7c3be04111fd784feb23243273ddd65`
- `reproduction/aristotle-prior-analytics-i39/model.py`：`c8b84dc0227c568e925e00585943cf4f2c60d230beb1ffe58a7afcd82157fa38`
- `reproduction/aristotle-prior-analytics-i39/test_model.py`：`9d06a6361773ef22c5dd091d65784166a89134645a90e0cea8c657e9ed433d27`
- `reproduction/aristotle-prior-analytics-i39/run_checks.py`：`d57c67488bdc577809fb3f70db71c6615d9f97c9cace38d1c68a7441f861f418`
- `reproduction/aristotle-prior-analytics-i39/independent_audit.py`：`cb58203f365dd9d3b4d8d2bdd9cd7b0686c6fd894efc1e0f466ea76394783c1f`
- `reproduction/aristotle-prior-analytics-i39/README.md`：`2a30a4a082e105381e55b51aa86e60e23f7e97a698e871bdc9290e544d346712`
