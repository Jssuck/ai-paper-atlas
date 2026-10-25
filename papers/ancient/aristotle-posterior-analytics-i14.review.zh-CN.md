# 《后分析篇》I.14：独立技术核验记录

## 结论与范围

**通过。** 本记录针对下列哈希对应的原创正文、集合模型、运行脚本和证据。来源版本、章界与勘误另见[来源台账](aristotle-posterior-analytics-i14.sources.zh-CN.md)。技术核验不是古代全部证明理论的复现，也不替代原文阅读；远端内容与数学渲染属于发布验证的另一环节。

审查者独立于模型编写者：既重跑配套测试，也另写四元素量词枚举程序。没有把作者自己的18项测试称为独立实现。所有公开材料仅含论文技术内容，不含私人运行路径、账户或对话。

## 可复查的实际执行

在 `reproduction/aristotle-posterior-analytics-i14/` 内执行：

```sh
python3 independent-review/oracle.py
python3 -m unittest -v test_model.py
python3 -O -m unittest -v test_model.py
python3 -OO -m unittest -v test_model.py
python3 model.py > independent-review/recomputed.json
cmp independent-review/recomputed.json results.json
```

证据：[独立oracle源码](../../reproduction/aristotle-posterior-analytics-i14/independent-review/oracle.py)、[oracle真实输出](../../reproduction/aristotle-posterior-analytics-i14/independent-review/oracle.log)、[三模式重跑日志](../../reproduction/aristotle-posterior-analytics-i14/independent-review/retest.log)、[重新计算与比较命令日志](../../reproduction/aristotle-posterior-analytics-i14/independent-review/recompute.log)、[重算结果](../../reproduction/aristotle-posterior-analytics-i14/independent-review/recomputed.json)。环境为同篇[环境记录](../../reproduction/aristotle-posterior-analytics-i14/logs/environment.txt)中的 Python 3.12.14，仅标准库。

真实结果：

- 普通、`-O`、`-OO`模式各18项配套测试通过；测试判断不依赖会被优化删除的裸assert。
- 独立程序使用四元素论域全部4096个S/P/M集合赋值；在三项非空政策下过滤不满足条件的赋值。以逐对象量词而非生产程序的集合运算重新计算，两种政策各192个格/式有效性判断均一致。
- 独立执行正文第二格16种前提组合的反模型构造，以及第三格两类全称结论共32个构造实例，全部满足前提并否定目标结论。
- 重新运行生产枚举所得JSON与保存的`results.json`逐字节相同。256类型占据模式、218个三项非空模式、各格4/6个有效式及三条归约零反例均一致。

## 手工数学审查

1. **第二格的一般反模型**：令S、P为不同单元素集合。分别按两前提是A/I或E/O决定相应对象是否属于M；M若为空则补M独有对象。这使任意前提对可满足，且S与P不交，肯定A/I结论均假。它是覆盖所有前提类型的构造，不是从几个错误例子跳到一般结论。
2. **第三格的一般反模型**：用单元素M满足任意两前提，必要时补M外对象使S、P非空。再加入M外的S独有对象可否定A，或加入M外S与P共有对象可否定E。两前提主项皆M，因而原真值不变。两个目标分别构造，不混同。
3. **第一格与存在**：Barbara、Celarent的任意对象证明正确，不需主项存在；从全称转为特称需见证。Darapti的M存在不可仅以S、P非空替代。
4. **归约**：E和I换位正确，A不可一般简单换位。Cesare、Camestres、Datisi的项序、见证与结论强度均保持；Camestres明确交换新主项和新谓项，而不是只替换格号。
5. **类型压缩边界**：AEIO只依赖交集/差集的空非空，故成员类型是否占据足以保持本语言真值。这个手工语义理由与有限实跑分开；没有把四元素或256模式的计算本身说成任意逻辑语言上的一般证明。
6. **解释边界**：第一格有效性未被等同于本质、原因、真前提或直接性；正文清楚区分原文、教学重构、分析推论和实跑。

## 发现与修正

初稿固定非空论域，而程序的允许空项政策另含一个空论域模式。正文已修正说明：该空模式与仅含一个三项外对象的非空模式对AEIO同值，不改变有效式列表；正文一般构造仍在非空论域内。这一修正已经复核。无未决技术错误。

## 哈希绑定

最终正文SHA-256：

```text
4b432af8762cd922e67b754ec4f60574c8c71585f8e2916b228b87b3d4250fdf
```

代码、正文、README、真实运行及独立核验附件的逐文件绑定见[SHA256SUMS](../../reproduction/aristotle-posterior-analytics-i14/independent-review/SHA256SUMS.txt)。清单不自引用，也不包含本审查文档。后续改变被审文件时须重新核验并更新绑定，不能沿用旧审查结论。
