# II.16 最小教学复现：共外延不等于互为原因

对象：[《后分析篇》II.16 中文深读](../../papers/ancient/aristotle-posterior-analytics-ii16.zh-CN.md)，98a35–98b38；[原文阅读入口](https://aristotle.johnhboyer.com/APo/book/2/#ch-2-16)。本目录仅含原创教学程序与真实运行证据，不含扫描件或全文翻译。

## 模型和可验证结论

`Model` 将谓词表示为同一有限论域的子集；`implies` 检查集合包含，`witnesses` 返回违例对象。它检查的是给定外延，不检验前提的自然学真实性、必然性、本质性或解释优先性。

- 三对象上C、B、A共有2^9=512种赋值，64种满足C⊆B⊆A，结论C⊆A违例为0。这是有限检查，不是任意论域的证明。
- `one_way`给出A⊆B失败的`other`对象；增加A⊆B及C⊆A后，逆向三段论形式才获保证。
- `orientations`在A=B时只返回两个**未选定的标签**。函数不接受因果观测，也不声称两方向都成立；正说明仅凭相同外延缺少选择方向的依据。
- 替代路线B、C各包含于A，但`c_only`反驳A⊆B，`b_only`反驳A⊆C。示例令A=B∪C只是便于演示；另一个测试含未列路线，显示两条充分性本身不保证A⊆B∪C。
- 树类T与条件S的合成模型**定义**A=T∩S，因此树论域内可互推，但`non_tree_s`反驳无条件S⊆A。此强形式依赖“结果A专用于树”的教学定义；原文的树内限定不单独规定树外所有情况。不能把古代凝结假说当作现代植物学定律。

输入会检查谓词和限制论域是否越界；未知名称抛KeyError。空前件、空限制域、空宇宙采用现代集合语义的空真，不能据此证明对象存在。测试显式覆盖这些差异，不声称完全复原亚里士多德存在预设。

## 运行

Python标准库，无第三方依赖；从本目录执行：

```sh
python run_all.py
```

该脚本按顺序真实执行并保存：

```sh
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python model.py
python run_notebook.py
```

19项unittest使用显式断言方法及异常检查，不依赖会被优化移除的Python `assert`语句。`logs/`记录命令、stdout/stderr与真实退出码；`environment.json`记录实际解释器。`sha256.json`绑定其他文件，不自哈希；再次执行后时间/日志/哈希可能变化。

## Notebook

[tutorial.ipynb](tutorial.ipynb)提供5个小代码单元，稳定且唯一的cell IDs。已阅读已安装notebook技能，但本地模板脚本不可用，参考资源读取失败；采用nbformat4.5手工结构并检查IDs。`run_notebook.py`使用**标准库exec而非Jupyter内核**从头顺序执行普通Python代码，捕获输出写回Notebook；没有安装软件，也不把此证据描述成Jupyter内核执行。

## 边界与改动

有限样例没有数据集、训练、预测指标、现代经验基线；它不是完整复现古代科学。若扩展为经验因果模型，必须另行给出干预、混杂控制与机制证据，不能把真值表扩大当成补足。代码/Notebook验证的是本文教学重构而非全章所有哲学主张。
