# 孔狄亚克《逻辑》第二部第九章：有限确定性教学复现

本复现只使用 Python 标准库，无须安装依赖、联网、笔记本环境、随机种子、API 密钥或付费算力。代码以 Python 3.10 及以上版本为目标；本次实际执行的解释器与环境记录在 [environment.json](environment.json)。这些小型现代模型用于说明 1798 年版印刷页 177–191 的若干区别，不是历史算法重建，也不把贝叶斯数值归于孔狄亚克。

## 阅读与运行

先读 [模型约定与历史边界](MODEL.zh-CN.md)，再按[中文逐步教学](WALKTHROUGH.zh-CN.md)预测输出、运行和解释。结果汇总见 [RESULTS.zh-CN.md](RESULTS.zh-CN.md)。在本目录执行：

    python examples.py
    python test_model.py
    python -O test_model.py
    python -OO test_model.py
    python verify.py

verify.py 会在普通、-O、-OO 三种模式下，分别启动真实子进程运行作者测试、示例和独立代码审计。它保存原始标准输出与标准错误，记录退出码和解释器参数，逐字节比较三种模式的示例输出，并把源码、测试、文档和日志绑定到 MANIFEST.sha256。

检查使用 unittest 的检查方法和显式异常，不使用可被优化删除的 Python assert 语句。日志中的运行时间自然会变化；例子输出和数学结果是确定的。重新执行 verify.py 会更新环境记录与执行日志，并把保存的示例结果与三次新运行逐一核对。独立代码审计另在 [AUDIT.md](AUDIT.md) 中绑定其实际检查的源码与原始证据哈希。

## 文件索引

- [model.py](model.py)：有限模型的小型 API
- [examples.py](examples.py)、[results.json](results.json)：可运行示例及保存的实际输出
- [test_model.py](test_model.py)：边界、反例与有限性质检查
- [independent_audit.py](independent_audit.py)、[AUDIT.md](AUDIT.md)：独立代码检查程序和完整审计报告
- [audit-evidence/](audit-evidence/)：独立代码审计者保留的三模式原始输出
- [argument-audit/](argument-audit/)：另一次独立论证审计的程序、执行记录与三模式原始输出；verify.py 不运行该独立审计
- [verify.py](verify.py)：作者执行与绑定工具
- [logs/](logs/)：verify.py 启动的真实子进程原始输出
- [environment.json](environment.json)：实际解释器、执行命令和退出码
- [PROVENANCE.json](PROVENANCE.json)：版本、原典来源与文件指纹
- [MANIFEST.sha256](MANIFEST.sha256)：本目录交付文件的 SHA256 清单

可执行以下命令校验文件内容是否与清单相符：

    sha256sum -c MANIFEST.sha256

清单不包含自身，以避免自引用；审计完成或交付文档变更后重新生成。清单校验能检出字节变化，不能代替对程序、历史文本或论证的审查。

## 范围与来源

模型以小型有限候选集上的精确表为输入，不含观测噪声，也不保证开放世界中的候选已穷尽。最小区分测试集合采用穷举，复杂度为指数级。有限枚举检查的是声明范围内的实现行为，不能证明普遍的哲学定理。完整状态识别与仅判断目标命题不同；当前最小测试 API 只实现前者。

PROVENANCE.json 记录来源与所读 OCR 摘录的 SHA256，并提供原扫描件 URL、PDF 指纹和公开来源账本链接。工作用 OCR 摘录本身不随包复制。目录名中的 1780 是作品年份标识，实际核读版本为 1798 年版，不能混为一谈。
