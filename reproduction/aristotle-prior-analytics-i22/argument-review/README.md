# I.22 独立论证检查

本脚本独立使用集合语义，不导入作者的模型和枚举程序。一般证明见[独立数学审查](../../../papers/ancient/aristotle-prior-analytics-i22.audit.zh-CN.md)。

## 命令

在本目录执行：

```sh
python check_arguments.py > results-normal.json
python -O check_arguments.py > results-O.json
python -OO check_arguments.py > results-OO.json
```

真实执行环境及终态见[run.log](run.log)。脚本使用显式运行时检查而非会被优化删除的assert。

## 有限范围

完整枚举(n,世界数)为(1,1)、(1,2)、(1,3)、(2,1)、(2,2)、(2,3)，共266888个配置。每配置检查8个蕴含族，共2135104次前提/结论检查；前提满足次数按族列在JSON。另有13个显式配置（含6个正文精确配置），包含n=3的非空项睡眠对照和Box/锚定必要的差异。这不是将n=3所有模型纳入穷举。

结果文件：[正常](results-normal.json)、[-O](results-O.json)、[-OO](results-OO.json)。这些是实现复核，不代替一般证明，也不认证原典唯一语义。
