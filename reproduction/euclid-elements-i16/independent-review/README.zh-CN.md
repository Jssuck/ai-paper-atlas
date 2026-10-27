# I.16 独立技术核查

本目录由独立审查者编写，未复用生产实现的内扇区判断作为预期答案。`check.py` 使用有理数和Cramer系数独立检验两组构造、严格正锥关系，并检查具体输入证书。

实际运行：三种优化模式各36项已有测试；独立300组构型、2400项证书/输入绑定篡改、512项扇区判断、256项普通角相等判断通过。Notebook六格在独立命名空间顺序重放，与已存stream输出逐字匹配；没有启动Jupyter内核。

原包几何检查使用精确有理数；独立脚本还以atan2角度作为附加近似诊断，对选定非极端样本检验严格大小和辅助函数，不能将浮点诊断当作一般证明。Cramer正系数与构造等式部分为精确检查。

命令、时间和退出码见[commands.json](commands.json)，统计见[results.json](results.json)，日志见[checks.log](checks.log)及三模式测试日志。命令可在上级目录运行：`python independent-review/check.py`。脚本不改Notebook或原作者日志。

有限测试只增加对实现和文稿对应的信心，不穷尽实数输入，也不提供欧几里得公理系统的机器形式证明。最终文稿绑定及审查结论见[技术报告](../../../papers/ancient/euclid-elements-i16.technical-audit.zh-CN.md)。
