# I.17 独立代码核验

## 结论与范围

独立审查者阅读了 `model.py`、`demo.py`、测试与复现说明，并以另一种集合算法交叉检查实际主项锚定语义。未发现实现缺陷。普通、`-O`、`-OO` 三模式均完成，结果除优化级字段外一致；没有依赖会被优化移除的 `assert`。这不是古代模态语义的唯一性认证，也不是无限模型定理的计算证明。

## 与作者实现独立的预言机

作者逐对象生成布尔序列再使用 `all/any`；[独立检查器](code-review/check_code.py)先将掩码经二进制字符串解为集合，再用集合交、并、补和包含求值。必要谓项资格为跨情形交集，弱可能资格为并集，双向偶然资格为并集减交集；最后仅对实际主项集合量化。

枚举范围是 `(对象数,情形数)` = `(1,1),(1,2),(1,3),(2,1),(2,2)`，包含每个实际情形选择、空项、重复情形及同项关系。每种运行模式检查：

- 9,928 个带实际点配置。
- 1,429,632 个四模态 A/E/I/O 命题值。
- 63,960 个外延、54,552 个对象模态序列。
- 89,352 组正负必要见证；89,352 次非偶然析取分解。
- 178,704 个共同情形判断，专门区别逐对象可能与共同世界可能。
- 119 个非法输入探针，包括布尔数冒充整数、空情形、越界掩码和实际点、错误项名及空主项下的坏谓项。
- 独立读取全部 16 × 16 = 256 个候选端项推论，核对前提真值、完整结论覆盖和反模型名单，非仅检查名单长度。

日志：[普通](code-review/normal.json)、[-O](code-review/O.json)、[-OO](code-review/OO.json)。

## 定向变异

检查器在内存中对作者源文本施加十个独立变异，不改作者文件；每个在三模式均被杀死：双向偶然退化为弱可能、必要退化为可能、可能加强为必要、忽略实际点、错误固定主项点、存在量词变全称、抹掉否定质、丢弃必要否定分支、共同情形误换逐对象可能、接受布尔论域大小。日志给出首次检出的性质；这不是完备的变异测试集合，也不排除其他潜在错误。

## 作者证据的再次执行

独立重跑作者三模式各 24 项测试，日志为[普通](code-review/author-tests-normal.log)、[-O](code-review/author-tests-O.log)、[-OO](code-review/author-tests-OO.log)。重跑普通模式演示所得[JSON](code-review/author-demo-rerun.json)与作者 `results/demo.json` 精确逐字节相同；作者三份已保存演示亦相同。优化模式的独立预言机与定向变异另有实际运行，不把静态阅读当实跑。

## 可重跑命令

从本复现目录执行：

```bash
python code-review/check_code.py > code-review/normal.json
python -O code-review/check_code.py > code-review/O.json
python -OO code-review/check_code.py > code-review/OO.json
python -m unittest -v > code-review/author-tests-normal.log 2>&1
python -O -m unittest -v > code-review/author-tests-O.log 2>&1
python -OO -m unittest -v > code-review/author-tests-OO.log 2>&1
python demo.py > code-review/author-demo-rerun.json
cmp code-review/author-demo-rerun.json results/demo.json
```

运行环境见[独立环境记录](code-review/environment.json)。[摘要绑定](code-review/reviewed-hashes.json)绑定审查的作者代码、说明及原始结果，以及本检查器和独立日志；摘要不作电子签名或外部认证。正文数学与原典另有独立审查，不由本报告替代。
