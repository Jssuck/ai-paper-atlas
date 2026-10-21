# I.16 独立代码审查

## 结论与范围

对本目录作者实现、输入契约、测试、演示与保存结果的独立检查通过；没有发现需要修改作者实现的缺陷。审查不等于完整软件无错证明，更不认证亚里士多德全部模态推理或其唯一历史解释。原典审查与一般数学证明另有记录。

本审查逐项阅读 `model.py`、`test_model.py`、`demo.py`、附件README，并对照主文第4–8、10节的现代合同。重点确认：实际主项锚定、局部必要性、双向负桥E*、逐情形包含S+、同一个特称见证、空主项、实际情形索引、逐对象与联合可能不是同一条件。主文的全部历史译义及20题整体论证由另一路独立审计负责。

## 独立执行证据

| 检查 | 实际结果 | 证据 |
|---|---|---|
| 作者测试重跑 | normal、-O、-OO各24项通过 | [normal](independent-review/author-tests-normal.log)、[-O](independent-review/author-tests-O.log)、[-OO](independent-review/author-tests-OO.log) |
| 独立集合／真值轨迹oracle | 每模式9,928配置、1,810,155次显式比较，三模式结果相同 | [脚本](independent-review/check_code.py)、[normal](independent-review/oracle-normal.json)、[-O](independent-review/oracle-O.json)、[-OO](independent-review/oracle-OO.json) |
| 保存演示一致性 | 三模式每次重建演示，UTF-8序列化内容与作者 `results/demo.json` 精确一致 | 同上oracle结果；包含8,320配置演示及13个命名模型 |
| 非法输入 | 三模式各91个独立探针，全部按契约抛ValueError | [脚本](independent-review/check_validation.py)、[normal](independent-review/validation-normal.json)、[-O](independent-review/validation-O.json)、[-OO](independent-review/validation-OO.json) |
| 定向故障注入 | 9个有效变异，每个在三模式均被作者测试检出 | [脚本](independent-review/check_mutants.py)、[结果](independent-review/mutants.json) |

oracle不调用作者的模型生成器来生成对照配置，而独立展开词项赋值，以集合成员和每个对象的真值轨迹求期望值；再比较作者API。范围为1对象的1、2、3情形，以及2对象的1、2情形，全部实际索引与9个有序项对（含相同项）。检查全部五个模态模式及全称／特称、四种实然质、E*、S+、联合可能的正反两型、mask与序列化。作者生成器另查数量与配置不重复。

以上计数是配置及API比较次数，不是互不等价模型数、独立样本或概率成功率。空真、同构、重复世界和不同实际索引都明确保留。证明任意论域和情形集上的定理仍须正文的一般论证。

九个变异分别破坏实际索引、K双向性、N+全称性、N−强度、特称量词、E*反向条件、S+全情形范围、布尔尺寸拒绝及实然E极性。各变异只在临时隔离目录改副本；检出来自测试失败而非语法或导入错误。该组不是全部缺陷空间的覆盖证明。

初次oracle末尾曾把Python元组对象直接与JSON加载后的列表比较，导致审计脚本自身的表示差异失败；未发现作者结果错误。已改为作者同格式的完整序列化内容比较，并从头重跑三个模式，以上文件均为修正后的真实终态。

## 重跑与完整性

[环境](independent-review/environment.json)记录实际Python和完整命令；只用标准库，不需要网络、安装或密钥。在本目录执行：

```sh
python independent-review/check_code.py
python -O independent-review/check_code.py
python -OO independent-review/check_code.py
python independent-review/check_validation.py
python -O independent-review/check_validation.py
python -OO independent-review/check_validation.py
python independent-review/check_mutants.py
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
```

[摘要绑定](independent-review/reviewed-hashes.json)记录作者实现、合同、运行证据及独立脚本／结果的SHA256。摘要只证明文件身份，不证明语义正确。若受审文件改变，须重新审查或明确补充核验，不把旧绑定冒充新版本审查。

没有完整历史推理器、无限模型枚举、Jupyter内核或AI性能评测声明。代码在本篇明示现代模型上的一致性检查，不补足历史语义失配，也不把有限执行变为数学证明。
