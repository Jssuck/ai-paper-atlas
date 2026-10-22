# I.21 独立论证检查

`check_arguments.py`不导入作者模型，也不使用作者`holds`结果作真值来源。它按逐对象集合定义独立检查七个规则族，以及六个正文配置和两个边界配置。一般证明另见[论证审查](../../../papers/ancient/aristotle-prior-analytics-i21.audit.zh-CN.md)。

实际环境Python 3.12.14，仅标准库。每模式枚举对象数/情形数：(1,1)、(1,2)、(1,3)、(2,1)、(2,2)、(2,3)，共266888个配置；七规则共1868216次条件检查。最后一组262144配置，前五组合计4744。规则前提成立数不相同，不能将无前提的配置视作成功见证。

命令：

```sh
python check_arguments.py > results-normal.json
python -O check_arguments.py > results-O.json
python -OO check_arguments.py > results-OO.json
```

[真实执行日志](run.log)，[正常结果](results-normal.json)，[-O结果](results-O.json)，[-OO结果](results-OO.json)。三模式均通过；检查使用显式异常，不依赖优化时可删除的assert。优化模式数字在报告内按实际执行保存，三个报告不是伪称独立算法。

[版本绑定](review-bindings.json)记录主稿、作者模型、审核稿、独立脚本和真实日志的SHA256。之后任何改动需重新核相关结论并更新绑定；摘要只是内容身份，不替代审核。

边界：不检查输入解析和全部API错误路径（由独立代码审查负责），不校勘原文，不把有界枚举替代主稿的一般证明，不认证唯一古代语义。
