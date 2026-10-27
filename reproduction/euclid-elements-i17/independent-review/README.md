# I.17 独立技术核验

本目录的脚本独立核对精确几何恒等式、证书篡改与输入绑定、抽象角量账本，并重放 Notebook。它不替代一般数学证明，也不是独立形式化证明内核。

在上一级复现目录运行：

```
python3 -m unittest -v test_geometry > independent-review/tests-normal.log 2>&1
python3 -O -m unittest -v test_geometry > independent-review/tests-O.log 2>&1
python3 -OO -m unittest -v test_geometry > independent-review/tests-OO.log 2>&1
python3 independent-review/check_independent.py > independent-review/result.json 2> independent-review/check.log
```

上述四条命令本次实际运行均退出0。三种模式各34测试通过。独立脚本使用81个新有理坐标构型；逐一核243对角的分子等于绝对两倍面积乘对应边长平方，检查1377次篡改/类型/输入绑定拒绝，216个任意正有理直角单位的账本。对严格前提退化为相等的情况也要求拒绝。

Notebook六格在同一Python命名空间中逐格compile/exec，捕获标准输出和标准错误，与已有输出逐字比较一致；未调用Jupyter内核，没有更改Notebook内容。运行环境见environment.json，计数见result.json。有限构型不覆盖任意输入，也不证明所有实现路径正确。
