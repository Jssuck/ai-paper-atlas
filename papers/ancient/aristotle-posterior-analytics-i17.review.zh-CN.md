# 《后分析篇》I.17：独立数学与代码审查

## 结论与范围

**通过，限本文件列出的最终字节版本与明示模型范围。** 独立审查者复核正文所有集合推导、数值算例、第二格反证、练习答案与复现源码，并独立复跑。不是人类专家或证明助理认证，也不是对科学适当中项的判定。来源校勘由另附来源审查承担；GitHub发布后实际页面与公式显示须另行验证，本文件不把静态公式检查冒称远端渲染完成。

## 数学核查

- 本文记号 `All(P,S)` 的顺序是谓项、主项；代码 `all_of(subject,predicate)` 顺序相反。逐项核对调用及四论式映射一致，没有因此交换包含方向。
- 非空B包含于C包含于A时，保留真小前提并翻转大前提，Celarent的前提为全假/真；真实分离链下Barbara同理。小前提的真值来自真实链，不来自肯定形式本身。
- 错误否定的两个非适当结构分别给双全假及真大/全假小；显式分离条件未偷换成一般不包含。
- 两种第二格在非空B包含于A背景中，双全假会让同一个B对象同时在C中且不在C中；一般反证正确。双部分假的数值例不违背该结论。
- 错误肯定各分支及结尾量词范围区分正确；固定大前提假时不错误列入真大/假小。
- 空项反例、交叠反例及Barbara双假真结论反例均有效。一般论证与有限穷举的证据职责分开。
- 审查指出第5节歧义误读对照必须显式保留真实B包含于A且B非空，否则共同上属D本身不足以保证否定结论错误；最终稿已补该条件。第8节另一序列中项亦保持真关系和F/T范围。

## 实际独立执行

在CPython 3.12.14下分别执行 `python3 -m unittest -v test_model.py`、`python3 -O -m unittest -v test_model.py`、`python3 -OO -m unittest -v test_model.py`，每次16项测试均通过。测试采用unittest方法，不因优化选项删除裸断言而形成虚假通过。重新执行 `python3 model.py` 后，输出与发布的results.json逐字节一致。

另写**整数位掩码实现**，没有导入或调用被审查model.py的谓词、分类或枚举函数：

1. 三元素论域全部343个非空三项解释，逐项对照公开JSON的所有结构计数、真假组合和见证，一致。
2. 四元素论域全部3375个非空三项解释，独立核查相同结构；四论式在含空项的4096个解释各核查一次，共16384项有效性检查，无真前提假结论。
3. 四元素时固定真肯定链175例、真否定链110例均为全假/真；两错误否定分支各110例分别为双全假与真/全假。
4. 四元素第二格每式在975个真肯定背景解释中均无双全假，各有302个双部分假。

这些数字只是指定有限论域的真实运行结果，不充当一般定理证明或原文唯一解释的证据。结构情景可重叠，不能将各行加总当作互斥划分。

## 复现、隐私与发布边界

run.sh仅在自身目录生成结果和日志，不联网或使用密钥；公开日志未发现私人路径、账户资料或秘密。Notebook依赖不可用的说明与环境日志一致，不冒称已执行Notebook。发布清单应排除运行缓存 `__pycache__`、私有审查工作目录及原文扫描件。外部链接、main冲突保护和最终GitHub公式显示仍由发布核验分别确认。

## 本次绑定的SHA-256

任何下列文件修改（包括公式格式变化），应重新核对并更新对应绑定；本表不对自身做循环哈希。

| 文件 | SHA-256 |
|---|---|
| `papers/ancient/aristotle-posterior-analytics-i17.zh-CN.md` | `11e9e198abfb53efd36b824e140697bf8c69f25a05fd910527da94123dd1f903` |
| `papers/ancient/aristotle-posterior-analytics-i17.sources.zh-CN.md` | `3b748dfb933bd09f268e792654de3cff0f42e17311dbdf319f32c0b963c1e38f` |
| `reproduction/aristotle-posterior-analytics-i17/README.md` | `3c6b381723541d9f6247c17b667f71e5509e08ec051853e977d9a6bf7996e370` |
| `reproduction/aristotle-posterior-analytics-i17/logs/commands.log` | `f71f623dc1b87478c98f3a7171d6a732bf830dd040a6117cee60e8e1db43772d` |
| `reproduction/aristotle-posterior-analytics-i17/logs/environment.log` | `ac972e9a927795500e2ff5b8c1b730c310ddd54f950c5eedebcbd2425ac21958` |
| `reproduction/aristotle-posterior-analytics-i17/logs/tests-O.log` | `678fe245b714c9f4ed3ddd7966a677c2fd7ecce7b2b7008980919b46a1e8ed95` |
| `reproduction/aristotle-posterior-analytics-i17/logs/tests-OO.log` | `acebe0bdaae29cdea806c41acc76f8ae7c016394718a0f6236042d25ef612aa4` |
| `reproduction/aristotle-posterior-analytics-i17/logs/tests-normal.log` | `678fe245b714c9f4ed3ddd7966a677c2fd7ecce7b2b7008980919b46a1e8ed95` |
| `reproduction/aristotle-posterior-analytics-i17/model.py` | `afa1cc0f4c96e974fdc61d20960a5dc096573a77259b1265298e75398abbef68` |
| `reproduction/aristotle-posterior-analytics-i17/results.json` | `37c7564ffdf3dfc9674a289a084afba4667abc132357d88517650abb2be73c7c` |
| `reproduction/aristotle-posterior-analytics-i17/run.sh` | `cc8606d444cb0c55cb624bd5e22bacfdfc710f5c94e3f172507303f51fba85ba` |
| `reproduction/aristotle-posterior-analytics-i17/test_model.py` | `c7482757ffb2da2750f5ddb33726324930b78424511d60fbf56ade7d88fb9d26` |
