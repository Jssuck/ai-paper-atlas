# 独立代码复核

- [完整中文审查报告](review.zh-CN.md)
- [独立测试与有限预言机](reviewer_check.py)
- [隔离重跑及真实变异执行器](run_independent_review.py)
- [最终执行摘要与源码指纹](logs/independent-summary.json)
- [全部独立变异输出](logs/mutations.log)

在上一级模型目录运行：

```sh
python3 independent-review/run_independent_review.py
```

执行器只更新本目录日志，不修改作者代码或作者日志。普通、`-O`、`-OO` 三种模式分别运行；有限测试不取代一般证明。完整数量、优化模式契约、已关闭问题和日志路径规范化规则见审查报告。
