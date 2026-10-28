# Euclid I.39 最小教学复现

[中文深读](../../papers/ancient/euclid-elements-i39.zh-CN.md) · [逐步演练](WALKTHROUGH.zh-CN.md) · [Notebook](teaching.zh-CN.ipynb)

只使用 Python 3 标准库的 `Fraction` 有理数运算，不安装依赖。真实命令：

```sh
cd reproduction/euclid-elements-i39
python run_all.py
```

`run_all.py` 依次执行普通、`-O`、`-OO` 三模式单元测试、有限例子、Notebook 构建与全新命名空间重放，保存真实 stdout/stderr、退出码、环境版本和 SHA-256 清单。17 个单元测试在三模式均通过；例子批量为 180 个合法定理实例、7 个非法几何直接拒绝。测试另覆盖两反证分支各 10 个仿射/反射实例、严格类型、所有证书叶值篡改及同面积异输入移绑。

## 边界

- **原文**：I.31 作平行线，I.37 得辅助三角形与原三角形等积，再用整体大于部分排除错误位置。
- **教学补显**：辅助交点可在 BD 内或越过 D；两者交换整体与部分。其存在性与顺序须由几何论证说明，不能靠有限测试确立。
- **现代模型**：`construction_trace` 用行列式与有理参数计算 E。接受非等积的同侧非退化输入，**仅用于展示反证分支**；`make_certificate` 进一步要求等积，否则 `ValueError`。
- `A=D` 不确定直线 AD，故定理接口拒绝；零底、任一退化、异侧也拒绝。若分支示例 A=E，则 AE 不是由两不同点确定的直线；辅助支持线始终指 `A + λ(C−B)`，叉积零只是向量检查。
- 输入严格要求 A/B/C/D 四键、二元素 list，坐标只收 `int`（不收 `bool`）或规范有理数字符串。不收 float/NaN/∞。证书只收 JSON 字符串/list/object；完整规范化坐标绑定，额外/缺失/变更字段均拒绝。
- 证书重算是程序一致性检查，不是独立几何定理证明；实跑不是一般证明，也不是完整古典几何复现。
- 已读安装的 Notebook 技能；本机脚手架文件与技能对应资源均不可用，使用自有标准库构建器。5 个代码单元实际以 `compile/exec` 顺序执行并逐字节比对重放 stdout；**未启动 Jupyter kernel**。

证据：[真实运行摘要](run-summary.json)、[环境](environment.json)、[案例](results.json)、[Notebook 核验](notebook-check.json)、[文件哈希](SHA256SUMS.json)。
