# 同一个问题，什么变换保持了它？

孔狄亚克《逻辑》第二部第七章的现代、低成本教学附录。仅使用 Python 3.10+ 标准库，无安装、账号、网络或随机数要求。不是历史机器复刻，也不是心理学实验。

## 快速运行

在本目录运行：

```sh
python3 demo.py
python3 -m unittest -v
python3 mutation_check.py
python3 walkthrough.py
python3 verify.py
```

`demo.py` 输出确定性的 JSON：初始数量 (7,5)、保持整个方程组的消元轨迹、丢失条件的反例、顺序动作的不同解 (4,2)、有理解与筹码解的区别以及退化情形。

`verify.py` 真实重跑普通、`-O`、`-OO` 下的演示、9个单元测试、8个故障变体、演练及独立行列式／叉积审计；任何子命令失败都会使总验证失败。它会覆盖本目录 `evidence/` 中由它生成的日志与 `VERIFICATION.zh-CN.md`。不改源代码，无远程写入。

## 阅读与文件

- [逐步演练](WALKTHROUGH.zh-CN.md)：可复制的最小例子与预期结果
- [模型和证明](MODEL.zh-CN.md)：假设、一般论证、语义反例、参数公式与验证边界
- [实际验证](VERIFICATION.zh-CN.md)：环境、模式和结果；[汇总 JSON](evidence/summary.json)
- `condillac_model.py`：精确仿射表达式、方程组、行操作证书和求解器
- `test_condillac_model.py`：手算案例、输入拒绝、有限独立算术 oracle
- `mutation_check.py` 与 `test_mutation_check.py`：行为故障及分类器
- `demo.py`、`walkthrough.py`：两种面向读者的执行入口
- `independent_argument_checks.py`：独立行列式／叉积 oracle，核对35,308个方程组；不以被测消元器生成答案
- `verify.py`：运行及保存命令、stdout、stderr、退出码和环境

## API 速查

`Aff(r,l,c)` 表示 rR+lL+c；`R`、`L` 是变量。`+`、`-` 和有理标量 `*` 构建表达式，`at(R,L)` 求值。数值必须是整数或 Fraction，不接受浮点、布尔或字符串。`equation(left,right)` 表示左减右等于零。

`system(rows)` 验证并固定行序列；`holds(rows,r,l)` 检查合取。`canonical(rows)` 给出有理解集的规范形；`equivalent(A,B)` 判断两组有理解是否相同。`solve(rows)` 返回字典 `kind` 和 `point`，kind 为 none、infinite 或 unique；只有 unique 的 point 非空。

`row_step(rows,op)` 支持 ('swap',i,j)、('scale',i,s)、('add',i,j,s)，最后一项把第i行替换为第i行加s倍第j行。索引从0开始；缩放不准为零，加行要求i≠j。`certificate(rows,ops)` 返回含初态的完整轨迹。

`transfer(a=1,b=1,k=2)` 是两个独立情景；`sequential` 是先后动作的反例模型。`feasible(r,l,a=1,b=1)` 只检查独立情景的非负整数与供给约束；与等式检查分开。`oracle(rows,bound)` 只在0至bound整数正方形内枚举方程解。详细契约与边界见 MODEL。

## 最重要的限制

可执行算术不解决史料转录争议。这里用初始数量 R、L 编码问题语义，没有把可能存在印刷异常的变量行偷偷当作原文。运行通过也不证明“思想即计算”之类历史或哲学主张。有限测试不能证明无限域中的一般定理；相关一般保证由 MODEL 中独立论证提供。
