# I.46 独立技术审查

结论：通过。本报告绑定正文 `papers/ancient/euclid-elements-i46.zh-CN.md` 的 SHA256：

`03ba93139f63d5ed46f41b3f6bec93b602c459fd0ca505c777a7782624cf8ed6`

## 数学与实现核查

- 原证先由平行四边形对边性质及AD=AB恢复四边等长，再由I.29和I.34传递直角，最后闭合定义22；没有反用I.47。
- 欧氏坐标模型另标为教学重构。非零u、v=±J(u)、等长正交、E交点及ADEB边界正确。第7节两侧唯一性证明针对输出正方形，不是辅助C唯一。
- 原文辅助线须可延长；程序选择C=A+2v并允许任意更远同射线C，是已声明的证书规格，不把二倍长度强加给原命题。
- A=(1,2)、B=(4,6)的两侧坐标以及第6、7题均独立计算复核。ADEB有向面积与side符号相反的说明正确。
- 非直角等边菱形、非等边矩形、等对角线不足、零长度及错误点序反例均成立；十五题答案与正文依赖一致。
- 验证函数直接核验几何，不重建候选后比较。独立测试把生产构造器替换为必报错函数时，手工证书仍能正常检查，确认验证路径不调用构造器。
- 输入类型明确排除bool、float、NaN、Inf、复数、字符串及非法方向；非法请求直接抛ValueError，非法证书返回False。正边长、四个转向及角边条件排除零图形与交叉配对。
- 原创双面板图已查看实际渲染：ADEB点序正确，红色AB与虚线辅助AC含义一致，两图C均在D外，没有标签裁切。

## 独立实跑

[独立检查器](independent_check.py)不用生产构造器生成主测试集：3个起点、24个非零有理方向、2个侧向，共144个另选合法证书。每例检查面积方向、输入保留、点扰动、任意合法辅助C、非法辅助C、元数据类型与额外字段。另有52次非法入口调用及正文算例、几何反例。

三个模式各 **3802 项检查通过**，全部退出码0：

- `python independent_check.py` → [日志](logs/independent-normal.log)
- `python -O independent_check.py` → [日志](logs/independent-O.log)
- `python -OO independent_check.py` → [日志](logs/independent-OO.log)

同时独立重跑原21单元测试，三模式均通过：

- `python -m unittest -v test_geometry.py` → [日志](logs/independent-unit-normal.log)
- `python -O -m unittest -v test_geometry.py` → [日志](logs/independent-unit-O.log)
- `python -OO -m unittest -v test_geometry.py` → [日志](logs/independent-unit-OO.log)
- `python verify_notebook.py` → [五格回放日志](logs/independent-notebook.log)

原48合法/12非法统计与附件一致；Notebook为标准库compile/exec和新命名空间回放，非Jupyter kernel测试。

## 审查中修正的测试预期

独立检查器初稿错误地要求“任意单坐标扰动C都必须被拒绝”。当正方形轴向放置时，这种扰动可能仍使C位于同一射线且在D外，因此证书应被接受。这是独立测试预期错误，不是生产验证器错误。已改为独立检查C的共线与超出D条件，三模式全量重跑通过。

初次真实失败日志保留：[normal](logs/independent-initial-normal.log)、[-O](logs/independent-initial-O.log)、[-OO](logs/independent-initial-OO.log)。其中仅将本地绝对文件路径替换为文件名，不改变异常类型、行号或失败原因；后续成功日志对应最终检查器。没有修改生产核心或正文来迎合错误测试。

有限实跑只提供实现证据，不证明全部实数实例、原尺规动作或一般定理；数学一般性由正文分层证明承担。所有运行已终态，无外部写入。正文若改变，需重新核验并绑定。
