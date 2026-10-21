# 独立论证核验实跑

日期：2026-10-21 UTC。环境：Python 3.12.14，仅标准库；未导入作者的 `modal.py` 或测试模块。独立使用不可变集合重建正文语义。

实际执行（工作目录为本目录）：

```bash
python check_argument.py > normal.json
python -O check_argument.py > optimized.json
python -OO check_argument.py > optimized2.json
cmp normal.json optimized.json
cmp normal.json optimized2.json
```

三种模式均正常退出，两个比较命令均返回0；输出逐字一致。检查函数使用显式异常，不依赖会被优化删除的 `assert`。

每个项每个世界有4种外延，三个项、两个世界共 `4**6 = 4096` 个模型。运行110615项检查；9条有效路线均有非空的前提满足模型，7种无效推广均找到反例。另逐一检查正文第8节的实际表格，以及第6节跨世界换类的反例。完整计数在JSON中。检查次数不是实验样本量，也不与其他审计累计。

局限：只穷举两对象两世界；非有限域和任意世界集由正文一般集合证明处理。这里不验证全部历史模态逻辑，不证明不存在软件错误，不代表古代文本语义已唯一确定。
