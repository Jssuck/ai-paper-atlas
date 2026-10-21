# 独立论证检查

本目录代码不导入作者模型。环境：Python 3.12.14，标准库；核验日期2026-10-21 UTC。它独立枚举集合解释，并用显式条件及RuntimeError实现核验，不依赖优化模式可能移除的assert。

从仓库根目录执行：

```sh
cd reproduction/aristotle-prior-analytics-i12/argument-review
python check_arguments.py > normal.json
python -O check_arguments.py > optimized.json
python -OO check_arguments.py > double-optimized.json
cmp normal.json optimized.json
cmp normal.json double-optimized.json
```

以上命令已真实运行，均退出0。各模式196619项检查通过，4096模型、192配置、52有限有效、140存在反例；4个手算反模型验证通过，所有配置都有满足前提的模型。结果文件是原始JSON输出。一般证明仍见主文，不能用本有限枚举替代。仅覆盖明定两对象、两情形及第一格四式。

`bindings.json`记录审核主文、来源账本、独立源码和输出的SHA256；不包含私有研究扫描，不声称复制了原典全文。
