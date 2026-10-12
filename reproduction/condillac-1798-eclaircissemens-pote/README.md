# 《Éclaircissemens》致 Poté：有限观测模型

这是对 Condillac 1798 年文本（致 Poté，印刷页 192–198）所引出问题的**现代教学重构**，不是作者原有的计算模型，也不是历史思想、心理规律或神学命题的实验证明。核心问题：观念的接续能否告诉我们全部外部变化，以及两个观察者的接续是否自带共同的瞬间尺度？

仅使用 Python 标准库；无需联网、训练、第三方依赖或付费服务。推荐 CPython 3.10 或以上。该目录可独立复制和运行。

## 快速运行

在此目录运行：

```sh
python demo.py
python test_model.py
python -O test_model.py
python -OO test_model.py
python audit_model.py
python -O audit_model.py
python -OO audit_model.py
```

正常退出码为 0；验证失败会抛出异常并非零退出。测试不使用会被优化开关删除的 assert。

## 文件

- `model.py`：纯函数及输入验证，无文件、网络或全局状态操作
- `demo.py`：隐藏变化、联合辨识、边际日志丢失对齐三个反例
- `test_model.py`：有限穷举与拒绝非法输入
- `audit_model.py`：独立审计的边界输入及多观察者检查
- `AUDIT.md`：独立审计范围、方法与实测结论
- `SHA256SUMS`：交付文件校验清单，可用 `sha256sum -c SHA256SUMS` 核验
- `MODEL.md`：精确定义、一般证明和边界
- `WALKTHROUGH.md`：从观测词到有条件同步的逐步说明
- `RESULTS.md`：实际运行结果和不能推出的结论
- `logs/`：真实运行环境与 normal、-O、-OO 及演示输出

有限穷举只验证列明的小定义域；一般命题的根据是 `MODEL.md` 的证明。代码并没有估计真实主观时间，也没有测量太阳或任何人的心理状态。
