# I.15：对顶角的精确教学核验

这是[中文深读](../../papers/ancient/euclid-elements-i15.zh-CN.md)的原创教学代码，不是古代文本的形式化认证，不是几何软件基准，也不把有限回归当成一般证明。

## 两层模型

1. **有理坐标层**：输入五点A、B、C、D、E。要求四条射线非零，B−E为A−E的负正比例，D−E为C−E的负正比例，且A−E与C−E行列式非零。故E分别位于两线段内部，支撑直线不同并相交于E。该层验证对顶角相同的尺度不变描述。
2. **角量账本层**：以一直角为1，单独输入正有理数x、y、z；若x+y=2且y+z=2，同减y得到x=z，进而四角和4。它不声称由有理坐标得到有理角度；两层输出不得拼成未经证明的角度转换。

对非零向量u、v，令d=u·v，s=|det(u,v)|；描述是(d/(|d|+s), s/(|d|+s))。它保存(cosθ,sinθ)的上半平面方向，故在普通角区间[0,π]内唯一识别角量；不是只用cos平方而丢掉锐钝信息。无需开方或浮点acos。几何输入层排除共线的0、π退化角。一般等角论证见正文；这里的代码只是有限实现检查。

## 运行

Python 3标准库，无安装、无网络请求。进入本目录：

```sh
python run_all.py
```

该命令按顺序运行三种模式的测试及例子，再创建并执行Notebook。单项运行：

```sh
python test_geometry.py
python -O test_geometry.py
python -OO test_geometry.py
python run_examples.py
python create_notebook.py
python verify_notebook.py
```

`run-summary.json`保存实际命令参数、UTC时间、耗时、退出码；`environment.json`保存实际Python/系统及未使用可选包的检测。`logs/`为真实stdout/stderr。当前实际三模式各32个测试，135个有效配置、13个非法输入、168个角量账本，结果一致。`assert`不用于优化模式下的正确性关卡。

Notebook `teaching.zh-CN.ipynb`共6个代码格；`verify_notebook.py`以共享命名空间compile/exec顺序实跑并写入真实输出。**没有启动Jupyter kernel，也未声称Notebook浏览器渲染验证。** 已阅读安装的Notebook技能，模板脚本在本执行器不可读，因此由标准库创建原创合法Notebook结构；未安装替代软件。

## 文件与边界

- `geometry.py`：输入检查、角描述、证书、严格JSON验证和同减账本。
- `cases.py`：确定性有限样本，不是穷举所有有理/实数输入。
- `test_geometry.py`：32回归，含错向、零向量、类型混淆、缺字段、篡改、输入不匹配。
- `create_notebook.py` / `verify_notebook.py`：Notebook构造与真实执行。
- `SHA256SUMS.json`：本目录公开文件哈希（排除自身与缓存）；最终发布若加入审查文件须刷新。

证书验证比较严格JSON序列化，而不是Python的宽松值相等：True与1不同，浮点数（包括NaN）、元组、非字符串字典键不能混入证书。输入坐标只接受整数或有理数字符串；输入会规范化，例如"2/2"与1同一有理坐标，不承诺保留输入文本拼写。此核验器不是针对任意敌对Python对象的安全沙箱，也不提供资源消耗限制。类型契约、有限覆盖、数学证明三者不能混同。

可核验结果仅限此处模型、输入与程序；不包含尺规实物测量误差、所有欧氏公理、古代传本正确性或作者发现顺序。
