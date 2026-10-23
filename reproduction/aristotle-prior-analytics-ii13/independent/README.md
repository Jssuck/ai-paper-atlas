# II.13 独立技术核验

`oracle.py` 独立采用显式集合包含、交集、差集判断，不导入生产程序的求值或蕴涵函数。八种布尔类型被当作不同对象；按基数再按字典序枚举支持集合，与生产输出的编码约定对齐，但逻辑实现独立。

实际命令：

```sh
python independent/oracle.py
python -O independent/oracle.py
python -OO independent/oracle.py
python -m unittest -v test_reproduce.py
```

三模式日志分别为 `normal.log`、`optimized.log`、`double-optimized.log`；独立结果为 `oracle-results.json`，生产测试重跑为 `production-rerun.log`。

核验范围：
- 255个允许空项模型与218个三项非空模型，每组64条固定项位候选。
- 128条路线的256条内部/外部记录逐字段核对有效性、可满足模型数、反模型数和最小反模型。
- 17个具名检查同样独立重算，涵盖四原文路线、B存在条件、错误假设、不同见证与结论强度。
- 四条原路线、内部无全称结论、I/O共真，以及完整原背景仍能另证原目标的区别。
- 生产13项测试另行实际重跑通过。

独立实现中检查使用显式异常，不使用可被优化删去的 `assert`。三模式执行都成功，并不表示古代语义已被唯一化。模型编码、允许空项政策和固定单步候选空间都是教学重构；一般证明另见正文，有限实跑不替代一般定理。

输出文件缺失时脚本只做独立模型计算并明确标记 `NOT YET AVAILABLE`；本次发布日志中已读取生产结果并显示完整比较 `PASS`。
