"""Seal the reread final source and actual outputs without self-hash cycles."""
from hashlib import sha256
from pathlib import Path
import json
BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'independent-review'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition: raise RuntimeError(message)


def main():
    matrix = json.loads((OUT / 'matrix-results.json').read_text())
    author = json.loads((BASE / 'evidence/summary.json').read_text())
    oracle = json.loads((OUT / 'normal-oracle.json').read_text())
    require(matrix['status'] == 'PASS' and matrix['source_unchanged_during_run']
            and matrix['equal_semantic_outputs_across_modes'], 'review matrix is not stable PASS')
    require(author['passed'] and author['source_files_unchanged_during_run']
            and author['deterministic_stdout_across_modes'], 'author verification is not stable PASS')
    for name, expected in matrix['source_sha256'].items():
        require(digest(BASE / name) == expected, 'source changed after review: ' + name)
    for name, expected in author['files_sha256_after'].items():
        require(digest(BASE / name) == expected, 'source changed after author verification: ' + name)
    excluded = {'independent-review/review.zh-CN.md', 'independent-review/review-manifest.json'}
    files = {}
    for path in sorted(BASE.rglob('*')):
        name = str(path.relative_to(BASE))
        if path.is_file() and '__pycache__' not in path.parts and name not in excluded:
            data = path.read_bytes()
            files[name] = {'bytes': len(data), 'sha256': sha256(data).hexdigest()}
    manifest = {'status': 'PASS', 'hash_algorithm': 'SHA-256',
                'scope': 'final source, tests, documentation, independent audit scripts and actual command outputs',
                'excluded_to_avoid_self_hash_cycles': sorted(excluded), 'files': files}
    mp = OUT / 'review-manifest.json'
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    c = oracle['counts']
    report = f'''# 独立代码审查：资料充分性教学模型

## 结论与对象

**PASS（下述有限范围内，无未解决的阻断问题）。** 本报告绑定最终实现、测试、中文说明和真实运行输出。首次审查发现的一个故障探针类型别名问题已修正。曾发生临时存储中断；恢复后重新读取文件并真实重跑全部命令，旧日志和旧摘要不作为本次最终证据。独立审核脚本为恢复后版本，不声称其字节与中断前相同。

历史锚点为孔狄亚克《逻辑》第二部第八章，1780年著作、此次所据1798年印本实际页170–176。可能世界、查询、编码纤维、最坏成本观测树和结构方程全是现代教学增补。本代码审查不替代原件校勘，不把程序称为历史算法复刻，也不声称验证或证伪人的能力起源理论。

## 实际检查与独立性

阅读核心、例子、演示、全部作者测试、行为故障探针、演练执行器、验证器和README／MODEL／WALKTHROUGH／VERIFICATION；改变及恢复的内容在最终封存前复读。预期答案不来自导入作者测试或调用被测最优递推。

[矩阵结果](matrix-results.json)保存普通、`-O`、`-OO`三模式的{len(matrix['commands'])}条真实命令、退出码及日志；全部退出0。每模式运行{author['unit_test_count_per_mode']}个作者单元测试、13项行为故障探针、8个中文演练Python块、独立oracle及两类验证工具健康检查。源码／文档运行中未变；确定性输出一致。oracle仅移除必然不同的optimization元数据后比较。

每模式独立检查数量：

- {c['analysis_cases']}个答案状态；{c['fiber_cases']}个编码纤维；{c['rewrite_and_evidence_cases']}组改写与资料合取。
- {c['exhaustive_binary_two_question_cases']}个完整枚举案例：1至4个有序世界、全部二值目标与两道有序二值问题，使用完整候选域。
- {c['seeded_multivalued_three_question_cases']}个固定种子17801798的多值、三问题、不同候选子集案例；另有空域、三比特选择器、四比特奇偶性深度4及因果例子。
- {c['independent_world_traversals']}次独立逐世界遍历，核对分支、叶值、问题不重复及实际最坏路径，并与follow_tree对照。
- {c['negative_contract_cases']}项拒绝检查，包含输入边界、非唯一答案读取、失败解码和域外编码；并非这么多种不同输入类型。
- {c['causal_mechanism_cases']}项结构方程结果以及新增干预问题的可识别性。

**独立策略oracle。** `audit_code.py`把完整策略表示为平坦的满r叉树问题索引数组，枚举小于“依次问完所有问题”上界的策略高度，把世界独立送到叶子并检查叶内目标恒定；不使用模型的递归最优值作为预期结果。相同联合回应、不同目标的不可解见证另行核对。另一份论证审计使用不同的位掩码／逐层树存在性oracle，其输出保存在上级evidence；作者测试次数不被冒充为独立证明。

## 语义与实现一致性

1. 空候选为inconsistent；非空且目标恒定才是identified。多世界共享一个答案可以充分，不能误成必须唯一世界。
2. 条件合取；新增资料只缩小或保持候选域。保世界比保当前答案强；改写链逐步核对，不能只看端点。空集等价另有nonvacuous标志，不能视作解题成功。
3. 编码充分性相对于当前候选域的纤维。失败返回真正冲突的候选世界对；成功解码只覆盖实际出现的编码。空域空真不产生答案。已知目标表是建模语义，不能解释为目标已免费取得。
4. 观测表为确定、无噪声、单位成本。最坏深度、分支候选、最早同价首问、实际遍历和不可解见证均核对。impossible仅相对于给定问题表。
5. M1（S:=U，A:=S）与M2（A:=U，S:=A）自然观测同为(0,0)、(1,1)。固定U=0并替换S方程为1后，分别为(1,1)、(1,0)。新增干预使模型一问可辨；这是新增观测能力，不是等义改写凭空增加信息。
6. 精确类型检查拒绝bool/int、float/int和自定义子类别名；覆盖递归元组、回放下标、约束真假表和因果输入。回调一次物化后不再执行；校验在优化模式仍生效。

## 已修正问题及验证工具健康检查

旧版 `strict_equal({{True: 'x'}}, {{1: 'x'}})`因普通字典键列表比较而误判相同。现在使用递归、类型严格的键元组比较。作者回归加上本审查的直接／嵌套／元组键案例均通过；也检查嵌套值、survived、killed、baseline_error、invalid_baseline和mutant_error。异常不算击杀。

13项是带明确见证的行为替代探针，**不是自动源代码变异覆盖率**；不能从全部击杀推出整体程序正确。

对verify.py，除了阅读三条失败保护，还在临时隔离副本真实执行四组夹具：正常、子进程退出7、跨模式输出不同、执行中修改静态文档。每组执行15个真实子进程；正常返回0，其余均返回1并记录对应原因。三种审查模式各重复这四组。参见[夹具结果](normal-verifier-sanity.json)及[故障分类器结果](normal-mutation-sanity.json)。夹具验证编排器，不替代完整模型测试；原始实现未被夹具修改。

## 限制

- 有限测试不是无限世界、无限问题或任意Python程序的一般证明。
- 手造Analysis／Compression／DecisionNode不是经校验的输入协议；follow_tree仅回放匹配的原问题、问题序列及生成树。回调纯度、现实假设、观测可信度和自然语言编码忠实性由建模者负责。
- 筹码默认各坐标0至10；上界6的失败显示有限域排除真解，不能证明原方程无解。
- 实测环境为CPython {oracle['python']}；目标语法为Python 3.10+，没有逐版本实测。
- 穷举可能昂贵；不承诺大规模效率，不含心理学验证、现实干预可行性或时间／风险成本模型。

## 精确版本绑定与复跑

[SHA-256清单](review-manifest.json)绑定{len(files)}个文件，包含最终实现、测试、说明、作者证据与本审查真实日志及JSON。清单SHA-256：

`{digest(mp)}`

清单排除自身及本报告，避免自哈希循环；本报告用上述摘要绑定清单。文件或日志改变后必须重新审阅、运行和封存，不能沿用旧摘要。

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent-review/run_review.py
PYTHONDONTWRITEBYTECODE=1 python3 independent-review/seal_review.py
```

最后一步仅在审查者复读改变内容后使用；它检查快照，没有自动替代语义审查。
'''
    rp = OUT / 'review.zh-CN.md'; rp.write_text(report, encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'bound_files': len(files), 'manifest_sha256': digest(mp),
                      'review_sha256': digest(rp)}, indent=2))


if __name__ == '__main__': main()
