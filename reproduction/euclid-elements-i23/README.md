# Euclid I.23：精确角复制教学复现

本包是原创现代坐标重构，不是对古代作图工具的模拟或全文翻译。I.23 原证调用 I.22 配置三边，继而调用 I.8（SSS）；这里直接解出满足三边条件的坐标，用精确有理数及单个正平方根表示坐标。**不是旋转作为原证，不是完整复现古代公理体系。**

## 输入和输出

`construct(C,D,E,A,B,side=1)` 接受二维点。C 为源角顶点，D、E 分别在源两条射线上；A、B 确定目标基射线。G 在 AB 射线上，F 在指定侧；AF=CD，AG=CE，FG=DE。D/E 只需为非顶点且不共线的截点，不要求 CD=CE，不要求 B=G。更换源截点可改变边长，不改变原来的两射线所夹普通内角。

坐标仅接受整数、有理数字符串、`Fraction`。拒绝浮点数、布尔值、错误维数、零射线、共线源射线；`side` 必须是整数 ±1。`side=1` 表示 AG 到 AF 的叉积为正（目标基射线左侧），-1 为右侧。普通角两支均相等，有向角只有匹配源方向的一支相等。

令 u=D−C，v=E−C，w=B−A；U=u·u，V=v·v，W=w·w，T=u·v，X=det(v,u)，Jw=(-w_y,w_x)。程序取 d=V/W，p=T/V，q=side×|X|/V，并输出

- G=A+√d w；
- F=A+√d(pw+qJw)。

证书中点表示为 `constant + sqrt(radicand) * sqrt_coefficient`，各系数均是规范有理数字符串。根式未做无平方因子化；即使 d 是完全平方数，表达仍精确。`checks` 保存 AF²=U、AG²=V、FG²=|v−u|²、AF·AG=T、det(AG,AF)=side×|X| 五条精确恒等式。G 位于 AB 正射线，因为 √d>0。

`verify(certificate,C,D,E,A,B,side)` 是**重新计算型校验器**，不是独立证明内核。它核查严格 JSON 类型并与规范证书比较，绑定源点、目标点和侧向；字典键顺序不重要，其他增删或修改均拒绝。尤其 Python 的 `True == 1` 不会让布尔字段冒充整数或反之。

## 真实运行

```sh
python run_all.py
```

仅依赖 Python 标准库，不安装第三方包。此命令顺序运行普通、`-O`、`-OO` 下的测试和案例，以及 Notebook 创建与执行，共 8 个子命令。真实命令、退出码、stdout/stderr 位于 `logs/`；`environment.json` 记录环境，`run-summary.json` 汇总。优化模式不删除 unittest 判定，生产代码和测试无 bare assert。

Notebook 包含 6 个代码格，通过 `compile/exec` 共享命名空间执行并保存真实输出，**不是 Jupyter kernel 执行**。已阅读安装的 notebook 技能；其脚手架 helper 在本执行环境未找到，因此以标准库生成原生 nbformat 4 文档，未添加依赖。执行器验证格数及代码运行，不等同于第三方 nbformat schema 全面验证。

32 个 unittest 覆盖 144 个正例、14 个非法输入，以及镜像、有理/巨大/近退化坐标、输入绑定、篡改和严格类型。各优化模式案例汇总应完全一致；具体根式和方向统计见 `results-normal.json`。源码、Notebook、日志与文档的 SHA-256 清单在 `SHA256SUMS.json`。

## 边界

有限案例不能证明一般命题；一般等式的推导见 [WALKTHROUGH](WALKTHROUGH.zh-CN.md)。输入限于有理坐标，不能表示一切原命题允许的任意实长度；也不处理曲线角、空间角、零角或平角。精确代数解算不检验古代圆交点存在性、公理独立性或作图工具误差。源文献、历史解释和 I.22/I.8 依赖请结合仓库正文阅读。
