# I.23 独立数学诊断

本目录只含审核者独立集合实现、真实运行输出及版本绑定。未导入作者model.py，未修改作者日志。一般证明审读见[论证审查](../../../papers/ancient/aristotle-prior-analytics-i23.audit.zh-CN.md)。

环境：Python 3.12.14，标准库，无第三方依赖。工作目录为本文件目录。

```sh
python check_arguments.py
python -O check_arguments.py
python -OO check_arguments.py
```

真实输出：[normal.json](normal.json)、[O.json](O.json)、[OO.json](OO.json)；命令与退出码：[normal.log](normal.log)、[O.log](O.log)、[OO.log](OO.log)。三模式JSON逐字一致，退出码均0。

每模式核查255个三项非空论域模型、218个全项非空，9180项对称/矛盾关系，222对自由B单点构造，65535个四项链模型，5组显式例、4种方向/3角色类，201项奇偶恒等式诊断。计数详见JSON。

局限：这是有界数学诊断，不是一般自由扩展定理、归谬证明检查器、全部古代三段论或无理性证明。一般论证另由审查文字逐步分析。
