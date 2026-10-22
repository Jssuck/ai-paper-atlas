# I.32 独立数学与代码核验

核验对象是本单元原创中文正文及教学实现，不是对古代逻辑全部解释的认证。核验者独立读全稿、源码、作者测试与实际结果，并另外编写逐对象布尔成员 oracle；没有把重新运行作者测试当作唯一审查。

## 结论与修正

在下列明确范围内通过。代码审查发现一个可恢复问题：`candidate_completions` 将 `nonempty` 迭代器原样传给每个候选；若调用者给一次性生成器，第一个候选消耗后，后续候选会失去存在约束。现于入口转为元组一次，保持所有候选检查同一组约束。作者测试新增第36项，独立审查也另含同一回归。三个执行模式均实际通过。修正只影响一次性迭代器输入，不改变既有列表/元组演示的输出。

没有把简单候选过滤说成语义非循环性验证：当前只去掉结构上等于目标或已有前提的条目，同义表达和E换位等仍需人工审查。`holds` 是内部集合求值接口，要求合法 `Prop` 和包含相关词项的集合解释；它不是无约束数据校验器。

## 数学逐项检查

1. 第2、4节：A/E/I/O主项方向一致。包含传递用任意对象；排斥用同一对象反证。两者允许空项，未暗加存在预设。
2. 第4.1节反例中1在S和M而不在P，2仅作I(M,P)见证，确实既反驳全称结论也反驳特称结论。
3. 第4.2节共同谓项两肯定反例全部词项非空；改变S为{1}后交集非空，确实同时展示不必包含也不必排斥。
4. 第4.3节：Darapti式重构显式使用M非空；空M、S={1}、P={2}反模型正确。特称前提版本用I内见证，无需另加非空。
5. 第5节：Γ含Δ时的经典单调性方向正确；删除必要小前提的具体反例正确。新项N的二步补法是另一条件充分方案，不是唯一意图或事实证据。
6. 第6节：条件传递的假设卸除合法。三个非空不相交集合满足两个存在蕴涵却不满足个体包含，证实逆向不成立；不把p⇒r偷换成r或必然r。
7. 第7节：目前稿件明确“任意部分单独被毁”不能由组成材料原则直接取得，限定整体依赖的相关构成要素与情形。只有在这个额外桥、同一D关系与补集解释下，A(K,D)、E(N,D)推出E(K,N)，并进一步K⊆T。证明没有认证现实形而上学，也没有声称本章给出唯一公理化。
8. 第8节：加入新对象z到S但不加入M或P，保持两个M主项全称前提并破坏S⊆P；这是该组材料的任意域扩张构造，不是所有第三格理论的完整不可能性证明。
9. 三格表只标主谓角色，负命题箭头不作集合包含。“非前三格”仅属识别器范围，不是无效判决。交换两前提不变，调换结论端项则可能改变识别问题。
10. 20道答案与上述模型一致；有限测试与一般证明的边界在正文、README及程序返回状态均保留。

## 独立实跑范围

[独立源码](independent_audit.py)用每个对象的真假成员资格定义量词语义，独立于生产代码的集合包含、交、差运算。有限域大小1、2、3，三个词项允许空扩张，共584个赋值。

- 21,024次语义比较：584赋值 × 4命题类型 × 9有序词项对（包括自反词项）。
- 768次形状、输入换序和一致重命名检查：4种项位 × 64种AEIO量词极性组合 × 3种检查。
- 2,048个完整有限配置：4项位 × 64组合 × 8种非空约束子集。独立oracle对每个配置完整枚举；生产程序找到反例时可提前返回。
- 其中1,892配置有反模型，逐个独立复核返回赋值及存在条件；156配置界内无反模型，同时核对 `checked`、`admissible` 与 `premise_models` 计数。156不等于156条历史有效式，也不等于已证明156个一般定理；其中存在约束不同，且可能有不可满足前提。
- 8项非法输入检查；一次性存在约束生成器的多候选回归；8行命题链真值及条件后承检查。
- 普通、`-O`、`-OO`三模式全部完成，独立JSON结果字节相同。另重跑作者测试，每模式36项通过，演示输出字节相同。

证据：[独立命令](logs/independent-commands.txt)、[环境](logs/independent-environment.txt)、[普通结果](logs/independent-normal.json)、[-O](logs/independent-O.json)、[-OO](logs/independent-OO.json)、[作者重跑命令](logs/run.txt)。关键检查用显式异常，不依赖优化模式会移除的 `assert`。

独立实跑不覆盖任意大小域，也没有验证自然语言释义、经验事实、古代唯一语义或全部参数组合；四词项与大小4是实现允许的上限，不是本次全量oracle范围。一般正确性仍以正文逐对象证明为据。

## 终稿摘要绑定

以下为本次核验最终文件的SHA-256；审查件不自绑定，以免自引用循环。正文后续若有改动，应重新核对受影响内容并更新绑定。原始来源核验见另行来源审查，本报告不冒充独立手稿校勘。

```text
48558962689ef24baee087ba0dbbd2534d3c819c35f9ebe40a09adbe55569813  papers/ancient/aristotle-prior-analytics-i32.zh-CN.md
b93dad51e09a3b61c55885f2f1e546bd9540256bc03ba86d5987c18c663db494  reproduction/aristotle-prior-analytics-i32/README.md
a3db28bdc2f1620809108c2c3fcbf0f7df5967d287f71e9c8658a2ed3ef81531  reproduction/aristotle-prior-analytics-i32/SHA256SUMS.txt
5889addf88fd7cb7de43c20d691e7b0fa8457b6b55a882285dc4522d5f946f7e  reproduction/aristotle-prior-analytics-i32/demo.py
7222752fbb8b35316cc0bb07e862fce61dbd11efead5f5506bd351ca79d96219  reproduction/aristotle-prior-analytics-i32/environment.txt
035cce8c89b595108c2ed20e4560fdbe47652d59a5b1f9b23b3685fa7e6fe1e6  reproduction/aristotle-prior-analytics-i32/independent_audit.py
af99b325f28a031eb656adf4c918c514339955214434142bb2cdf7824f8444a1  reproduction/aristotle-prior-analytics-i32/logs/demo-O.json
af99b325f28a031eb656adf4c918c514339955214434142bb2cdf7824f8444a1  reproduction/aristotle-prior-analytics-i32/logs/demo-OO.json
af99b325f28a031eb656adf4c918c514339955214434142bb2cdf7824f8444a1  reproduction/aristotle-prior-analytics-i32/logs/demo-normal.json
2cf48117eff59ea545ef4f6c08aa54b8bc74450b2dddb8858a6397c741ebbef6  reproduction/aristotle-prior-analytics-i32/logs/independent-O.json
2cf48117eff59ea545ef4f6c08aa54b8bc74450b2dddb8858a6397c741ebbef6  reproduction/aristotle-prior-analytics-i32/logs/independent-OO.json
00fde371cc64e5f637e4bf3a31330b91b6677daf9fd573cc446725db6cb6e402  reproduction/aristotle-prior-analytics-i32/logs/independent-commands.txt
40abd271a9c258b94aefd3da5a34238bb4b5c5083f531e95b4a80e310dc6cd0f  reproduction/aristotle-prior-analytics-i32/logs/independent-environment.txt
2cf48117eff59ea545ef4f6c08aa54b8bc74450b2dddb8858a6397c741ebbef6  reproduction/aristotle-prior-analytics-i32/logs/independent-normal.json
6c0bacd94ed6b2e3c905957a4ad3d43161c70fccc0785658fe54c34c7f64f3bd  reproduction/aristotle-prior-analytics-i32/logs/run.txt
8dd4a7602312eb21d5da6545d9b2dfeccfc6aa5bf0051e3de325e53ee91668e2  reproduction/aristotle-prior-analytics-i32/logs/tests-O.txt
6b29dd5d3eb70b79fdaed3b044cacb4beba2273da64f2d6318cf2c4e9d1d2705  reproduction/aristotle-prior-analytics-i32/logs/tests-OO.txt
7dc30d08e0e55bcdb2d1b580219e25330fd6a97a0c0e6af67753452292bfd5af  reproduction/aristotle-prior-analytics-i32/logs/tests-normal.txt
90eeac97b12b3bacf042e62cd593dd501a41b0182f902432d98eee900168935f  reproduction/aristotle-prior-analytics-i32/model.py
af99b325f28a031eb656adf4c918c514339955214434142bb2cdf7824f8444a1  reproduction/aristotle-prior-analytics-i32/results.json
93beaaf6d0b416b6ecc4763047d968bf91d717591a9261b127130affaeabb594  reproduction/aristotle-prior-analytics-i32/run.sh
d7dfcc54dd7bb4db6451094f0502e2ed72c6dd3096bfeeb36214736eda87ffed  reproduction/aristotle-prior-analytics-i32/test_model.py
```
