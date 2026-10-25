# I.29 独立技术终审

审查日期：2026-10-25。结论：**通过，限于下述正文版本及现代教学模型**。本审查者独立于正文和初始复现编写者；没有参与作者实现。来源语词与版本校勘由另一来源审查承担。本报告不是对全部亚里士多德逻辑、科学因果或原例心理学前提的认证。

## 1 逐项论证检查

- 两条 B→D→A、B→H→A 均由包含传递性得到同一个全称结论；任取元素的证明不依赖有限枚举。
- B 非空保证 D、H 有共同见证，但不保证任一全称包含方向。三元素反模型中两条路线均真且两方向各有反见证；不足三元素不能同时容纳共同点和两个方向的反见证。空 B 可允许不交中项，正文已显式区分。
- 中项候选与 A\B 的子集一一对应，故在 B⊆A 时为 2^|A\B|；端点相同只扣一个对象，严格内部候选数处理 k=0、1 正确。不存在 B⊆A 时无候选。
- 同链换切口与独立根前提不同；缺失图边不等于不包含。代码只枚举给定图的简单路径，没有把循环或所有科学解释声称已穷尽。
- Celarent 与 Cesare 的负前提中中项位置不同；集合不交对称性不抹去句法格差别。二者在允许空项的外延模型中有效；正文未偷换为第三格全称结论。
- 原文、教学模型、分析推论和实跑清楚分开；共同见证的有限反模型没有被用来冒称解决87b14–16全部历史解释争论。

## 2 独立 oracle 与真实执行

[独立实现](../../reproduction/aristotle-posterior-analytics-i29/independent_oracle.py)不导入作者 model.py 计算判定结果：作者用整数位掩码，审查者用显式 frozenset 和逐元素量化。先核对发布的全部集合计数及负规则计数，再扩大范围；另验证严格内部候选数，包括空域和端点退化。

真实运行命令（在复现目录）：`python independent_oracle.py > logs/independent-oracle.json`。

[真实输出](../../reproduction/aristotle-posterior-analytics-i29/logs/independent-oracle.json)：

- n=0至5：1365端点赋值、9331有序中项对、2884不可比对；5425非空主项对，交叠失败0、结论失败0、计数失败0。
- 严格候选数另查1365个端点赋值。
- 否定规则n=0至4：69905个四项赋值；两规则前提各4681次，同时成立1555次；错误结论0。
- 原发布n=0至4和n=0至3计数逐字段完全匹配。

另独立重跑作者22项unittest，在普通、-O、-OO三模式均通过，见[复跑日志](../../reproduction/aristotle-posterior-analytics-i29/logs/independent-tests.log)。这个复跑本身不等于独立oracle，二者分开记录。

## 3 Notebook核验

独立审查按顺序执行四个代码单元，逐字比较每单元stdout与Notebook已有输出，并核对执行序号，全部相同；过程中不写Notebook。Notebook代码使用作者模块，因此此项是保存输出真实性复核，不是第二套数学oracle。执行机制为标准库exec，不是Jupyter内核，不认证浏览器交互显示。审查未安装任何依赖。

## 4 限制与发布门槛

全部有限枚举只覆盖声明范围，不证明一般定理；一般教学结论依据第1节所核的任取元素和双射证明。审查未发现阻断技术错误。实际GitHub公式显示、全部远端字节、main提交与链接核验由发布者另行完成，不能仅凭本报告标记发布完成。若正文或核心代码发生变化，须重新审查并重绑哈希。

## 5 版本绑定（SHA-256）

- `papers/ancient/aristotle-posterior-analytics-i29.zh-CN.md`：`ec1b8f6f570172d7fb0fff023accd1a2aafde6e7ded419579269e3cde823d0a8`
- `reproduction/aristotle-posterior-analytics-i29/model.py`：`1db0ca15107f545778cd847565452bdcd34e617facf1c21963ee00abb40205c7`
- `reproduction/aristotle-posterior-analytics-i29/test_model.py`：`e399089111cc66e836c03a69a1c8cdfce0a9f05355cf1b7816d3736dd7df23bf`
- `reproduction/aristotle-posterior-analytics-i29/i29_teaching.ipynb`：`c7f05cb78e66b322d537198320644eaf5b0f9b28c19ed8b4257016289002a4ed`
- `reproduction/aristotle-posterior-analytics-i29/verify_notebook.py`：`c9768fb45a08aa5255d24ef0b35ce1f768ff5750ca641142be1f3f7485d48d4f`
- `reproduction/aristotle-posterior-analytics-i29/results.json`：`db4adbf81b638292e2c4bbdaea5209a34755b624a43806e6faf9428ac3ac556f`
- `reproduction/aristotle-posterior-analytics-i29/independent_oracle.py`：`0a8a231dda7f749189428bda7f655f0abded068b7126dc47eb7ccd16108e9856`
- `reproduction/aristotle-posterior-analytics-i29/logs/independent-oracle.json`：`2eaba1f6edc7dfa52faee57c54226670852760567e8b435b05fd3a9b799bbf95`
- `reproduction/aristotle-posterior-analytics-i29/logs/independent-tests.log`：`279542d6130042fd25d88d2bdab83dfeab4071c9e8e589ff694aa3b0dc448be6`
