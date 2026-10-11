# Condillac, La Logique I.8: qualitative teaching reconstruction

这是《逻辑》第一部第八章的原创现代教学模型。1780仅为本次核定的一版书目年；实际所据1798年版印刷页67—71，对应扫描PDF第75—79页。它区分客观缺少、被剥夺和需要，允许从未享用却惯常想象其乐，保留暂停中的激情，并将希望与狭义意志所结合的两种判断分别建模。

仅用Python标准库、CPU，不安装任何包，不联网。没有概率、效用优化或作者未曾给出的学习算法。输入是教学注释；运行成功不是心理学验证。

## 一条命令复现

要求Python 3.10或更新版本。进入本目录运行：

```sh
python verify.py
```

该命令实跑普通、`-O`、`-OO`三种模式的模型自测、自带变异检查及独立审计，再生成确定性演示；任何检查失败都会以非零状态退出。本次实际解释器与源代码指纹见[环境记录](results/environment.json)，汇总见[运行汇总](results/run-summary.json)。版本要求是代码兼容目标，不表示所有Python版本都已测试。

如本机只有`python3`，把各命令开头换成`python3`即可。子进程沿用实际解释器。不要使用`pip install`。

## 单独运行

```sh
python test_model.py
python -O test_model.py
python -OO test_model.py
python demo.py
python mutation_check.py
python -O mutation_check.py
python -OO mutation_check.py
python independent-review/review_model.py
python -O independent-review/review_model.py
python -OO independent-review/review_model.py
python independent-review/mutation_review.py
python -O independent-review/mutation_review.py
python -OO independent-review/mutation_review.py
```

测试使用显式`unittest`检查，不使用会被优化删除的`assert`语句。普通、`-O`、`-OO`确实执行检查；变异子进程继承该次优化级别。

## 目录

- [MODEL.zh-CN.md](MODEL.zh-CN.md)：符号、史料与现代假设边界、一般命题证明、非嵌套反例与显式桥梁
- [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：按演示编号逐步跟踪输入与输出
- `model.py`：当前情感记录、经验习惯、有限非空信念支持集、实际世界、两种判断与分类
- `test_model.py`：27个测试方法；含480个分类组合、64个事实性命题检查、130个限制命题检查及15个桥梁支持集
- `demo.py`：九个案例及一个支持集限制实验
- `mutation_check.py`：11个语义变异和真实语法错误对照，框架失败与行为检出分开记录
- `independent-review/`：独立实现的核查、独立变异及审计记录，详见[独立审计报告](independent-review/review.zh-CN.md)
- `verify.py`：一键重跑及写入结果；`results/`保存实际日志、JSON、环境及源代码指纹

`verify.py`会覆盖本目录`results/`中的对应结果记录，不改写模型。变异检查创建本目录或独立审计目录内的临时副本，结束后删除。请勿将临时副本当作生产模型。自带变异报告中的诊断日志只把本机执行目录路径替换为`BASELINE_DIR`或`MUTATION_WORKDIR`；其他诊断、测试数和结果不变。所有记录均由脚本实际运行产生，未手改结果。

## 关键结果怎么读

- 原模型每个优化模式均应27个测试通过，11/11语义变异被行为断言检出
- 语法、导入、运行异常或超时不等于语义检出；框架失败不能凑入通过数
- `hope=true`不保证实际获得；`narrow_will=true`不保证实际无障碍
- 希望和狭义意志没有无条件的嵌套；若加上支持集中的“无障碍则获得”桥梁，便可证明相应方向的蕴涵
- 支持集不能为空；实际世界不被强制放进主体支持集
- 一般证明与有限枚举分别报告，不能把四种命题真值类型当成所有身份关系或心理动态的完整覆盖

[开始逐步练习](WALKTHROUGH.zh-CN.md) · [查看演示输出](results/demo.json)
