# Euclid I.11 独立技术审查

结论：**通过本次声明范围的技术核验**。审查与正文写作、复现实现分工；没有声称人类专家认证或证明助理验证。日期：2026-10-27。

## 绑定对象

正文：[I.11 深读](euclid-elements-i11.zh-CN.md)

正文 SHA-256：`37b102ea3c8c8cdf2d3ba8c9058342a4aa2b5325fd21d819473e459defa98eb0`

以下源码逐一绑定；若正文或代码改变，应重新核查相关结论并更新绑定，而不沿用旧审查。

| 文件（相对复现目录） | SHA-256 |
|---|---|
| `geometry.py` | `825fc5c7c67c8515a23296880b0766b6b15b873d7742fd196b04516f6dabba53` |
| `cases.py` | `e7aecbe0688c333c7d71b33b793659261316e111333996476ad803ee80e62720` |
| `test_geometry.py` | `7d228dbf96f53647bc6e4c8e79d6ebce3419064292b7a73d76da930f30355596` |
| `run_all.py` | `b2fe28df044f9c67ad9ed9fc3f6b1a65660d6708fee55e276e18d626b3987376` |
| `run_examples.py` | `a4db2940a19f64ce41b574093266af84f9303cc04fd186780b500986a71a8f56` |
| `verify_notebook.py` | `4a26a33e9fc3ae1148c418ccfd3ce73de725a7cd67d45d3d49369a7d8d9ac397` |
| `create_notebook.py` | `0ee8f911610d920b097b144d603b31f0c8de4b607eb6d0e3614286dcd9cfa5ba` |
| `independent-review/checks.py` | `521b9bba3c679a774cdcf1c0c14bc7bd9a52e3b7d1cee5440fbf24376aebf705` |

## 数学逐项核验

1. 原构造的目的与条件明确：先使 D、C、E 共线且 C 严格居中，CD=CE，再用 I.1 提供 DF=EF=DE。三边对应为 D↔E、C↔C、F↔F，I.8 推出 C 处等角；相反底线射线与非零 CF 才允许按定义 10 认作直角。正文没有用后来的三角形内角和或 I.13 反向支撑原证明。
2. I.3 的较长承载段前提、内点选择半径的约束与端点需要延长均已明确。程序输入是闭 AB 上的有理坐标点，允许辅助点越出原段；不会把这一 API 说成正文图式的逐字端点覆盖。禁止延长原 AB 的评论方案与主构造分开，未声称已完整复现其交点存在性。
3. 坐标式 D=C−hv、E=C+hv、F=C±√3hJv 的平方距离和点积推导正确；h 是无量纲比例，不是绝对长度。两圆方程相减得到 x=0，再得 y²=3r²，存在性补证被明确放在现代实数平面，不冒充古代许可步骤。
4. 两个顶点对应相反射线，而无向垂直直线相同；二维一般唯一性按 p≠0 与 p=0 分情况成立，非零向量保证比例非零。三维不唯一的限制已说明。
5. 正文的非中点内点、端点越界、等边但不等距、30°角平分和零向量反例逐项正确。一般证明与有限测试、几何结果与操作合法性没有混淆。

## 实现与证据核验

- `Q3` 使用有理系数表示 a+b√3；乘法、共轭除法和符号判定经代码阅读及独立运算核验。原始坐标与截距拒绝浮点、布尔及不合类型；不以浮点容差决定等距或共线。
- `check_certificate` 从可信输入重新计算证书条件，不信任证书提供的通过标志。它检查输入绑定、截距与分支、共线、相反非零射线、等距、等边、非退化、三边前提和现代结论。现代等角检查同时保留余弦分子符号，避免仅平方导致补角混淆。
- 仅满足垂直而未满足此次等边构形的候选会被拒绝；将 F 设为 C、改变坐标、改输入或分支也不会误收。这里验的是受限构形证书，不是一般尺规证明语言。
- 原始日志与 `run-summary.json` 相符：三模式各 28 tests、864 正证书及 12 负证书，案例结果相同。审查者另外重跑三模式单测，全部退出 0。
- 审查者自写的系数检查没有调用实现的距离函数来建立预期等式；对 864 正例直接计算 D/E/F 有理系数及三条平方边长。另核 12 负例、1156 组字段算术、18 次逐坐标非零篡改，并核正文不等距等边反例，全部通过。有限枚举仍非全输入域定理。
- 读出保存的 Notebook 后，以新的共享命名空间重新顺序执行 6 个代码单元，标准输出与已保存输出逐字匹配。执行器是 Python 标准库 compile/exec，**不是 Jupyter kernel**，也不构成 Notebook 页面渲染或完整 nbformat 模式认证。

独立证据：[核查脚本](../../reproduction/euclid-elements-i11/independent-review/checks.py)、[核查真实输出](../../reproduction/euclid-elements-i11/independent-review/checks.log)、[普通模式重跑](../../reproduction/euclid-elements-i11/independent-review/tests-normal.log)、[-O 重跑](../../reproduction/euclid-elements-i11/independent-review/tests-O.log)、[-OO 重跑](../../reproduction/euclid-elements-i11/independent-review/tests-OO.log)、[命令与退出码](../../reproduction/euclid-elements-i11/independent-review/run.json)。可在复现目录运行 `python3 independent-review/checks.py` 重做独立检查。

## 修正与未覆盖事项

审查发现正文最初的复现说明链接指向不存在的 `README.zh-CN.md`，现已改成真实的 `README.md`；当前绑定正文已包含真实统计与附件入口。未发现需要修改算法或数学论证的阻断问题。

本报告不代替独立来源校核，也不承担远端 main 提交、所有链接或 GitHub 公式截图验收。未检查其他输入模型、物理尺规误差、完整几何公理系统、Heron 评论方案的全部操作、通用自动证明搜索或全部潜在 Python 实现缺陷。公开代码与日志为原创教学成果；内部工作路径及原始文献截图不属于这些公开附件。
