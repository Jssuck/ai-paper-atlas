# 独立数学计数核验

独立于上级目录作者模型；只用 Python 标准库，无安装步骤。验证路径计数、内部插入的前提/结论类别变化，以及满二叉树的出现次数；不验证原文所有论证。

从本目录运行：

```sh
python3 independent_counts.py > results-normal.json
python3 -O independent_counts.py > results-O.json
python3 -OO independent_counts.py > results-OO.json
```

提交的真实日志：`run.log`，三个 JSON 分别记录解释器版本和优化级别。有限测试全部成功并不构成一般数学证明，证明见论文旁的 `audit.zh-CN.md`。正常模式与优化模式均使用不会被优化删掉的显式异常检查。不会导入 `../model.py` 或其它作者模块。

`review-bindings.json`在最终审查时记录正文、来源账本及本核验的 SHA-256，用以限定审查版本；后续修改需要重新核验，不能沿用“通过”的结论。
