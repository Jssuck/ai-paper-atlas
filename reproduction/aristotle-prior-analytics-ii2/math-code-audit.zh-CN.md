# II.2 独立数学与代码核验

结论：**通过**。核验对象是本章原创教学形式化和实现，不是古代文本全部语义，也不是现代 AI 实验。

## 1. 数学审查

- 逐项复核正文四式 P/R/Q 的方向、逐对象保真证明和逆否推理；没有把固定模型中的物质蕴涵误认作有效性。
- 第 7 节 10 个全称案例逐项复算：结论均真，前提的全假／部分假／真标签正确。第 8 节两见证例子及 4 行双式构造成立；存在句的不同见证没有被混用为有效推导链。
- 空主项的全称句空真，不会误归全假。大前提全假、真全称小前提推出假全称结论的限制明确要求 C 非空；去掉条件的空 C 反例正确。
- 16 道练习的数学答案与正文一致；全假／部分假均属二值 F，不引入第三真值。
- 八类型压缩保留本语言的见证／违例存在性、空项和混合分类，不保留重数、关系或因果。该一般证明和有限运行证据分开陈述。

## 2. 独立运行与交叉核验

审查者重新运行 `python3 -m unittest -v`、`python3 -O -m unittest -v` 和 `python3 -OO -m unittest -v`：每模式 21 项测试均通过。另运行 `python3 review_oracle.py`；全部终态和命令见 [独立实跑日志](logs/independent-review.txt)。没有安装依赖。

[独立 oracle](review_oracle.py) 不调用被测谓词取得期望值：它按每个对象的三位隶属表，使用逐对象全称／存在量词计算 A/E/I/O。穷举域大小 1–4 的 **4680 个有标号模型**，核对 **168480 项谓词与分类**，并核对同数的压缩前后真值／分类，以及 **18720 次四式评价**。未发现差异或 TTF。这个有标号模型计数与主实验的类型子集计数是两种枚举，不能相加称独立语义情形数。

主实验三份优化模式 JSON 已逐字比对一致。255 个非空类型子集以及 228 个 B/C 非空子集计数正确（后者是前者子集）；每模式分别 1020 和 912 次式评价。12 个具名例子均有真结论。README 的 228 模型真假签名表与日志逐项相符。运行检查使用显式异常或 unittest 断言方法，不依赖优化模式会删除的裸 `assert`。

这些运行不是对一般定理或因果知识正确性的独立经验“证明”。独立 oracle 覆盖重复类型和多对象域，用于发现方向、空项、分类和压缩实现错误；一般性仍来自正文数学论证。

## 3. 最终内容绑定（SHA-256）

以下散列绑定本次实际审查的正文、仓库索引、实现、说明与真实证据；任一改变须重新确认对应审查结论。审查文件本身不自引用散列。

| 文件（仓库相对路径） | SHA-256 |
|---|---|
| `papers/ancient/aristotle-prior-analytics-ii2.zh-CN.md` | `90297be485ce2ae20482e42b0692c0bc4b12685994c7ffd17670ceb575ba53d5` |
| `README.md` | `cfb9bec33153f69de6fd992e3df193214bf2e928277b07e0f389be8134d0bfea` |
| `reproduction/aristotle-prior-analytics-ii2/README.md` | `11ece00a6cf2780f31f691ca8cf67de76b27458ad5e393d9a2810cb32f97a7e6` |
| `reproduction/aristotle-prior-analytics-ii2/model.py` | `c509c26dab7966703242863b6f65fb70ad4f219b44c8c3c7ed64896742e7142d` |
| `reproduction/aristotle-prior-analytics-ii2/run_experiment.py` | `ca4aef952e61e6729fb55f1189e26572db486633b0af267a59589c384f295711` |
| `reproduction/aristotle-prior-analytics-ii2/test_model.py` | `cec70eff870dae0379a7424ca044dc2e7a3bc7321ea378bf632c3b4d4f7d3d24` |
| `reproduction/aristotle-prior-analytics-ii2/review_oracle.py` | `31378123b0afcbbc4a6a45d491fb829d621e2c35144e8aecde960579d9b98c61` |
| `reproduction/aristotle-prior-analytics-ii2/logs/environment.txt` | `ef2502778f1181c29ebe9f6bbe6424b77efe92c309c78a04fae19a76a4f98ab4` |
| `reproduction/aristotle-prior-analytics-ii2/logs/experiment-O.json` | `8f213c52583a12117b08130fbbeaf8fc1039070d4ceb084fae1ddb00994b3abf` |
| `reproduction/aristotle-prior-analytics-ii2/logs/experiment-OO.json` | `8f213c52583a12117b08130fbbeaf8fc1039070d4ceb084fae1ddb00994b3abf` |
| `reproduction/aristotle-prior-analytics-ii2/logs/experiment-normal.json` | `8f213c52583a12117b08130fbbeaf8fc1039070d4ceb084fae1ddb00994b3abf` |
| `reproduction/aristotle-prior-analytics-ii2/logs/independent-review.txt` | `7549fefe8efbe4b4f843d83816e2613350459b6a4b61a9ed468f8cb2ec2cba2e` |
| `reproduction/aristotle-prior-analytics-ii2/logs/tests-O.txt` | `1890305e8234464c14253f90ad01b8504a3198f942b4df172efb058874517fa3` |
| `reproduction/aristotle-prior-analytics-ii2/logs/tests-OO.txt` | `57e25dc2580ec40ec5a14b44ed21d5a0383eab020b69eb0d614ced4d5c112b00` |
| `reproduction/aristotle-prior-analytics-ii2/logs/tests-normal.txt` | `7f65c8ce2019e1a052c42b3fdff4560c5205b9fe74472abf6579370b43669483` |
