# I.2 独立技术核验的公开证据

这里保存第二次审查实际生成的日志，不替代上一级目录的原始复现记录。

- `tests*.log`：原25项 unittest 在普通、`-O`、`-OO` 下重新运行。
- `results-rerun.json`：重新运行原演示，与原 `results.json` 的 JSON 值完全相同。
- `notebook-exec.log`、`notebook-review.json`：在隔离副本上执行原 Notebook runner，5个代码单元及输出与原件相同；只做明列的结构检查，不是 Jupyter 内核或完整 nbformat JSON-schema 验证。
- `independent_oracle.py`：此次原创的独立精确核验代码。使用环境已存在的 SymPy 1.14.0 代数数域计算几何约束，不复用被测几何、符号与点序函数。原代码仍只需标准库；SymPy 仅为这份审查脚本的依赖。
- `oracle-results*.json`：独立核验在普通、`-O`、`-OO` 下的实际结果。三份的样本计数和判定相同，运行时间可不同。
- `review-manifest.json`：审查对象、SHA-256 和实际执行方式。

从上一级复现目录重跑独立核验：

```sh
python3 independent-review/independent_oracle.py .
python3 -O independent-review/independent_oracle.py .
python3 -OO independent-review/independent_oracle.py .
```

需要已经可导入 SymPy 的 Python 环境；本次核验没有新安装软件包。脚本失败时以非零状态退出，不使用可被 `-O` 关闭的裸 `assert`。

294组是规范构造器输出；1568组是独立生成、范围更广的有效证书，不能算作构造器支持了新输入。56组A=C与168组A在BC内部属于这1568组的子集，不另加到总数。216组故障属于9类各24组。1875次算术对照和153次符号对照是运算计数，不是额外几何命题。有限样本无不一致不构成一般证明。
