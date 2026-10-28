# Euclid I.31 最小教学复现

原创有理欧氏坐标核验：检查指定侧的角复制和反向延长能否给出经过A的平行线。不是古代尺规操作模拟、形式化证明助理或第五公设独立性实验。[一般证明及历史分层](../../papers/ancient/euclid-elements-i31.zh-CN.md)；[模型推导与反例](WALKTHROUGH.zh-CN.md)。

## 运行

Python 3标准库，无第三方依赖或网络访问。在本目录运行：

```sh
python3 run_all.py
```

geometry.py：make_certificate(data)生成证书，verify_certificate(expected_input,certificate)核验。

输入恰含A、B、C、D、E、F六点，每点是两项规范有理数字符串列表，如["-1/2","3"]。拒绝布尔、整数、浮点、空白和未约分字符串。BC非零，D在线BC且D≠C，A在线外。D不必位于线段BC内部。AE非零，E与C严格位于AD两侧，角EAD等于角ADC；AF是AE反向射线。核验侧向、无向角、反延长，而非只检查平行输出。

证书绑定完整输入和其SHA256，记录点积、范数平方、侧向乘积、正比例系数与结论。严格递归比较类型，避免True与1混同。哈希不是数字签名。此核验器重算同一模型条件，故独立技术审查仍必要。

## 真实执行

27单元测试分别在普通、-O、-OO模式通过；1008正输入覆盖7斜率、4高度、3辅助点位置、3比例对、4旋转；10类负输入直接要求生成器抛ValueError，避免仅用空证书拒绝遮掩前提错误。results.json、environment.json、run-summary.json及logs/01.txt至06.txt保存真实证据。

teaching.zh-CN.ipynb六代码格按顺序通过标准库compile/exec真实运行且再次核对输出，**非Jupyter kernel执行**。读取了已安装Notebook技能；建议的本机模板脚本不存在，故使用原创标准库create_notebook.py生成结构，未安装新软件。Notebook不是完整复现古代构造。

有限样例不能证明一般定理；有理坐标模型不代表全部实数输入。只完成I.31教学单元，不能由本实验推出平行线唯一性在中性几何成立。SHA256SUMS.json由发布前最终生成，独立审查可能追加证据。
