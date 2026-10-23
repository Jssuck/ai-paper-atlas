# II.11 教学复现：内部第一格与正确的归谬目标

本目录是原创、低成本的现代集合模型，不是古代程序的复现，也不是完整自然语言证明器。对应[中文精读](../../papers/ancient/aristotle-prior-analytics-ii11.zh-CN.md)所读《前分析篇》II.11。原文完整阅读采用Owen1853印204–207和Jenkinson《Prior Analytics》Book II第11章电子转录；所见文字问题由正文与独立来源审查处理，不把译文误字写入规则。

## 语义和范围

`U(P,S)`：每个S都是P；`E(P,S)`：没有S是P；`I(P,S)`：有S是P；`O(P,S)`：有S不是P。谓项在前。整句矛盾为U/O、E/I；不能把I与O当作互否。

论域非空；分别使用允许空项及A、B、C全部非空两种政策。第二种只是敏感性对照，不断言古文要求所有项都存在。程序还单独检查原文全称背景的C存在条件，避免用过强政策遮蔽最小条件。

每个对象只记录是否属于A、B、C，共8种成员类型；`t`的二进制位0、1、2依次代表A、B、C。每个非空类型支持集只放一个对象，得到255个模型；三项均非空过滤后有218个模型。对象重数对这里的四种无等号一元命题无影响。此解释说明枚举的边界，不能用运行次数替代一般证明，更不能推及模态、关系、计数或现实命题。

## 128个候选如何产生

目标固定为`Q(A,B)`，暂时假设为它的整句矛盾H。只允许**一个内部第一格三段论**，不先换位、不增加中项、不允许多步绕行：

- H作大前提：`H(A,B)`与`X(B,C)`，候选内部结果为`R(A,C)`。
- H作小前提：`X(C,A)`与`H(A,B)`，候选内部结果为`R(C,B)`。

Q、X、R分别四型，假设两种位置，因此每种政策128候选。C可统一代表原文某些B侧例中的D，因为每条路线只使用三个不同项。

每条路线分开检查：
1. 内部两前提有模型且保真地推出R。
2. 独立背景是X及R的**整句矛盾**，该背景可满足。
3. 该背景推出目标Q，即假设撤除后的结论。

`certificate`是三项检查都通过的教学标签，不是形式证明助理的内核证书。失败内部推导附最小支持集反模型。无效内部推导有时仍可能被背景另行推出目标，所以不能只凭第3项回头称内部路线有效。

## 实跑结果

|政策|模型数|候选数|U目标有效路线|E目标有效路线|I目标有效路线|O目标有效路线|
|---|---:|---:|---:|---:|---:|---:|
|允许空项|255|128|0|2|2|4|
|三项非空|218|128|0|2|3|7|

这是本目录明示的候选语言及结果粒度下的计数，不是原文给出的数字。全项非空新增4条涉及UUI或EUO的弱化结果；没有把它们冒称4个新独立三段论式。第一格不能以特称否定O作为这里有效的内部前提，故目标U要求的假设O没有路线；这不等于任意多步或任意逻辑系统不能证明U。

另有11个具名蕴涵检查和1个I/O共真实例：
- `U(B,C), U(A,C) → I(A,B)`允许空项时失败，最小反模型C为空；添加C非空即可成立，不需要另添A、B非空。
- 把`U(B,C)`改为`I(B,C)`会自带存在见证。
- E目标核C-A肯定和否定两条；O目标核A侧与B侧、全称与特称等路线。
- `非E → U`和`非U → E`都失败，程序以等价的I与O作前提输出反模型。
- 混合模型A={7}、B=C={6,7}满足I(A,B)与O(A,B)，也满足U(C,A)及I(C,B)。E(C,B)为假；因此不能把这个为真的I假设连同真实背景归谬为假。

精确矛盾背景与原文可能使用的更强已知命题须分清：例如内部得到E(A,C)时，本表背景使用I(A,C)；原文用U(A,C)排斥E(A,C)还须C存在。`named_checks`单独保留这一差别。

## 文件与重跑

仅Python标准库，无安装、网络、密钥、数据下载或付费依赖。

一键执行并保存输出：`python run_all.py`。脚本遇到非零退出立即失败，并核对三份结果逐字一致。也可逐项执行：

```sh
python -m unittest -v test_reproduce.py
python -O -m unittest -v test_reproduce.py
python -OO -m unittest -v test_reproduce.py
python reproduce.py > evidence/results-normal.json
python -O reproduce.py > evidence/results-optimized.json
python -OO reproduce.py > evidence/results-double-optimized.json
cmp evidence/results-normal.json evidence/results-optimized.json
cmp evidence/results-normal.json evidence/results-double-optimized.json
```

- [一键运行脚本](run_all.py)、[源码](reproduce.py)、[12项回归测试](test_reproduce.py)。使用unittest方法，不依赖优化模式会删除的裸assert。
- [运行环境](evidence/environment.txt)。其时间为实际执行环境记录。
- [普通测试](evidence/tests-normal.log)、[-O测试](evidence/tests-optimized.log)、[-OO测试](evidence/tests-double-optimized.log)：均12项通过。
- [普通命令](evidence/run-normal.log)、[-O命令](evidence/run-optimized.log)、[-OO命令](evidence/run-double-optimized.log)。
- [普通结果](evidence/results-normal.json)、[-O结果](evidence/results-optimized.json)、[-OO结果](evidence/results-double-optimized.json)：逐字一致。
- [SHA-256清单](SHA256SUMS)标识生产文件及运行证据；不包含清单自身。

## 能证明什么，不能证明什么

代码验证声明语言中的模型关系、反例和路线分类。它不验证事实背景确实为真，不从原文自动抽取项位，不裁定希腊文异读，也不验证古代“明显为真”的认识论要求。背景可满足比真实可靠更弱。一般性的归谬原理及类型压缩理由仍需正文中的证明，不能由这次小实验代替。
