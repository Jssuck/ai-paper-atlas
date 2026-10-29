# II.8：八块面积与补方的精确教学核验

这是原创有限教学模型，不是古代原文的机器证明，也不是现代学习模型复现。Python 标准库足够，不安装包，不读取网络或源文献文件。

## 几何对象

设 a=AC、b=BC=BD 的基系数，a,b 严格正；等分 a=b 合法。单位基时它们就是长度，非单位基时实际长度须乘基向量长度。原点可平移，两基必须正交、等长且非零；旋转、反射与等比例缩放均支持。设 s=a+2b，图为外平方 AEFD。两条竖线 x=a,a+b；两条横线 y=b,2b。ED 对角线经过 Q 和 K。

| 区域名 | 循环顶点 | 单位基面积 |
|---|---|---|
| CK | C B K G | b² |
| KD | B D N K | b² |
| GR | G K R Q | b² |
| RN | K N P R | b² |
| AG | A C G M | ab |
| MQ | M G Q O | ab |
| QL | Q R L H | ab |
| RF | R P F L | ab |
| OH | O Q H E | a² |
| AK | A B K M | (a+b)b |
| 曲尺形 | A D F H Q O | 四倍AK |
| 外平方 | A D F E | s² |

`L` 同时可能出现在普通数学中的长度记号里；本代码只把它用作点名，外边系数用 `s`。STU是曲尺形的辅助指示，不是额外三角形；原创图用颜色分组而未冒充三个几何点。

## 接口与检查边界

`construct(a=3,b=2,origin=(0,0),u=(1,0),v=(0,1))` 返回仅含 `points` 字段的证书。参数只接受 int 或 Fraction，拒绝 bool、float、字符串及非正长度。`verify(c,...)` 需带同一组外部参数，逐点检查构造位置，再用多边形鞋带公式求面积，核对两组四块等积、八格曲尺形、AK分割和OH补方。没有依赖可被 -O 删除的 assert。

非单位基的所有面积乘 u·u。例如 (3,4),(-4,3) 长度为5，面积乘25。默认a=3,b=2，每个小平方4，每个窄矩形6，AK=10，八格40，OH=9，整平方49。

验证器按规范构造函数复核点，因此点坐标检查与构造有同源局限。它不是任意输入图形的形式证明器；独立技术审查需由另一个实现构造外部证书并比较。精确有理数可防浮点误差，但有限样本不能证明所有实数情形。一般证明在正文中。

## 运行与证据

在本目录运行 `python run_all.py`。七条实际命令记录在 `run-summary.json`，对应日志见 `logs/`：

- `python -m unittest test_geometry -v`
- `python -O -m unittest test_geometry -v`
- `python -OO -m unittest test_geometry -v`
- `python run_examples.py`
- `python create_notebook.py`
- `python verify_notebook.py`
- `python draw_figure.py`

20项单测在三种模式通过；其中网格项为64个正整数构形，并覆盖等分、有理系数、旋转、反射、缩放、平移、点篡改、标签缺失/增加、非法输入。四算例包含偏分与等分。

[Notebook](teaching.zh-CN.ipynb) 五个代码格由标准库逐格 compile/exec，捕获真实stdout；新命名空间回放与已存输出逐字一致。**未启动Jupyter kernel**，execution_count为null，不能据此声称内核执行。Notebook以nbformat4结构生成，并通过逐格执行、输出回放和结构检查。

[原创SVG](figures/ii8-eight-cells.svg) 从已验证坐标生成，不复制原文扫描图。日志仅保存命令、结果、退出码与必要运行版本，未包含本地绝对路径或账户字段。`environment.json`给出Python版本。重新运行会更新本地证据，不自动发布。
