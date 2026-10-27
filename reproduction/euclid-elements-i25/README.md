# Euclid I.25 · 精确最小教学复现

这是现代 Gram 数据检查和原典证明依赖记录，**不是**完整形式化 Euclid，也不是历史实验复刻。原典用 I.4、I.24 和角大小的排除；本代码用现代内积模型独立核查结论。有限网格不能证明一般命题。

- [逐步说明](WALKTHROUGH.zh-CN.md)
- [可执行教程](teaching.zh-CN.ipynb)
- [核心代码](geometry.py)、[测试](test_geometry.py)、[样例](cases.py)
- [实跑结果](results.json)、[命令与终态](run-summary.json)、[环境](environment.json)、[Notebook 校验](notebook-check.json)
- [完整深读](../../papers/ancient/euclid-elements-i25.zh-CN.md)

## 重跑

仅 Python 标准库，无安装步骤。在本目录运行：

```sh
python run_all.py
```

该脚本依次运行 29 项 unittest 的正常、`-O`、`-OO` 三模式，250 个正例，Notebook 生成和执行。真实 stdout/stderr 与退出码保存在 `logs/01.txt` 至 `logs/06.txt`。所有关键校验使用显式异常或 unittest，不依赖被 `-O` 删除的 `assert`。

本环境未找到技能默认路径的 `new_notebook.py`，使用可审查的标准库后备生成器 `create_notebook.py`。Notebook 六个代码单元在共享命名空间中按顺序 `compile/exec`，随后在新命名空间重跑比对输出；**未运行 Jupyter kernel**。`execution_count` 保持 null，单元元数据标注 compile/exec 顺序，不假冒内核执行次数。`verify_notebook.py` 可直接复验已保存 Notebook。

## 范围与安全边界

证书记录规范输入、精确结果、两条排除依赖及三分性，不检查 I.4/I.24 的内部几何证明。证书核验器与生成器共享数学实现，所以独立技术探针与正文证明仍有必要。不是不可信网络输入服务；未设置输入字节或整数位数上限，不提供拒绝服务防护。JSON 拒绝重复键和非有限常数；数值只接受约分、正分母、长度为 2 的整数列表，明确拒绝 bool、浮点、字符串。所有字典字段必须准确匹配；证书逐层类型比较，不接受 True 冒充 1。输入被完整绑定，因此仅相同数值摘要不能跨输入重放。
