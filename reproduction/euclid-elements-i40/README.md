# I.40 最小复现：等底共线、同侧等积与平行

这是原创 Python 标准库 `Fraction` 有理坐标教学模型，不是《几何原本》的形式化证明。原文依靠 I.31、I.38 与整体大于真部分；坐标面积仅用于独立检查有限实例，不能替代该依赖链。

## 字母映射与模型范围

原文比较 ABC 与 DCE，底 BC、CE 共端 C，辅助平行线交 CD 于 F。本代码为检查底的位置变化，显式推广为 **ABC 与 DEF**：原 C 在两底的角色拆为模型 C、E；原 E 改名模型 F；原辅助 F 改名 G。原图子情形设置模型 E=C、模型 F=2C−B。本模型允许两底分离、交叠、共端、重合和反向；这些不是声称原图全部画出的位置。

所有坐标要求整数或规范分数字符串，例如 `"1/2"`；拒绝 bool、浮点、非规范 `"2/4"`、错误字典键和点形状。两底必须非零、等长、在同一直线上，两个非退化顶点位于该线同侧。`make_certificate` 还要求等积。`construction_trace` 故意允许不等积，用于演示反证内外分支，不将这类输入标为满足命题。

若 A=D，命题“AD 平行”没有定义；程序返回 `AD undefined; common parallel through coincident apex`。该分支只记录共同顶点的平行线存在，不冒称重合点定义直线。辅助 G=A 时 AG 也不定义；`cross.BC_AG=0` 是位移向量数值记录，不是对零向量作直线命名。

## 文件和运行

- [geometry.py](geometry.py)：解析、合法几何验证、辅助构造、证书及严格重算。
- [cases.py](cases.py)、[test_geometry.py](test_geometry.py)：固定例、非法例、20 项单元测试。
- [run_examples.py](run_examples.py)、[results.json](results.json)：168 个合法输入（含 84 个顶点重合边界）、9 个非法输入直接拒绝及两种非等积反证分支。
- [Notebook](teaching.zh-CN.ipynb)、[create_notebook.py](create_notebook.py)、[verify_notebook.py](verify_notebook.py)：五代码格，真实标准库 compile/exec 输出及全新命名空间回放，不是 Jupyter kernel 执行。
- [环境](environment.json)、[运行命令与退出码](run-summary.json)、[测试日志](logs/tests.log)、[优化模式](logs/tests-O.log)、[双优化模式](logs/tests-OO.log)、[示例日志](logs/examples.log)、[Notebook构建日志](logs/notebook-build.log)、[回放日志](logs/notebook-replay.log)。

在本目录执行：

```sh
python run_all.py
```

脚本在 normal、`-O`、`-OO` 三模式分别运行 20 项测试，随后生成案例与 Notebook 并核对其全部 stdout。核心校验不依赖 `assert`，优化不会移除校验。读取了已安装 notebook skill；本机没有其 `new_notebook.py`，未安装任何额外依赖，使用原创标准库 builder。Notebook 可在常规 Jupyter 中自行运行，但本轮并未声称做过 kernel 回放。

## 证书与局限

证书包含规范化后的所有输入点、平方底长、辅助点 G、比例 t、分支、各双面积和方向行列式。验证器从输入重算全部字段，限制证书为 JSON string/list/object 树；同面积换顶点、字段篡改、数值布尔替换和额外字段均不能通过。非法几何先被 `make_certificate` 拒绝，而非仅借助空证书得到 False。

这是一个可检查的教学计算协议，不是独立于生成器的证明核；同一函数重算无法发现其自身共有缺陷，因此仍须独立技术审查和原文证明重建。有理数点不穷尽实数平面；有限运行不证明一般定理，不证明 I.31/I.38，更不证明第五公设。程序使用现代行列式与有理数域，而非古代面积演算。
