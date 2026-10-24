# 《后分析篇》I.12 独立技术审查

## 范围与结论

审查对象为正文的现代教学重构、原创 Python 实现、测试和保存的有限枚举结果；原文版本与章界的核验另见[来源台账](aristotle-posterior-analytics-i12.sources.zh-CN.md)。技术审查独立于代码编写，重新执行了测试，并以不同表示方式复核关键结果。

**结论：下列最终字节通过本次技术核验。** 不把有限枚举当作任意论域定理的证明，不把显式域标签或意义 ID 当作真实科学知识的认证。本结论不替代发布后的链接、正文公式显示及远端内容验证。

## 发现与修正核验

1. 初稿将 512 图写成无自环图，已改正为三节点允许自环有向图：9 个可能有向边各自选取，故为 2⁹＝512；无自环时应为 2⁶＝64。
2. 原先把独立可达性 oracle 称为 BFS，而实现使用列表尾部弹出，即栈式遍历。正文与附件已改成可达性搜索／栈式搜索，不再错误命名；可达性结果不受该术语订正影响。

## 实际复跑

在附件目录独立执行：

```sh
python3 -m unittest -v test_model.py
python3 -O -m unittest -v test_model.py
python3 -OO -m unittest -v test_model.py
python3 model.py
python3 -O model.py
python3 -OO model.py
sha256sum -c SHA256SUMS
```

三个测试模式均实际通过 19 项，三次枚举 JSON 与已保存 `results.json` 完全相同，校验清单所列文件全部通过。测试使用 unittest 的显式检查方法，未依赖优化后消失的裸 assert。

## 独立重构核验

- 未调用作者的位掩码包含函数来重数反模型，而将三元素论域的 8 个子集构造成 Python 集合，以集合包含逐一检查 512 三元组和 64 集合对。重新得到共享属性前提 125、包含误推反模型 61、双非空反模型 42；反向包含误推 19、双非空 12；有效链反模型 0。
- 对所有 512 张允许自环图，用关系合成反复扩展到不动点，作为区别于作者矩阵式闭包与逐起点栈式搜索的第三种检查方式；与 `closure` 差异 0。自反关系在初始状态显式加入，与接口承诺相符。
- 阅读包含链和双向包含相等的逐元素证明。正文用有限路径归纳说明传递路径的可靠性；没有把 512 图通过说成一般正确性的全部根据。
- 非空的共同属性反例确实满足两前提而否定目标包含；反向推理例子没有把集合包含、材料蕴含和古代原因解释直接等同。
- `same_middle` 仅比较外部意义 ID，`question_route` 仅消费领域、角色与有向桥声明。正文及附件明确不保证这些声明的正确性，也不把专家身份当作前提真值。
- 输入允许空集，但关键无效论式另计双非空反例，避免依赖存在预设争议。程序未建立火的经验模型，未测量增长规律，未复现完整古代科学理论。

## 绑定的最终文件

SHA-256 仅绑定以下文件字节；任何相关内容或格式变化须重新核验。审查文件不纳入自身散列，避免循环依赖。

| 文件（仓库相对路径） | SHA-256 |
| --- | --- |
| `papers/ancient/aristotle-posterior-analytics-i12.zh-CN.md` | `5c73a9dd54e1690e775570e8c6df0ff7f7946dfcac394f08503cfd887003a54e` |
| `reproduction/aristotle-posterior-analytics-i12/model.py` | `633bf87a5c994febac50bbfe06208a2384e928ecf504df1b31fe87b3d8844ffc` |
| `reproduction/aristotle-posterior-analytics-i12/test_model.py` | `820d8ed2ef75cf7f345e04363460fa1ef5ca4ae92d721b4eefb36e480c767c2e` |
| `reproduction/aristotle-posterior-analytics-i12/run.sh` | `03fa7bb4a11c075a0d4ad93de25335036773adb3e9ee20fe11107b8878ebec59` |
| `reproduction/aristotle-posterior-analytics-i12/README.md` | `471c099fade89bbb5e1750958873124141daf6f07c64fe7d3ad0590153372297` |
| `reproduction/aristotle-posterior-analytics-i12/SHA256SUMS` | `b78b8bdcab5211bc6a1b9a547d4bae1f5fb982e10f7beb8450bbc2ec1d0b3a4a` |
| `reproduction/aristotle-posterior-analytics-i12/results.json` | `c219f5679a9b10f4c5e41689678e68150b81c080f0a72d774addd819797a3389` |
