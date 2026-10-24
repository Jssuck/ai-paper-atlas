# 《后分析篇》I.11 独立数学与代码审查

结论：**通过所述有限范围的技术审查；未发现阻断发布的数学或实现错误。** 审查者未编写正文和生产实现；独立阅读正文、复现说明、模型、生产测试及运行脚本，另写语义不同的有限 oracle 并实际运行。本报告不是古代文本校勘认证，也不是对所有逻辑系统的证明。

## 1. 关键数学判断

- 全称实例化加肯定前件的教学推导成立；分离实体既未被使用，也未因此被证伪。同名中项反例中，空的H₁令全称前提真，H₂(c)真而A(c)假，确实阻断错误连接。
- 有符号闭包是明确给定的有限正向规则系统。负号属于独立支持标识，不是自动取补集；程序没有爆炸、逆否或缺省否定。冲突输入不删除既有正向证明，但这不认证真实对象矛盾，也不认证原文已建立现代次协调逻辑。
- 终止来自有限可加入的结论；最小性来自每个闭集模型都包含迭代各轮；单调性来自旧推导可在包含更多事实的新输入中重演。正文与复现说明的归纳论证符合实现。
- 未导出负支持，不等于已证负命题为假，更不等于双重否定证明。正文已专门区分。程序的`Literal`只存标识及极性，不存量词或对象变量；其例子是固定个体上的命题化演示，不能当作多对象一阶推理器。
- K3模块的U是教学中选定的缺口值；它与支持模块的正负并存不是同一状态空间，代码也未把两者转换或混算。K3表在U行不使排中式取T，并不反驳经典二值排中；局部覆盖函数只是集合覆盖检查，不是归谬证明器。
- 所有现代数学及程序结论均受模型范围约束；古代段落的局部大项条件不能被较弱的“没有负支持记录”替代。正文没有作这种替代。

## 2. 独立可重复检查

独立源码：[audit/independent_test.py](../../reproduction/aristotle-posterior-analytics-i11/audit/independent_test.py)。它未调用生产`graph_oracle`。针对三个有符号原子，列出8个可能事实集、24条可能规则（每个前件子集乘三个后件），遍历24×24个有序规则对和8个种子，共**4608次**闭包比较。oracle枚举所有包含种子且满足规则的闭集模型，再取其交集；与生产的迭代方式及生产测试的图可达方式不同。

该范围包含空前件、合取前件、循环、自依赖、重复规则，但**不是所有三原子规则集的穷尽**，更不是无限系统。每种模式另检查4608次幂等性、15552对包含关系下的单调性、56组允许值/情形覆盖，手列3个否定表项、9个析取表项、排中各行，以及支持四态、无爆炸、无逆否、无缺省否定、身份不合并、非法输入等边界。

实际结果（Python 3.12.14，CPython；[环境](../../reproduction/aristotle-posterior-analytics-i11/audit/environment.log)）：

| 模式 | 独立 unittest | 重跑生产 unittest | 重跑生产一元图枚举 |
| --- | --- | --- | --- |
| normal | 6项通过；4608次oracle比较一致 | 18项通过 | 65536组合，0差异 |
| -O | 6项通过；4608次oracle比较一致 | 18项通过 | 65536组合，0差异 |
| -OO | 6项通过；4608次oracle比较一致 | 18项通过 | 65536组合，0差异 |

各模式是同一案例的重复运行，不算新增独立理论证据。测试使用unittest断言方法，不依赖会被-O移除的语言assert。独立测试和生产枚举实际退出码均为0。

日志各自首行保存命令，从复现目录执行：

- [独立normal](../../reproduction/aristotle-posterior-analytics-i11/audit/independent-normal.log)、[-O](../../reproduction/aristotle-posterior-analytics-i11/audit/independent-O.log)、[-OO](../../reproduction/aristotle-posterior-analytics-i11/audit/independent-OO.log)
- [生产测试normal](../../reproduction/aristotle-posterior-analytics-i11/audit/production-repeat-normal.log)、[-O](../../reproduction/aristotle-posterior-analytics-i11/audit/production-repeat-O.log)、[-OO](../../reproduction/aristotle-posterior-analytics-i11/audit/production-repeat-OO.log)
- [枚举normal](../../reproduction/aristotle-posterior-analytics-i11/audit/enumeration-repeat-normal.log)、[-O](../../reproduction/aristotle-posterior-analytics-i11/audit/enumeration-repeat-O.log)、[-OO](../../reproduction/aristotle-posterior-analytics-i11/audit/enumeration-repeat-OO.log)

## 3. 绑定版本（SHA-256）

以下是实际阅读与测试的字节版本；正文或生产代码发生变化需重新确认本审查是否适用。

| 文件 | SHA-256 |
| --- | --- |
| 正文 `aristotle-posterior-analytics-i11.zh-CN.md` | `525d42f22888e3c9ea4b53d970feb611494d6a141faa5fa0eaa63eafff2db675` |
| `model.py` | `94191d92333058ca7a601fcd7cd4240908ba5eef314d7993ff796834e4b182fc` |
| `test_model.py` | `0f47bc3a1ed1281c7030ea05d20daa8f7f1d1551a6cc0dcefecff9e78c3de161` |
| `run.sh` | `0ecdebd04e73a4e6bc9ecc5b085d4623a908592b9d81c4665787ce669afcb498` |
| 复现 `README.md` | `fa2fc1c359bc250a20e44703fbf0541e4963044b32fe9f2fbda39ac1ec18b9c8` |
| `audit/independent_test.py` | `d5575832f22d7590c28463b14c1c8e5d42b0b482f9f129425cc21e63e3fcf500` |

## 4. 保留限制

测试不能判定自然语言同义、对象属正确性或现实证据可靠性，不能把K3空缺解释强加给古代作者。一般性质由上述定义和归纳承担，有限枚举仅核查实现。本次未更改生产源码；复现README补充了固定个体/ground范围、独立检查范围及证据链接，并已重新阅读绑定；来源、年代及章界由独立来源审查另行承担。
