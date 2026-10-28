# Euclid II.2 独立技术审查

审查日期：2026-10-28。结论：**修正后通过本记录列明的技术检查**。审查者是独立AI代理，不是人类专家或证明助理。本文结论不代替独立来源审查与发布后的页面显示验证。

## 绑定版本

最终正文 `papers/ancient/euclid-elements-ii2.zh-CN.md` SHA256：

`1fd4c95dea9e2ebd264c7c0c79234b91d77f78ee1c37380bd4374f7f91541b64`

| 文件 | SHA256 |
| --- | --- |
| geometry.py | `047ec7c1eb45ae5faea7745883fb6e6e869b234dc7e354e5d8e854d3b8d92cf6` |
| test_geometry.py | `2523492ae0f1445f2963279894df6ab1c89456c9e2078f6e529a848c45ff049d` |
| independent_check.py | `6cec2b4eca35c32cc000ffe998b95f6024c87ee9c589425be002d1146b6e5980` |
| create_notebook.py | `418e223c043925694023557837aef76eb6e0868ddeab46282370c7bd15eb7824` |
| verify_notebook.py | `6608674b4bf018cb43df7c854129d74146b0d88f2d4ce68cfeb6a533b117f546` |

## 独立复核内容

- 实际通读正文、几何实现、测试、Notebook生成与回放程序及结果文件，不仅依据作者摘要。
- 核对正方形A-D-E-B、分割点A-C-B和D-F-E、区域AF=A-D-F-C、CE=C-F-E-B，以及原证使用DA=AB和BE=AB辨认矩形的数学关系。
- 检查第5节参数映射的单射性：非零垂直向量独立，两个参数区间内部不交且覆盖整体；不是仅用面积和相等推断覆盖。
- 核对现代式的前提L>0、0<x<L及II.1的共同高等于整段这一特例条件；现代算术检验没有被说成原几何证明或分配律的无循环基础。
- 独立手算正文整数、分数、斜置例；斜置C=(11/5,−2/5)、F=(−9/5,13/5)及面积10、15均正确。外切、非等边矩形、非正交等边菱形、对角线误读的反例成立。
- 检查生成器与验证器：`verify`不调用`construct`，通过逆解仿射坐标重新核验点位，并把区域顶点绑定到固定点名；验证正方形输入、各块直角及共边后才计算鞋带面积。

## 初审问题、修正与重新执行

1. 初稿 `verify` 只用集合比较检查 `points` 键；`points=list('ABCDEF')`会通过集合检查后在`.items()`抛出AttributeError，而不是返回False。已增加明确的字典类型检查，并新增第29项回归测试，覆盖列表、元组、字符串、集合和None容器。该漏洞涉及坏证书拒绝行为，不是有效几何实例面积公式错误。
2. 初稿Notebook虽声明未启动kernel，却把execution_count设置为序号。现改为null，保留真实stdout及compile/exec说明，避免把普通Python执行呈现为内核计数。
3. 正文明确原创图与原图上下方向不同，且练习区分长度数值缩放与单位大小变化。复读了修正后的统计、图示方向和单位表述。

完成上述代码修正后真实运行 `python run_all.py`，**7条主命令全部exit_code=0**。普通、`-O`、`-OO`各29项unittest全部通过；其中网格项检查64个合法构形，不与测试项数相加。

独立复核新增 [independent_check.py](independent_check.py)：每模式检查90个有效构形，并按点位移、区域反序、坏容器及非正方形输入进行819个拒绝检查。分别在普通、`-O`、`-OO`真实运行，均退出0，原始日志为 [normal](logs/independent-normal.log)、[-O](logs/independent-O.log)、[-OO](logs/independent-OO.log)。独立预期整块面积用边向量平方长度计算，与多边形鞋带路径交叉比较。

Notebook有11个单元，其中5个代码格。实际顺序compile/exec执行和新命名空间回放输出一致；全部代码格execution_count为null。未启动Jupyter kernel，未做Jupyter界面渲染或完整nbformat第三方模式验证。

## 边界与未声称事项

有限有理数实例和篡改测试不证明任意实数长度的一般定理，不构成对《原本》的完整形式化；输入输出类型合同并非面对任意有恶意行为的Python对象的安全沙箱。核心运算仅接受整数/Fraction坐标。原图SVG的浏览器目视与公开GitHub公式实际显示由发布核验单独负责，不能用本技术记录代替。公开包未包含原PDF、全文译文、账户信息、秘密或私人对话。
