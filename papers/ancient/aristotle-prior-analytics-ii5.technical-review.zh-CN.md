# II.5 独立数学与代码审查

日期：2026-10-23。对象：[II.5中文深读](aristotle-prior-analytics-ii5.zh-CN.md)及[教学复现](../../reproduction/aristotle-prior-analytics-ii5/README.md)。审查者独立于正文起草和主程序编写。来源及异读考证另见来源审查；本报告不代替远端发布完整性与公式实际显示检查。

## 1. 数学检查

- 核对原文谓项在前与现代主项在左的方向。P为B⊆A，R为C⊆B，Q为C⊆A，V为A⊆C；全称不自带存在断言，补集限定同一论域。
- 逐步检查第3节肯定传递及两条反向恢复。反向包含必须另作假设，不能由原全称肯定免费换位。
- 检查第4节六关系账本：每一步包含传递有效，但T依赖R、V，S依赖V、P，最终V仍依赖P、R、V。严格包含链反例使P、R真而V假，排除错误消除假设。
- 检查第5节否定传递、否定前提恢复和补集覆盖桥。E命题对称换位不提供覆盖；B⊆U\A与U\A⊆B不可互相替代，二者同时成立才有B=U\A。
- 检查第6–7节所有特称推导的同一见证、两存在见证不能拼接、无法由所限前提恢复全称的非空反例。全称补集桥被准确限定为现代充分条件，不冒称最弱条件或唯一原文复原。
- 逐题检查16道练习及答案，均与正文语义一致。模型外延相等不等于语言意义或知识根据相同；局部有效不等于独立奠基。

## 2. 初审发现与修复

1. 初稿第9节把主程序的C⊆A短环说成正文第6步的V循环。现已明确它是同型短环、不是六关系账本的逐行重放；本独立审查另行实现正文V账本，得到依赖集合P、R、V。
2. 作者测试旧名称把反向补集桥称为更强。两个方向一般不可比较；已更名为“不由原方向蕴涵”，代码语义未被错误名称改变，修订后重跑通过。

未把“有限枚举全通过”视为一般定理证明或文本异读的裁判。正文一般推导已逐对象核查；历史存在预设及古代体系的完整语义仍超出本次重构。

## 3. 独立实跑

[独立源码与证据](../../reproduction/aristotle-prior-analytics-ii5/independent-audit/README.md)公开可重跑的标准库程序与实际日志。实际CPython版本、时间与命令见该目录 `run.log`。

- 作者程序与7项作者测试重新执行，退出状态均为0；作者JSON结果与原交付逐字节一致。
- 独立实现使用逐对象布尔量词，不导入作者谓词或模型实现。255种非空占用模式与218种全项非空模式，对8个有效、6个无效模式的前提满足数及反例数全部相符。
- 直接检查作者输出的12个反模型，均满足前提并违反目标；受限域三个词项确实都非空。
- 另枚举1–4个带标签对象的全部4680种成员赋值，包含重复成员类型。10个有效模式（作者8个及正文两个特称正向式）均零失败，6个无效增强均找到反例。
- 正文6个具体反例逐一通过；独立六关系依赖检查保留V。

这不是4680个模型各证明一个古代定理，也不是通用证明助手。作者依赖函数只遍历依赖边，不验证任意推理边的逻辑正确性；正文与复现README均清楚披露这一限制。

## 4. 内容绑定

以下SHA-256标识本地被审内容，不是Git提交号。修改后需重新检查相关结论并重绑；本报告不宣布已公开发布。独立结果不依赖公开进度记录中的统计字段。

来源台账中数学边界与根README本章新增入口、目录行和末段亦已核对；根README旧章节未在本次重新审查。

**结论：修订后技术审查通过。**

|仓库相对路径|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-ii5.zh-CN.md`|`f2f81471dfec6bc9f1b7bf179d0eb7bdfe11d472dd5cb4c247b5043c937b1b99`|
|`papers/ancient/aristotle-prior-analytics-ii5.sources.zh-CN.md`|`a45ddbd45c61d3e7a7d6dd88694d5347ce9692364676f8948a8cc3881ee90341`|
|`README.md`|`9b91f1f38209948d2e4f65b589e50f50c7934b2685624e182c2a69b07020ee75`|
|`reproduction/aristotle-prior-analytics-ii5/README.md`|`665a77641305fcec311831ad5cedb775133d8a19a6de9b36358de23c22130866`|
|`reproduction/aristotle-prior-analytics-ii5/check.py`|`081cfa9628b5b2d4f34708d12bcd821e0286f4cfebad00de7747a550f59c2059`|
|`reproduction/aristotle-prior-analytics-ii5/independent-audit/README.md`|`ca9f2abc852eac2dbd018368debc23308629668dcd2bf0ce2327c81e41dbb734`|
|`reproduction/aristotle-prior-analytics-ii5/independent-audit/audit.py`|`2b826e3967893b15740eb06890654e2757b7033970d0be6f5c4583f5a583afaa`|
|`reproduction/aristotle-prior-analytics-ii5/independent-audit/author-results.json`|`a14038b9d1d0e6c08b96a7730e133d2dbe703779570a83180d3de6282ce9f3e2`|
|`reproduction/aristotle-prior-analytics-ii5/independent-audit/author-tests.log`|`c4e2960bc000e5790b0a170e5d6055f60bec144e2eb17b5c988f38598541651b`|
|`reproduction/aristotle-prior-analytics-ii5/independent-audit/results.json`|`b8d27779c13b8cca6e5afde761217a9550d863a25a1cd782bace4bf9664ff14d`|
|`reproduction/aristotle-prior-analytics-ii5/independent-audit/run.log`|`2af16229e90ea289a6443a74c553f31555a8f2ede8d669dcd7b91c7ce4eed197`|
|`reproduction/aristotle-prior-analytics-ii5/independent-audit/run_audit.py`|`a58b706bd8dd82ee0db6025ddbe370862b5dbb34144567856ab52b5c574297c5`|
|`reproduction/aristotle-prior-analytics-ii5/results.json`|`a14038b9d1d0e6c08b96a7730e133d2dbe703779570a83180d3de6282ce9f3e2`|
|`reproduction/aristotle-prior-analytics-ii5/run.log`|`dda97d49bc12843f9517d88f1beb4f2538b1fe6a9596d816557c334f1d103c75`|
|`reproduction/aristotle-prior-analytics-ii5/run.py`|`e45440616d7e594aac1313f1016555a7fc999e156afabb8b56e61871d4bd0014`|
|`reproduction/aristotle-prior-analytics-ii5/test_check.py`|`31e5583972d6c3f15455c7b03ea182647a2f43f2e52f375fe8c8d04295cfa3c4`|
|`reproduction/aristotle-prior-analytics-ii5/tests.log`|`6046900db763ef86b204359e46986263ebe91eb321d47e9470760fc97369490c`|
