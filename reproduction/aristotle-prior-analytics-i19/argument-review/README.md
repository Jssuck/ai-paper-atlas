# I.19 独立论证检查

[中文证明和反模型审查](../../../papers/ancient/aristotle-prior-analytics-i19.audit.zh-CN.md)为主要结论；这里保存不导入作者实现的标准库脚本和真实运行输出。

## 命令

在本目录执行：

```sh
python3 check_arguments.py > normal.json
python3 -O check_arguments.py > optimized.json
python3 -OO check_arguments.py > double-optimized.json
```

脚本使用显式条件检查并抛出异常，不依赖会被优化关闭的assert。任何异常令进程非零退出；不能只看输出文件是否存在。

## 已执行结果

- Python版本和优化级别、脚本SHA256分别保存在三个JSON输出中。
- 每次8395配置，41975次集合式与对象量词式比较。
- 八类蕴含全通过；真前提实例数量分别2135、1668、1639、1168、1168、1639、435、1245。
- 六个手工指定边界例及八个正文算例逐一检查所需真值/假值，模型及所有相关真值完整保留。
- 域大小0、1、2；情形数1、2；每个情形都轮流指定为实际情形。空域测试是现代定义边界，不是古代存在论主张。

normal、-O、-OO结果的数学部分相同；重复执行验证优化不会删掉检查，不增加独立模型范围。

脚本不导入作者代码，不联网，无第三方依赖，无随机采样。这里的集合恒等式交叉检查和有限模型枚举不能代替一般证明，不能认证完整古代模态体系。

[普通模式结果](normal.json) · [-O结果](optimized.json) · [-OO结果](double-optimized.json) · [源码](check_arguments.py)
