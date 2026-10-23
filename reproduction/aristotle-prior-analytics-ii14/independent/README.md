# 独立集合 oracle

本程序不导入生产源码。按本章十五条路线另行转录，用集合运算检查三种存在政策下45条记录的180项蕴涵/冲突结果，包含前提模型数、反模型数及最小反例。另核两政策共48个命题补集、27648次条件转置，以及6项边界检查。

在父目录运行：

```sh
python3 independent/oracle.py evidence/results-normal.json
python3 -O independent/oracle.py evidence/results-normal.json
python3 -OO independent/oracle.py evidence/results-normal.json
```

三模式真实输出和日志在本目录。程序抛显式异常，不依赖会被优化移除的assert。候选形式和语义是明示的现代教学重构；格编号由人工审查，不是程序从任意句法识别。转置穷举不替代正文一般证明，有限集合结果不裁定古代唯一语义。
