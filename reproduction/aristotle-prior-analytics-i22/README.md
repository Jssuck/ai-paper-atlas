# I.22 教学复现：必要性标签与实际见证的范围

本目录是自有教学代码；`Model` 核心与有限维度枚举器复用仓库 I.21 的自有标准库实现，I.22 的十二配置、十八测试、七类检查及日志重新编写和执行。没有复制古代原印页图或全文译文，不声称复原唯一古代模态语义。

## 1. 环境、文件和复跑

实际环境 Python 3.12.14，标准库；详见[环境与命令记录](environment.json)。在本目录执行：

```sh
python -m unittest -v test_model.py
python enumerate_models.py
python -O -m unittest -v test_model.py
python -O enumerate_models.py
python -OO -m unittest -v test_model.py
python -OO enumerate_models.py
```

[模型](model.py)、[单测](test_model.py)、[枚举器](enumerate_models.py)。单测使用 unittest，枚举用显式异常，因此优化模式不会关闭检查。未创建 Notebook，不声称 Jupyter 内核运行。

## 2. 精确语义

非空有限对象域U，非空有序情形序列W，第0个为实际情形。每情形存(A,B,C)三个位掩码；位i为1表示对象i属于该项。对象身份跨情形保持，外延可变。

`holds(mode, quantity, predicate, subject)`：谓项在前、主项在后。a/e/i/o为全称肯定、全称否定、特称肯定、特称否定。

- D：在实际主项Y0内判断实际谓项X0。
- N：仍以实际主项Y0为量化范围，逐对象要求所有情形满足X或非X。
- P：仍量化Y0，每对象要求存在情形满足X或非X；不同对象可使用不同情形。
- C：Y0中对象对X既有属于情形也有不属于情形；a和e等值，i和o等值。此C标签与第三项名C分属参数位置。
- BOX：在每个情形重新取Y(w)，按该情形X(w)评价对应直言句，再对所有情形取合取。它不是N的另一种拼法。

空实际主项使全称真、特称假。模型不把此政策认作古代唯一存在理论。拒绝布尔值伪装整数、负/越界位掩码、空世界序列、非法项、量词或模式。有效维度不设人为上限，但枚举指数增长，不应任意扩大实验。

## 3. 一般论证和有限核验分开

记V(A)为在某情形属于A且在另一情形不属于A的对象集合。安全桥：C0非空、C0包含于V(A)、C0包含于所有B(w)时，任选同一个c属于C0；它既属于B0又属于V(A)，故C_i(A,B)。若必要前提为特称，先取其C0中见证；若偶然前提为特称，先取其见证再用全称必要包含。此任意见证论证适用于所有满足定义的模型，不依赖有限枚举。

相反，N_a(A,C)和C_a(B,C)并不保证任何实际B属于C0，故不能无条件搬动见证。N_e(A,C)同样不能自动保证D_o(A,B)。如果另加B0交C0非空，本模型反而分别得到N_i(A,B)或N_o(A,B)：选交集中对象并沿N定义直接继承。这揭示模型与原典关于结论强度的分类有边界，不能冒称全章被现代模型验证。

BOX_e(A,C)按逐情形集合互斥对称，故可换位；N_e(A,C)固定C0，其换位会改成A0，未必成立。BOX必要否定可在一个显式配置中与实际但非N必要的特称否定共存；这个例子展示语义差别，不证明BOX解释全部历史路线。

## 4. 十二个显式配置

位掩码1={0}，2={1}，3={0,1}，4={2}，5={0,2}，6={1,2}，7={0,1,2}。除empty_middle外，表中所有项在所有情形都非空。

|配置|对象数；两情形(A,B,C)|核查用途|
|---|---|---|
|safe_contingent_not_actual|2；(2,1,1),(3,1,1)|C_a(A,C)、N_a(B,C)、C_i(A,B)真；D_i、N_i、N_o(A,B)假|
|necessary_major_missing_actual_witness|2；(1,2,1),(1,3,1)|N_a(A,C)、C_a(B,C)真，但P_i(A,B)假|
|necessary_negative_missing_actual_witness|2；(2,2,1),(2,3,1)|N_e(A,C)、C_a(B,C)真，但D_o和P_o(A,B)假|
|box_negative_actual_not_necessary|3；(2,1,1),(3,2,4)|BOX_e(A,C)、C_a(B,C)、D_o和P_o(A,B)真；N_e(A,C)、N_o(A,B)假|
|sleeping_horse|3；(6,2,1),(7,2,1)|C_a(A,C)、N_e(B,C)、N_a(A,B)真，P_o(A,B)假|
|waking_horse|3；(4,2,1),(5,2,1)|同前两前提真，N_e(A,B)真而P_i(A,B)假|
|different_particular_witnesses|2；(1,1,3),(3,1,3)|N_i(B,C)见证0，C_i(A,C)见证1，C_i(A,B)假|
|weak_not_strong|2；(2,3,1),(2,3,1)|P_o(A,C)真而C_o(A,C)假|
|empty_middle|1；(1,1,0),(1,1,0)|两全称前提可空真，C_i(A,C)与C_i(A,B)皆假|
|anchored_negative_not_convertible|2；(2,1,1),(2,1,3)|N_e(A,C)真而N_e(C,A)假|
|necessary_positive_intersection|2；(1,3,1),(1,2,1)|N_a(A,C)及实际B/C交集非空，N_i(A,B)真|
|necessary_negative_intersection|2；(2,3,1),(2,2,1)|N_e(A,C)及同一交集，N_o(A,B)真|

睡/醒马是借用原典术语位置的自有数字模型，非关于真实动物或古代本体论的实验。全称前提蕴含特称需要非空，因此这对非空例也能检查改成特称偶然前提的失败方向。

## 5. 真实结果

正常、-O、-OO三模式各18项单元测试通过，各枚举4744配置，维度(n,情形数)=(1,1),(1,2),(1,3),(2,1),(2,2)，计数8+64+512+64+4096。七类检查分别是三个安全桥、两个交集桥、偶然否定改写及BOX必要否定换位。前提满足计数依次为300、396、332、336、336、4744、4744，均无反例。三模式JSON结果相同。

- 正常：[单测日志](logs/normal-tests.txt)、[枚举日志](logs/normal-models.txt)、[JSON](logs/normal-results.json)
- -O：[单测日志](logs/O-tests.txt)、[枚举日志](logs/O-models.txt)、[JSON](logs/O-results.json)
- -OO：[单测日志](logs/OO-tests.txt)、[枚举日志](logs/OO-models.txt)、[JSON](logs/OO-results.json)
- [作者文件SHA256绑定](author-manifest.json)

这些是有限实现回归检查，不是一般数学定理的实验证明，不覆盖全部模型规模，不认证任何古代唯一语义。只对I.22相关问题作最小教学复现，不计I.23或全书完成。
