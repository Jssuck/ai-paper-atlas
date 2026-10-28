# Euclid I.35 独立技术审查

- 审查日期：2026-10-28（UTC）。
- 结论：本次检查未发现阻止发布的数学、输入校验或实跑一致性问题。
- 被审正文：[中文深读](euclid-elements-i35.zh-CN.md)。SHA256：`a478a5798edc505d7f5abfae79188d9b092fc524abe481592027396956ec2d35`。
- 被审核心：`geometry.py` SHA256：`ec7d9128ff33289548b68d541a6f6c1b15cdb9881811d3ec0439fde29acecc76`。
- 独立探针：[independent_probe.py](../../reproduction/euclid-elements-i35/independent_probe.py)，SHA256：`44ddf420bf6f041e3d80616c280ffd625f07ef12fd9411f39914090a62bacb6c`。

## 数学与教学分层

逐项复核了正文、核心程序、作者测试、案例、复现说明和 Notebook 回放脚本。原文分离图形下，先由 I.34 得相应边相等，由 I.29 得夹角相等，再由 I.4 得三角形全等；随后减去共同三角形、加上共同三角形，确实推出目标平行四边形等积。此处没有用底乘高或后续三角形面积命题替代原证。

上边重叠时应从相等上边减去共同线段，不能照搬分离情形的“加 DE”。正文分别处理重叠、相接、完全重合及负向平移。相接时共同区域退化为三角形；完全重合独立返回，不对零面积三角形错误使用 SAS。统一外梯形减去全等三角形的论证已标为教学重构，与原文切拼路线区分。

坐标层中，非零行列式、两条上边均等于有向底边，以及上边位移与底边平行，共同保证合法非退化平行四边形，而不是仅检测两个多边形面积相等。负移位经交换目标图形归入正移位。分离分支的交点为 `G=b+u+v/t`，仅在 t>1 时处于所需内部区域；正文 t=1/2 的交点位于外部，不能沿用分离图。手算 t=2、1、1/2 的各块面积、相同面积而非全等的边长例子、错高度及非平行四边形反例均复核正确。

行列式面积是现代坐标核验层，不冒充欧几里得原证。一般证明依赖明确的区域包含和有限可加性；有限程序样本不是一般定理的证明。

## 独立攻击与真实执行

独立探针没有仅重复作者断言：另行实现精确有理数鞋带面积和凸多边形裁剪，直接计算两个大三角形及两个平行四边形的交集，交叉检查切拼区域的值。生成族含水平、竖直、斜基、旋转与反射、有理基向量、平移，以及负向、零、重叠、端点相接和分离的全部分支。非法几何逐点扰动 A/D/E/F、塌缩底边、倒转上边；证书攻击逐层修改、删除、增加字段并尝试重新绑定不同输入；非法输入覆盖布尔、浮点、空值、容器、非法及非规范有理数字符串等。

在复现目录实际执行下列命令，全部退出码 0，全部取得终态：

```bash
python3 independent_probe.py
python3 -O independent_probe.py
python3 -OO independent_probe.py
python3 test_geometry.py
python3 -O test_geometry.py
python3 -OO test_geometry.py
python3 verify_notebook.py
```

每一种独立探针模式均通过：

| 检查 | 每模式数量 |
|---|---:|
| 合法仿射几何案例 | 1023 |
| 非法几何直接拒绝 | 10230 |
| 证书攻击拒绝 | 735 |
| 非法输入直接拒绝 | 660 |
| 独立精确交集检查 | 930 |

三模式的作者测试均为 27 项通过。Notebook 回放为 6 个代码单元、保存输出匹配；执行方式是标准库 `compile/exec` 回放，不是 Jupyter 内核运行。独立探针使用显式失败检查而非 `assert`，优化模式不会删除其判定。

真实日志：独立探针[普通](../../reproduction/euclid-elements-i35/logs/independent-normal.txt)、[-O](../../reproduction/euclid-elements-i35/logs/independent--O.txt)、[-OO](../../reproduction/euclid-elements-i35/logs/independent--OO.txt)；作者测试[普通](../../reproduction/euclid-elements-i35/logs/independent-tests-normal.txt)、[-O](../../reproduction/euclid-elements-i35/logs/independent-tests--O.txt)、[-OO](../../reproduction/euclid-elements-i35/logs/independent-tests--OO.txt)；[Notebook 回放](../../reproduction/euclid-elements-i35/logs/independent-notebook.txt)。

## 边界与保留意见

证书校验是对完整输入重新计算预期证书并严格比较类型和内容，并不是独立形式化证明内核。坐标限定为整数或规范有理数字符串，拒绝浮点及布尔值是接口设计，不表示这些数不存在几何意义。多边形裁剪仅用于已构造的凸图形核查；样本覆盖多种任意方向的代表，不声称穷尽所有实数坐标、所有攻击或一般定理。此次技术审查不替代独立书目来源审查，也不替代发布后的远端内容、链接和公式实际显示验证。
