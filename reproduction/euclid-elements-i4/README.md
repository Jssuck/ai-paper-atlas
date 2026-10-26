# 《几何原本》I.4：精确有理 SAS 教学复现

这是**原创的现代坐标教学模型**：把有标号三角形放在现代实数内积平面中，以有理坐标进行精确计算，检查 SAS 数据，构造并独立验证一个等距仿射映射。无第三方依赖，不调用现成 SAS 定理。

**不是**古代“叠合”操作的物理复演、欧几里得原公设系统中的完整形式推导或证明助理复现。有限样本成功不能证明所有有理数或所有实数情形。下述一般矩阵推导是现代数学解释，不应把它与测试次数混为一谈。

## 一分钟运行

使用 Python **3.10 或以上**（本次实际环境：CPython 3.12.14、Linux x86_64）。把工作目录切换至本文件所在目录，再运行：

```bash
python3 -B run_all.py
```

无需安装任何包。脚本真实运行下列命令、记录标准输出/标准错误与退出码，重建结果 JSON、Notebook 输出和校验和：

```bash
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B enumerate_cases.py
python3 -B -O enumerate_cases.py
python3 -B -OO enumerate_cases.py
python3 -B build_notebook.py
python3 -B execute_notebook.py
```

`-O/-OO` 不是证明强度的升级；它们用于确认执行不依赖会被优化删除的 `assert`。关键运行检查使用显式 `if ...: raise ...`，回归测试使用 `unittest`。

## 输入、接口和语义

```python
from fractions import Fraction as F
from euclid_i4 import Triangle, Certificate, compare_sas, verify_certificate

abc = Triangle((0, 0), (3, 0), (0, 2))
known = Certificate(((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5))),
                    (F(7, 3), F(-5, 2)))
def_ = Triangle(*(known.apply(p) for p in abc.vertices))
result = compare_sas(abc, def_, require_direct=True)
print(result.certificate.q, result.certificate.t)
print(verify_certificate(abc, def_, result.certificate))
```

- `Triangle(a,b,c)`：三个**有序**点。也可给 `compare_sas` 传入含三个点的 list/tuple。对应关系固定为 A↔D、B↔E、C↔F，不自动重排顶点。
- 每个点必须为恰有两个坐标的 list/tuple；坐标只接受内置 `int`（不含 `bool`）或 `Fraction`，统一规范为 `Fraction`。
- 拒绝所有 `float`（包括有限数、NaN、±Infinity）、字符串、Decimal、复数、错误维度等；共线/重复顶点同样抛出 `InputError`。不能把无效输入误读为“合法但不满足 SAS”。
- 推荐 `F(1,10)`，不要先经过 `0.1`；若调用者自己传入 `F(0.1)`，已经得到精确的二进制浮点对应有理数，接口无法追溯其来源。
- `compare_sas(..., require_direct=False)` 返回 `SASResult`。`sas_equal` 按“第一边平方、第二边平方、夹角内积”的顺序记录三个布尔值。
- `congruent` 表示**在给定标号对应下、允许反射**的全等；`orientation_preserving` 表示已验证的 Q 是否满足 det Q=+1；`accepted` 还遵守可选的保向策略。镜像可以 `congruent=True` 而 `accepted=False`，原因是 `reflection_excluded`。
- 不满足 SAS 时返回 `reason='sas_mismatch'`，没有证书；独立核查异常时抛出 `VerificationError`，而不是隐去问题继续成功。
- `Certificate(q,t)` 表示候选仿射映射，构造函数**只验证数据格式**，不会把任意候选当成等距映射。`verify_certificate` 才进行具体检查。

## 算法：不是循环援引 SAS

令

```text
u = B-A, v = C-A, U = E-D, V = F-D
P = [u v], R = [U V]
```

1. 拒绝 det P=0 或 det R=0 的退化三角形。
2. 精确检查 `u·u=U·U`、`v·v=V·V`、`u·v=U·V`。前两项相等且边非零时，第三项在现代实数内积模型中等价于普通夹角相等；**代码没有独立计算或校验任意角函数**，也没有把数值角度的近似值当输入。
3. 用 2×2 逆矩阵显式公式计算 `Q = R P⁻¹`，再令 `t = D - QA`。
4. 独立检查 `QᵀQ=I`、`QA+t=D`、`QB+t=E`、`QC+t=F`，并要求 det Q=±1。
5. 直接从坐标检查 `BC²=EF²`、全部对应边平方，以及各顶点的 `(相邻边平方, 内积, 另一相邻边平方)`。最后这些数据相等支持对应内角相等的现代解释，而不是独立的角函数测试。

一般代数理由：第二步正是 `RᵀR=PᵀP`，因此

```text
QᵀQ = P⁻ᵀ RᵀR P⁻¹ = P⁻ᵀ PᵀP P⁻¹ = I.
```

三点映射由构造成立，第三边也满足 `|v-u|²=|V-U|²`。这里使用线性代数和实数内积知识，不以“这两个三角形由 SAS 全等”作为验证子程序。程序既不是从欧几里得原始公设推导这些代数基础，也没有证明 Python/Fraction 实现无错误。

det Q=−1 是**反向等距仿射映射**；总体可能包含平移，不宜把每个这样的映射都描述成关于一条固定直线的纯反射。它与 det Q=+1 的保向运动明确区分。三点非共线确保映射唯一，因此不能为同一标号镜像另外选择一个保向映射。

## 实际结果

`logs/` 保存真实子进程输出；`results/environment.json` 保存不含账户/私有路径的环境信息；`results/verification.json` 汇总各退出码与三模式结果哈希。

| 检查 | 实测结果 |
|---|---:|
| unittest 方法，普通 / `-O` / `-OO` | 每种 28 项通过 |
| 向量集合 `[-2,2]²` | 25 个向量 |
| 首顶点为原点的有序向量对 | 625 |
| 退化输入拒绝 | 129 |
| 非退化有标号三角形 | 496 |
| 全部有序三角形配对，逐一调用 API | 246,016 |
| SAS 通过、证书各项验证通过 | 4,096 |
| 其中 det Q=+1 / det Q=−1 | 2,048 / 2,048 |
| 不满足 SAS 而拒绝 | 241,920 |
| 另加有理旋转/反向变换＋非零有理平移 | 992 项，全部精确回收 Q,t |

枚举在普通、`-O`、`-OO` 三模式均实际执行；生成的 `results/enumeration.json` 字节级 SHA-256 一致。上表的 246,016 不是全空间证明，也不意味着这些都是不同的几何形状；包含有序自配对和标号相关的重复。

## 必须保留的负例

1. **退化**：重复点、斜共线、竖直共线、有理坐标共线均拒绝。
2. **错对应**：`(0,0),(3,0),(0,2)` 交换第二、第三目标点，给定标号的两边平方不相等，拒绝。对称三角形交换这两点仍可能全等，测试另有合法反射例，不能把所有换序一概称错。
3. **剪切**：源三角形 `(0,0),(1,0),(-1/2,1)` 经 `Q=[[1,1],[0,1]]` 变为 `(0,0),(1,0),(1/2,1)`。两已知边平方都保持为 `1,5/4`，夹角内积却从 `-1/2` 变为 `1/2`；虽然 det Q=1 且三点映射成立，`QᵀQ≠I`，必须拒绝。
4. **非夹角 SSA**：`A=D=(0,0), B=E=(4,0), C=(1,1), F=(3,3)`。`AB²=DE²=16`、`BC²=EF²=10`；AC、DF 同向同射线，故首顶点角相等，但这不是两条给定边的夹角。`AC²=2`、`DF²=18`，所以不全等。无需用反三角函数判定“同射线”。
5. **错误证书**：错误平移虽有正交 Q 仍不能映射三点；剪切虽能映射三点仍不正交。独立检查器确实拒绝这两种情况。

## Notebook 的真实执行边界

`euclid_i4_tutorial.ipynb` 为 nbformat 4.4 文件，含 7 个 Python 代码单元。当前环境未安装 `jupyter`、`nbformat`、`nbclient` 或 `ipykernel`，没有新增第三方安装。保存输出由 `execute_notebook.py` 在共享命名空间中按顺序 `compile`/`exec` **真实执行**产生，详见 `logs/notebook-stdlib.log`。这不是 Jupyter 内核执行，也不是完整 nbformat schema 验证或内核兼容性认证。已有 Jupyter 的读者可自行打开并“Restart and Run All”。

已读取 Notebook 技能说明，但技能的附带模板和生成器在本环境不可读取、本地也不存在。故采用随附 `build_notebook.py` 的标准库回退生成，未声称使用不可用的模板。

## 文件索引

- `euclid_i4.py`：精确输入、SAS 比较、矩阵构造、独立证书检查。
- `test_euclid_i4.py`：28 项回归测试，含子用例。
- `enumerate_cases.py`：完整有限网格配对及有理变换实验。
- `results/enumeration.json`：统计、精确矩阵/平移、SSA/剪切等示例；有理数用字符串保存，不转换为 float。
- `build_notebook.py`、`execute_notebook.py`、`euclid_i4_tutorial.ipynb`：Notebook 构建、真实标准库执行及已保存输出。
- `run_all.py`、`logs/`、`results/environment.json`、`results/verification.json`：复跑命令、实跑证据与环境。
- `SHA256SUMS.txt`：本实现交付文件的内容校验和（不包括该清单本身、缓存与另行负责的 `independent-review/` 审稿材料；审稿证据由其独立流程绑定）。
