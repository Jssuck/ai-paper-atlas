# Euclid I.23 独立技术审查

审查日期：2026-10-27。结论：数学推导、修正后的向量措辞、有限精确实现与所声明的执行边界相符。这里的“独立”指由未编写正文和生产算法的另一审查代理重新推导并实跑参考检查；不表示人类专家签名、第三方机构认证或证明助理验证。

## 1. 审查对象与关键结果

- 从原证调用结构检查 I.22 的三边构造与 I.8 的夹角认证分开；给定顶点、基射线和侧向是单独的输出约束，正文没有用量角器或现代旋转冒充原证。
- 重新推导 UV=T²+X²，其中 X=det(v,u)；正根 √(V/W) 保证 G 在 AB 正射线上，非零 X 保证两个分支非退化。
- 逐项核对 AF²=U、AG²=V、AF·AG=T、FG²=U+V−2T、det(AG,AF)=side×|X|。镜像只改变叉积符号，不改变普通夹角；有向方向只在对应的一支保持。
- 核对第 7 节手算中 d=5/2、F 系数 (−2/5,6/5)、G 系数 (1,1)；平方距离依次为 4、5、5。审查中修正“FG 的系数向量”为“F−G 的系数向量”，避免把无向长度和有向位移混用；来源审查同时纠正练习 11 的 DE=v−u。两处不改变平方长度结果。
- 核对原例、反例、20 道练习答案及有限复现口径，没有从有限测试外推一般定理。

## 2. 不共享几何辅助函数的参考核验

[独立检查器](../../reproduction/euclid-elements-i23/independent-review/check.py)使用有理数对 (a,b) 表示 a+b√d，自行实现加、减、乘法；从证书 F/G 的坐标重新计算三条平方距离与叉积。没有调用生产代码的 dot/cross/sub，也不把证书 checks 字段视为几何真值。它仍调用生产 construct 取得候选，随后用另一条算术路径核验候选。

实际检查：源臂坐标分量取 −2 至 2，去除零向量与共线组合；3 个目标位置/方向、2 个侧向，共 **2976** 组。每组三条平方距离的根式系数均严格为零，常数与源距离平方相符；正射线、正根、指定侧也通过。另检查 **21** 份篡改证书及 **2** 次外部输入重绑定，全部拒绝。代码、[真实结果](../../reproduction/euclid-elements-i23/independent-review/result.json)和[命令退出码日志](../../reproduction/euclid-elements-i23/independent-review/run.log)一并公开。

这些是所述有限网格的实跑结果，不是所有有理输入或实数输入的穷举。一般恒等式依靠正文代数推导；本检查器本身也不是形式证明内核。

## 3. 类型、绑定与实现边界

生产 verify 为重算规范证书后比较 JSON 文本的校验器，不是独立几何核。审查确认 strict_json 要求内建类型，序列化比较区分 true 与 1，拒绝额外/缺失字段、篡改根式和坐标、NaN、浮点值、tuple 冒充 JSON 数组等。输入源点、目标点与 side 均纳入绑定，字典键顺序可以改变。

等价但非规范的根式表示可以被拒绝；这只是接口规范，不是判其几何错误。检查范围是有限、可序列化输入与所列非法输入，不承诺处理任意递归 Python 对象或无限资源攻击。

审查代理另行重跑普通、-O、-OO 下的 **32 项 unittest**，各自通过。生产证据的 **144 正例、14 非法输入、126 非有理尺度、72 反向分支**与代码循环和输出相符，三模式一致。程序不依靠会被优化删除的 bare assert 来验收。

Notebook 为 **6 格标准库 compile/exec**，不是 Jupyter kernel；输出来自真实执行。环境、命令与退出码见复现目录，不把未执行的浏览器 Notebook 渲染或完整 nbformat schema 检查写成已通过。

## 4. 绑定摘要

以下 SHA-256 绑定本次审查的最终文本与实现。内容变更后需要重新核对，不将摘要当作签名。

| 文件 | SHA-256 |
| --- | --- |
| `papers/ancient/euclid-elements-i23.zh-CN.md` | `844fee59fbc8390d93edbc3942abf6eb06496376eda5af9a99e966117521e3d6` |
| `reproduction/euclid-elements-i23/geometry.py` | `1fe89f6a41fab7030b273b2cf6cfb7067c7ceb46b7b6c16373ae5408f4ac4986` |
| `reproduction/euclid-elements-i23/test_geometry.py` | `5a8600b235d018dec5cd37b9cedfdb708bcc61f28a9c8681f7e7c3372eec73e3` |
| `reproduction/euclid-elements-i23/verify_notebook.py` | `1ac2b37a6e55b495061aad2c612bac62739709050ac20237e517e3f8271da6d0` |
| `reproduction/euclid-elements-i23/teaching.zh-CN.ipynb` | `0802a003208149df36e7ad922b1549bf290fc46d43e386b142d6a6c7b39a7652` |
| `reproduction/euclid-elements-i23/independent-review/check.py` | `c31ddd2ed0a1c738b378703ed17f9909fa91bfaca42d8144a21413a01f70a8c0` |
| `reproduction/euclid-elements-i23/independent-review/result.json` | `b6a665650771ae78e63a26d62d02130ed9c9a16429b82336ccb71cfc21f50cee` |
| `reproduction/euclid-elements-i23/independent-review/run.log` | `3513573f8ce5e8895a3dd2962517b96a489963df3049e2bcfb4951ddbcba0475` |
| `reproduction/euclid-elements-i23/SHA256SUMS.json` | `a0d74fc250c787e387c9d3a53c636f1772af41fa2e953be8669f3a5c66fee9ea` |

最终 Notebook 核验保留 execution_count=null，以 metadata.compile_exec_index 记录本地逐格核验序号 1–6；修正后完整 8 命令重新执行并通过。
