# I.28 教学代码独立核验

核验日期：2026-10-22。审查者与代码作者为不同执行代理；不是人类专家认证、证明助理认证或安全认证。范围限本目录的六类中项配对教学实现，不认证古代全文解释或任意三段论完备性。

## 结论与修订闭环

最终受检版本通过以下有限核验。初审发现两个接口需修订项，由作者修复并重新执行；另有一项独审链接误报被整包检查纠正，以下如实保留：

1. 原 `search` 对相同主谓端项可能产生随后被 `verify` 拒绝的证书。现在入口显式拒绝相同端项，且中项必须异于两端。
2. 原项名没有严格类型与空值限制。现在要求非空、非纯空白字符串；非法类型在接口明确抛出 `ValueError`，而不是到排序时偶发失败。
3. 独审曾误判复现 README 到论文的相对链接少一级，并建议改为 `../../../papers/...`。整包链接检查指出此建议会越过仓库根：README 位于 `reproduction/aristotle-prior-analytics-i28/`，原 `../../papers/ancient/aristotle-prior-analytics-i28.zh-CN.md` 才正确。已恢复原正确路径；这是审查者误报，不是作者原实现错误。README 哈希与独立运行记录已在恢复后刷新。

作者新增回归测试后，普通、`-O`、`-I` 模式均为29测试通过。审查者另用隔离进程重跑作者完整29测试，退出0；真实输出见[作者测试复跑 stderr](independent-review/author-tests.stderr.txt)及[stdout](independent-review/author-tests.stdout.txt)。

## 独立方法与实际结果

[check.py](independent-review/check.py)自行使用位掩码定义集合包含、交集及差集，不调用作者的 `true_fact`、`facts_from_model` 或 `requirements` 来决定预期结果；仅调用作者搜索及证书核验接口接受挑战。这样避免作者语义辅助函数与预期结果共同出错时自证通过。

普通、优化、隔离三模式分别真实运行，结果完全一致：

- 论域大小0至4的4681个三集合赋值，生成并核验2123份证书。CF/DF/BH各341，CG/DG各440，BG为220。
- 每份证书挑战5种篡改：未知规则、中项更换、合并端项、缺前提列表、伪造结论。共10615次拒绝。
- 从每份证书的知识库中逐一删去必需前提，共5346次拒绝。
- 独立搜索12组非空反模型，分别否定BF、CH、DH对既定A谓述E方向四型结论的保证；同时检查CH仍支持逆向特否，未误写成全无两端关系。
- 13个非法输入案例被明确拒绝，含相同端项及空、空白、None、数值、列表、字典项名。
- 专查BG不能以M非空替代A非空；45a的B/G排斥反例支持特否但不支持B/H，未将有疑点桥接写成有效规则。

日志：[普通结果](independent-review/normal.stdout.json)、[普通 stderr](independent-review/normal.stderr.txt)、[优化结果](independent-review/optimized.stdout.json)、[优化 stderr](independent-review/optimized.stderr.txt)、[隔离结果](independent-review/isolated.stdout.json)、[隔离 stderr](independent-review/isolated.stderr.txt)。三份stderr均为空，退出码均0。运行器[run.py](independent-review/run.py)保存命令、环境和哈希到[checked-sha256.json](independent-review/checked-sha256.json)。解释器命令路径标准化为python3，真实stdout/stderr未修改。

作者[evidence.json](evidence.json)的四个源码哈希已逐项与当前文件比对相等；作者demo计数、三份测试日志与其README陈述一致。

## 规则与边界检查

六索引方向与正文一致；`none`仅将有显式证据的全称排斥对称规范化，不把缺项视为否定。CG/DG依赖中项非空，BG依赖A非空。全称规则无需存在条件。证书存储规则名、两端、中项、规范化前提及结论，验证器重建前提，不信任证书自报的结论。

`nonempty`是输入前提，不是程序自行找到的现实对象见证；`verify`保证该规则实例相对输入前提的形式正确，不保证经验前提真实、不保证库一致、完整或已闭包。接口将不同名称视为不同项，不合并同延或同义词；只搜索显式六模式，不推导全部可能的闭包。无候选不是目标为假。

论域0的枚举是现代实现额外空域压力测试；正文采用非空论域，不因程序也测空域就把历史模型改为空域理论。有限枚举与攻击样例不能证明任意规模实现完备或安全，也不能代替正文任意对象的一般推导。

## 最终受检源码 SHA-256

|文件|SHA-256|
|---|---|
|model.py|`9f2f31c82d8ca363cf652d1e5ab9cf3fa0b6a91ce80e1ac8203f44425c3a25e1`|
|test_model.py|`7d0d29027d145059af8054a2b46a1568e1518589b23b6c0919eba4bd54875e01`|
|run_demo.py|`f9b31ae8abae33958c29705f7955bd6bc49cbf9827069c8e442a4d68ecf85980`|
|run_evidence.py|`60d4f5b292f8ee8fbef36982e21367f83d481ebbc59d308af5a144551b880a1b`|

README及独立核验脚本的哈希另列在checked-sha256.json。任何代码变化都需重新执行并更新绑定；这份记录不认证未经重跑的后续版本。
