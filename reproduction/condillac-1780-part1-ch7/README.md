# Condillac, La Logique I.7: finite teaching reproduction

这是《逻辑》第一部第七章（所据1798年版印刷页58—66）的原创、低成本现代教学模型。它演示部分观察、比较与未知、特征相似、质量重组、有限正Horn推理，明确区分历史论述与现代形式化。它不是心理学或形而上学的验证，也没有声称作者给出了这些算法。

## 环境与一条命令复现

要求 Python 3.10 或更新版本；仅用Python标准库；CPU即可；不安装任何包；不联网。进入本目录后运行：

```sh
python verify.py
```

它依次运行普通、`-O`、`-OO`测试、演示和变异测试，将本次实际结果写入`results/`。如果任何子进程失败，总命令以非零状态退出。现附运行环境见`results/environment.json`；它是本次执行记录，不是支持版本的穷举验证。

也可分别运行：

```sh
python test_model.py
python -O test_model.py
python -OO test_model.py
python demo.py
python mutation_check.py
```

不要使用`pip install`。`python`须指向Python 3；若系统命令为`python3`，可逐条替换命令开头。脚本以当前解释器启动子进程。

## 文件导览

- `MODEL.zh-CN.md`：有限域、语义边界、命题与证明，以及第65页脚注的方向/空集说明
- `WALKTHROUGH.zh-CN.md`：按实际演示结果逐步阅读代码
- `model.py`：验证输入、观察、比较、等价类、想象、闭包、证书、独立真值表、集合包含
- `test_model.py`：18个测试方法，含1024个两原子理论穷举和200个固定种子三原子案例
- `demo.py`：确定性的JSON演示；生成闭包时同时复查证书与真值表
- `mutation_check.py`：8个明确语义错误的临时副本，须被行为断言击败；崩溃不计成功
- `verify.py`：完整复现入口
- `results/`：实际测试日志、演示JSON、变异结果、环境和汇总

`verify.py`会覆盖本目录中的结果记录，不修改模型或测试。变异脚本在本目录创建临时子目录，结束后删除；生产代码不会被改写。测试用`unittest`的显式断言方法，它们在优化模式下仍运行。模型中没有可被`-O`删除的`assert`语句。

## 结果如何读

普通、`-O`、`-OO`均应显示18个测试通过。变异报告应显示8/8被行为测试击败。注意总共是18个测试方法内部包含有限穷举案例，不能把18误说成只有18个输入，也不能把穷举说成覆盖任意大小系统。

演示中，两对象在color、shape相同，却在隐藏的material不同；4个质量组合只有2个具有目录见证；缺少桥接前提时不能推出column_supported；补入明示假设后可以；无种子循环不能推导出任何原子。空集包含推理成立不意味着有对象存在。

详见[模型与证明](MODEL.zh-CN.md)及[逐步讲解](WALKTHROUGH.zh-CN.md)。
