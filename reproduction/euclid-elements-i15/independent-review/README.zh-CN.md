# I.15 独立技术核查

本目录由与复现实现分离的审查过程生成；只检查公开教学模型，不是历史全文形式化，也不是证明助理认证。

从复现根目录真实执行：

```sh
python3 -m unittest -v test_geometry > independent-review/tests-normal.log 2>&1
python3 -O -m unittest -v test_geometry > independent-review/tests-O.log 2>&1
python3 -OO -m unittest -v test_geometry > independent-review/tests-OO.log 2>&1
python3 independent-review/check.py > independent-review/check.log 2>&1
```

四个命令退出码均为0。三模式分别32测试；独立脚本检查496个非平行有理配置、2480次证书或输入篡改、576组向量普通角描述（17个不同角类）、323个有理角量同减账本；Notebook6格重新compile/exec执行，捕获输出与已保存输出逐字一致。没有使用Jupyter内核，也未将有限测试表述为一般定理证明。

独立角度交叉检查采用点积符号及余弦平方的精确有理值；它与实现的L1归一化表达不同，避免仅重复调用实现来断言实现正确。一般注入性理由见正文与独立技术审查报告。

篡改覆盖版本bool/int、交叉积、结论bool/int、比例与输入点B；原测试另检查NaN、tuple、额外键、缺键、角量破坏和退化输入。上述不是恶意输入全空间穷尽或安全审计。
