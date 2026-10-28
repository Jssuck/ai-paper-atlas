# Euclid I.30 最小教学复现

原创二维有理欧氏坐标教学模型：从两条直线分别平行于第三条，检查方向传递及三线互异条件。不是欧几里得的角证明、证明助理或第五公设独立性实验。一般原证见[中文深读](../../papers/ancient/euclid-elements-i30.zh-CN.md)，模型推导和反例见[教学复盘](WALKTHROUGH.zh-CN.md)。

## 使用

Python 3标准库，无第三方依赖，无网络访问。从本目录执行：

```sh
python3 run_all.py
```

geometry.py提供make_certificate(data)和verify_certificate(expected_input, certificate)。输入恰含A、B、C、D、E、F六个点，每点是两个规范有理数字符串的列表，例如['-2/3','1']；不接受布尔、整数、浮点、未约分或带空白形式。AB、CD、EF方向必须非零、两条平行前提成立、三线两两互异。允许反向方向和任意相对侧向，不暗设图形顺序。

证书包括完整输入、SHA256、前提与互异行列式、比例、截线交点和结论。核验器严格递归类型比较并与独立提供的输入绑定；哈希不是签名。仅二维模型，空间仅“不相交”不传递反例在WALKTHROUGH中，不混同空间方向平行。

## 真实执行范围

27项单元测试分别普通、-O、-OO通过。896个正确输入覆盖7斜率×4位置组合×4方向比例组合×4旋转×2平移；8个负输入直接调用生成器要求ValueError，不靠空证书掩盖前提遗漏。真实结果results.json，命令/退出码/stdout/stderr位于logs/01.txt至06.txt，环境与时间见environment.json和run-summary.json。

teaching.zh-CN.ipynb六代码格按顺序以标准库compile/exec真实执行，保存输出，**不是Jupyter kernel执行**。Notebook由原创create_notebook.py构建，无需安装依赖。verify_notebook.py可重新执行，测试耗时可有不同。

有限测试不证明一般定理，也不验证公理系统一致性、完备性或独立性。只发布原创代码、说明和已核查日志，不含原书PDF/全文翻译/私人信息。SHA256SUMS.json在独立审查追加后由发布者最终更新。
