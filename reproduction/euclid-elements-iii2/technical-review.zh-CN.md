# III.2独立技术审查

核验日期：2026-10-29。结论：当前正文及实现通过本次有限范围的独立技术核验。这里的“独立”指另行检查推导、构造不同坐标样本及对照计算，不是人类专家签名、形式化证明助理认证或第三方CI认证。

## 1 版本绑定

正文 `papers/ancient/euclid-elements-iii2.zh-CN.md` SHA256：

`697e4e9b0453d387cdf6c3133d36d654d97ca0e3a40a6ce99eeb9b60ed341994`

实现及证据文件SHA256：

| 文件 | SHA256 |
| --- | --- |
| `README.md` | `1538d6710d87812387b4f26042516559cd3c9841501264fbb496d37ad3b98f0e` |
| `geometry.py` | `557469159e2366c5e44b00df90dd7ac75ed8191f3b02c74a8dd4404a16418dd0` |
| `test_geometry.py` | `1790be991fb137d4470139ebf1db24d7ad2fc882712b18cc1a1a6b1fe534aa8f` |
| `independent_audit.py` | `88c75d9d531f7f38d7c1476770379d2ec271c53a278bbf84a7de71e6b6c83ccb` |
| `create_notebook.py` | `b1d579f2a6000597789572f46e7d9beef5ef01bc7624611e64b00afafa7bfe5d` |
| `verify_notebook.py` | `034863341dbae98039650809b5a5489388227286626ba1988c58bf002c72ef4f` |
| `teaching.zh-CN.ipynb` | `3303c71b46968299558f267d9f213eebf1778197937199695d948c107ad61a2c` |
| `draw_figure.py` | `f66cbcff5ede12fa8e3587ea16a2fa18cfe955a6e9bc38b99439722da5fc35d7` |
| `figures/chord-interior.svg` | `b44d265901ddff416e430213e18a99354ce57cf08a632d2ce2be65bc36bf39af` |

哈希是此次复核版本标识；后续修改应重新检查，不能将本报告自动视为新版本的审查结论。

## 2 证明、条件和练习

- 非直径时D、A、B不共线，严格点序A–E–B保证DAE、DEB非退化，且AE/AB、BE/BA各为同射线。I.5的底角相等可以移到角DAE与DBE。
- I.16用在DAE，外角是DEB；I.19用在DEB，大角DEB对边DB，小角DBE对边DE，得到DB>DE。没有把不同三角形的边角混用。
- 外点反证的D–F–E给DF<DE，与DB=DF及DB>DE冲突。圆周分支不需要F，由DB=DE直接冲突。正文明确承认径向内外及点序基础没有被程序公理化。
- 直径情形不套角定理：等距且互异的两端位于D两侧，再按E=D或在D一侧分三种点序。中心零射线未被错误定义为角。
- 独立展开平方得到 `r²−DE²=t(1−t)|A−B|²`。三个因子的正性要求严格内插与不同端点；t=0或1归边界，外插余量负。模型不要求半径本身有理，只要求输入的半径平方可精确表示。
- “至多两个交点”按三个不同共线点的中间点反证，不偷换为交点存在性。一般凸集反例与圆盘严格性说明适当。
- 正文五行数值表、近端点、半径平方26的错误前提和八道习题答案逐项核对。四分点DE²=73/4、余量27/4；三分点17与8；t=1/100时61609/2500与891/2500；外插t=3/2时52与−27。直径行换端点后弦平方为100，不误用36。

修订后复查了正文图链接与图示范围：使用实际存在的chord-interior.svg，仅描述非直径弦及中点；外角DEB误写成内角DEA的教学警示也已明确。

## 3 实现独立检查与真实实跑

`geometry.py`只接收准确类型的整数或Fraction，排除bool和浮点；检查r²>0、端点不同、两端确在指定圆周及闭区间参数。证书复核要求完整键集合、正确字段类型和重新计算的全部字段；拒绝把布尔值或整数别名冒充输出Fraction。中心、端点与严格内点分支符合规格。未发现依赖可被优化模式移除的assert来执行输入验证。

独立检查器没有复用生产网格：采用12个显式有理圆周点、66对端点、三种变换（含负尺度及旋转平移）和六种内插比例（含1/10²⁴），独立点积计算并检查端点反转不变性。逐项篡改证书字段，另外检查bool别名、列表冒充元组、非法输入和缺键等畸形记录。

每种解释器模式的实际结果如下；这些计数是各模式重复的有限检查，不是互不相交的全新样本或三个独立实现。

| 检查 | 普通 | -O | -OO |
| --- | ---: | ---: | ---: |
| 生产单元测试 | 23通过 | 23通过 | 23通过 |
| 独立有效证书 | 1188 | 1188 | 1188 |
| 独立篡改拒绝 | 17820 | 17820 | 17820 |
| 独立非法输入拒绝 | 54 | 54 | 54 |
| 独立畸形证书拒绝 | 68 | 68 | 68 |
| 手算/扩展示例 | 8 | 8 | 8 |
| Notebook代码格对照 | 5 | 5 | 5 |

全部进程退出码为0。生产23项单测中每模式含900组网格；独立1188组不是把这900组重复计数。生产run_all.py另重建了5命名算例、Notebook及SVG。

在本目录执行的独立命令：

```sh
python -B test_geometry.py
python -B -O test_geometry.py
python -B -OO test_geometry.py
python -B independent_audit.py
python -B -O independent_audit.py
python -B -OO independent_audit.py
```

实际日志：[单测普通](logs/independent-tests-normal.log)、[单测-O](logs/independent-tests-O.log)、[单测-OO](logs/independent-tests-OO.log)；[独立普通](logs/independent-audit-normal.log)、[独立-O](logs/independent-audit-O.log)、[独立-OO](logs/independent-audit-OO.log)。环境见[environment.json](environment.json)，生产完整命令见[run-summary.json](run-summary.json)。

## 4 Notebook与图形

Notebook重新生成并顺序compile/exec保存输出后，独立检查器以只读方式再次顺序执行五个代码格，逐格比较标准输出与保存输出，并核对文件前后字节哈希不变。这是Python标准库回放，**不是Jupyter kernel执行，也不是nbformat完整模式验证**。重跑不覆盖保存证据来制造匹配。

SVG已实际渲染为图像并目视检查：圆心D、端点A=(−3,4)、B=(3,4)、中点E=(0,4)及橙色弦、绿色DE相符；25、16、9的标注正确，文字可读，没有用可实现图冒充原证的不可能外点假设。此处为本地SVG渲染核验，GitHub页面公式与图片实际显示须另在发布阶段核查，不能由此报告替代。

## 5 限制

没有发现阻止当前版本发布的技术错误。有限精确有理样本和篡改检查只检验实现与模型的一致性，不能证明所有实数构形，更没有形式化认证古典几何的连续性、点序或全部依赖。正文的全称论证与有限实验分开承担责任。本报告不声称图像识别、浮点鲁棒性、性能优越性或AI模型测评结果。
