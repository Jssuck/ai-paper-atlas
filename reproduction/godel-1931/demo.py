"""Run: python demo.py. All examples are bounded, illustrative, and TOY."""

from godel_toy import (
    Add, Eq, Nat, Var, ProofStep, bounded_search, check_proof,
    component, concatenate, decode, encode, encode_proof, evaluate,
    formula_code, formula_tokens, proof_relation, substitute_numeral,
)


def main():
    print("TOY 教学实验；不是 Gödel 原系统，不是对不完备性定理的计算证明。")
    print("\n1. 素数幂序列编码：指数 a_i + 1")
    seq = (0, 2, 1)
    code = encode(seq)
    print(f"encode{seq} = {code} = 2^1 * 3^3 * 5^2")
    print(f"decode({code}) = {decode(code)}")
    print(f"component({code}, 1) = {component(code, 1)} （从 0 编号）")
    print(f"空序列编码 = {encode(())}；单元素 [0] 编码 = {encode((0,))}")
    joined = concatenate(encode((0, 2)), encode((1,)))
    print(f"拼接 [0, 2] 和 [1]：编码 {joined}，解码 {decode(joined)}")
    try:
        decode(10)
    except ValueError as exc:
        print(f"拒绝 10 = 2*5：缺少位置对应的素数 3（{exc}）")

    print("\n2. 无量词 AST：把 x 的自由出现替换成数字项 2")
    original = Eq(Add(Var("x"), Nat(1)), Nat(3))
    replaced = substitute_numeral(original, "x", 2)
    print(f"原式 x+1=3；前缀 tokens = {formula_tokens(original)}")
    print(f"替换后 2+1=3；tokens = {formula_tokens(replaced)}")
    print(f"原式 toy code = {formula_code(original)}")
    print(f"替换后 toy code = {formula_code(replaced)}")
    print(f"在自然数解释下求值：{evaluate(replaced)}；求值不等于形式证明。")

    print("\n3. 独立的有限证明系统：公理 A；规则 A→B、B→C、C→D")
    valid = (ProofStep(0, 0, 0), ProofStep(1, 1, 1), ProofStep(2, 2, 2))
    invalid = (ProofStep(0, 0, 0), ProofStep(2, 2, 1))
    p = encode_proof(valid)
    print(f"有效证明 [A, B, C] 的编码 p = {p}")
    print(f"Proof(p, C的代码2) = {proof_relation(p, 2)}")
    print(f"同一证明是否以 B 结束：{proof_relation(p, 1)}")
    print(f"无效跳步 [A, C]：{check_proof(invalid, 2)}")
    for bound in (2, 3):
        result = bounded_search(2, bound)
        print(f"至多 {bound} 行：找到 C 的证明 = {result.proof is not None}；"
              f"检查 {result.candidates_checked} 个有效证明前缀")
    print("2 行内未找到，不推出 C 不可证明；3 行时已找到。")
    print("本实验没有量词、自指、可表示性证明、ω-一致性论证或不完备性定理实现。")


if __name__ == "__main__":
    main()
