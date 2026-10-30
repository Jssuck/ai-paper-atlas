# Euclid III.21：同弓形角的精确教学检查

这是原创现代坐标教学重构，不是古代实验，也不是对《几何原本》一般定理的计算机证明。只用 Python 标准库，输入限于整数或 `fractions.Fraction`；拒绝浮点数与布尔值。圆心 O、半径平方 r2、共同底弦端点 B/C、圆周顶点 A/D 均由调用者指定。四点须属于同一给定圆，B≠C，A/D 不得是 B/C；允许 A=D，此时等角平凡成立。

## 判据和范围

对顶点 P，u=B−P、v=C−P，程序计算 `cot(angle BPC)=dot(u,v)/abs(cross(u,v))`，不用 `acos` 或舍入。合法角严格在 0 与 π 之间，故 cot 的单射性允许从相同 cot 判断相同角；负 cot 表示钝角，不得取绝对值。

`sign(cross(C−B,P−B))` 判断圆周顶点位于弦的哪一侧，而不是用屏幕上下关系。A/D 同侧时输出 `relation=equal`；异侧时输出 `relation=supplementary`，两 cot 互为相反数。异侧不意味着相等；共同底弦为直径时两角均直角，是异侧仍相等的例外。`equal` 是额外的数值等角字段，不能把 `relation=supplementary` 误读成一定不等。

`certificate` 先校验合法域，再计算两角和侧别，不预筛选待证的等式。`verify` 对原始输入重新计算并检查精确字段集合、值、类型；它能发现记录篡改，**但与构造器共享实现，不是独立证明器**。独立技术审查应检查数学式、测试覆盖和实现本身。

## 实跑与重跑

在本目录执行：

```sh
python run_all.py
```

[环境](environment.json)、[运行汇总](run-summary.json) 保存真实执行结果。主脚本分别以普通、`-O`、`-OO` 执行：

- [18 个 unittest](test_geometry.py)：优弓/劣弓、异侧、直径、重合顶点、平移缩放、弦反向、非法半径/点/类型、证书篡改以及网格。
- [命名例与枚举](run_examples.py)：10 个有理圆周点，所有无序底弦与剩余点中无序双顶点，共 1260 配置/模式；同侧 840，异侧 420，直径底弦 112，至少一钝角 406。后三者可能交叉，不应相加。三模式重复同一网格，不是 3780 个独立配置。
- [Notebook 回放](verify_notebook.py)：5 个代码格按顺序 `compile/exec` 后逐字比较已存标准输出；**未启动 Jupyter kernel**。`execution_count` 保持 null，避免伪装为内核计数。这检查 Python 单元逻辑及输出，不验证 kernel 协议或前端渲染。

日志：[普通测试](logs/test_geometry-normal.log)、[-O 测试](logs/test_geometry-O.log)、[-OO 测试](logs/test_geometry-OO.log)、[普通例子](logs/run_examples-normal.log)、[普通 Notebook](logs/verify_notebook-normal.log)。其余同名 `O` / `OO` 日志也由脚本生成。

[教学 Notebook](teaching.zh-CN.ipynb) 由 [create_notebook.py](create_notebook.py) 生成；安装技能所述 scaffold 脚本在本环境不存在，因此按 nbformat 4 结构生成 JSON，未安装额外软件。可在已有 Jupyter 环境从本目录打开后重新顺序运行。

## 命名例

圆心 (0,0)、半径 5，共同底弦 B=(−3,4)、C=(3,4)：

| 情形 | A | D | 两角 cot |
|---|---|---|---|
| 同优弓形 | (0,−5) | (−5,0) | 4/3、4/3 |
| 同劣弓形 | (0,5) | (7/5,24/5) | −4/3、−4/3 |
| 异侧反例 | (0,5) | (0,−5) | −4/3、4/3 |

直径例另用 B=(−5,0)、C=(5,0)、A=(0,5)、D=(0,−5)，两 cot 均为 0。错误例把顶点换成圆心而保持圆参数不变，被圆周归属校验拒绝；不能将“在圆内部”替换为“在圆周上”。

![同侧与异侧示意](diagram.svg)

图由 [make_diagram.py](make_diagram.py) 原创生成，根元素显式指定 1200×480；为教学示意，不以读图测量代替证明。另在已有 Inkscape 中渲染 PNG 并目视核对点名、弦、三组连线和文字，未将本地工具路径或私人审计记录纳入公开文件。

## 不能据此声称的结论

有理点有限枚举不能证明所有实数圆周点；精确算术只消除该样本中的舍入误差。程序不验证古希腊原文、一般平面公理、III.20 的证明或历史归属。没有训练数据、基线准确率或实验性能主张。一般论证请读对应正文；本目录用于排错、展示条件及反例。
