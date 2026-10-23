# 独立数学核验

本目录不导入生产程序的模型、规则或求值函数。

- `audit.py`：直接枚举三个标号对象的512个三项集合模型，检查两格、六种相反品质排列、两个非空政策、两个结论方向和两种否定量，共96条记录；另有12项边界和10条通用方向检查。
- `compare.py`：按支持集大小与组合生成255个模型，重新核对生产程序输出中的36条路线/背景记录、14条通用规则、3条包含关系记录，以及反模型。
- 两套枚举方法目的不同；前者是有界独立检验，后者针对明确的一元集合语义比对生产结果。两者都不能单独证明一般定理或古代唯一解释。

从复现目录运行：

```sh
python3 independent/audit.py > independent/normal-oracle.json
python3 -O independent/audit.py > independent/optimized-oracle.json
python3 -OO independent/audit.py > independent/double-optimized-oracle.json
python3 independent/compare.py > independent/normal-comparison.json
python3 -O independent/compare.py > independent/optimized-comparison.json
python3 -OO independent/compare.py > independent/double-optimized-comparison.json
```

JSON为真实运行输出；全部失败条件以显式异常处理，不依赖会被优化删除的assert。语义无反模型和规则证书是不同结果：不一致前提的空泛蕴涵不会自动成为新增形式规则。
