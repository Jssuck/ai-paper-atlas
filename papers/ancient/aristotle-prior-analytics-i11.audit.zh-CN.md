# I.11 完整论证与数学独立审计

结论：**PASS，已修正两处文字精度问题并按最终正文重新核验。** 本报告独立检查正文各节、六式分类、一般证明、反模型与20道答案；不以作者测试通过代替论证。

## 1. 阅读与边界

完整读取本篇正文和来源账本；原典逐图核查由另列独立来源审计承担，本审计对其给出的31a18–32a5、Owen103–106范围和段落表作一致性核对，不冒称再次独立读取所有手稿和版本。现代必要性语义不是古代语义唯一解释。历史表的“不保证”与现代锚定模型的“有效”在Disamis/Bocardo等处明确分开。

## 2. 全文逐段审查

| 正文部分 | 审查结果 |
|---|---|
| 1–2 问题与版本 | 原文、重建、模型和实跑四层明确；版本日期不当作创作年；章界与账本一致 |
| 3 记号 | AEIO以主项在前；C→A、C→B、B→A固定，必要I换位未预先假定 |
| 4 原章分类 | 六式12配置与来源段落对照；Darapti/Disamis小前提必要先得逆向必要I，另列换位依赖；末尾必要O失败未漏 |
| 5 四条见证路线 | Darapti/Felapton另需C存在；Datisi/Ferison特称前提给出同一对象；未把不必然混成必然不 |
| 6 两条逆向路线 | 直接仅得N I(A,B)，改到N I(B,A)依赖附加规则；没有把普通换位偷换为必要换位 |
| 7 模型定义 | 实际世界包含于非空W，固定对象域及谓词可变明确；稳定交与可能并用于不同量质；必要推出实际的证明条件足够 |
| 8 六个一般证明 | 每式逐一追踪同一个c；在任意非空W、任意域成立；只有AAI/EAO需另假定C非空。现代额外有效式明确不算历史验证 |
| 9 一对象反模型 | 两组前提真实满足、对应必要结论失败、普通结论仍成立；反模型否定一般保证而非断言所有模型结论假 |
| 10 模态量词 | 轮换见证反驳固定对象交换；双边稳定I对称，但不能无证替换中间式 |
| 11–12 实词与取证 | 失败例归属保留；31b33–37位置已修正；不会把生物实词例称为实证数据 |
| 13–15 复现和局限 | 一般证明与有限枚举分开；未宣称统一古代模态语义、软件完备或AI性能实证 |
| 16 全部练习 | 20问均有答案；存在、方向、量词、反模型、历史归属回答与正文一致 |

## 3. 两处修订记录

初稿把同一见证稳定性写为“恢复对称结论至少需要”的条件，可能误读为结论成立的必要条件。已改为沿同一见证完成该步骤所需，并明确结论可能由另一见证成立。一个足够的证明路线不等于结论的全部成立条件。

证据表中“全称必要否定加特称肯定”的起始行从31b29改为31b33–37，与来源账本相合；31b28–33仍属此前肯定失败的实词例。两项不是作者正式勘误，不改古代正文。

## 4. 一般数学核验

记实际集合为C₀、B₀、A₀；稳定A为所有A_w交集，可能A为所有A_w并集。

对大前提必要的AAI、AII，选出的c位于C₀且B₀，必要A把c放入稳定A。对EAO、EIO，同一c不在可能A。IAI直接由必要I给C₀中的稳定A见证，普通A(C,B)把它送入B₀；OAO同理以不在可能A的见证得到必要O。每条在任意域/世界成立，不调用有限枚举作证明。

反向Darapti/Disamis得到实际A中稳定B见证。这不等于实际B中稳定A见证。单对象A在世界1消失、B保持就是严格反例。加入该见证A稳定是沿同一对象完成交换的充分桥接，但并非结论的一切可能成因。

实际世界被包含保证稳定A包含于A₀、A₀包含于可能A，故四类必要命题都推出对应实际命题。若省略这一条件，不能保留该推导。

双边稳定I由两个稳定集合交集非空定义，因此对称；但实际A中的稳定B对象未必是稳定A，故不能把锚定I的前提免费强化成双边稳定I。逐世界存在也不能免费换成跨世界固定对象。

## 5. 独立执行

[独立检查器及命令](../../reproduction/aristotle-prior-analytics-i11/argument-review/README.zh-CN.md)使用Python标准库，没有导入作者教学实现。normal、-O、-OO均执行成功，每模式4,096模型、63,659显式检查，三日志逐字一致。

有限分类是：锚定六式仅大前提必要的方向无反例；六种小前提必要都有反例；句子必然性12配置均有反例。每配置检查前提可满足性，避免以无模型伪造有效结论。正文未声称句子必然分类为古代作者结论。

本审计没有检验所有更大模型、所有代码缺陷或所有历史解释。一般性来自上述证明与具体反例，不来自测试次数。

## 6. 最终文本和执行绑定

以下SHA-256覆盖审查实际读取的正文、来源和独立执行证据；未把哈希等同于正确性证明。后续改正文须重新检查绑定。

| 文件 | SHA-256 |
|---|---|
| papers/ancient/aristotle-prior-analytics-i11.zh-CN.md | 8155b8d7690ec6a361ad5e8225bbcc2111c69ffd6347bd202cc4d0978a88c624 |
| papers/ancient/aristotle-prior-analytics-i11.sources.zh-CN.md | a53f1c8581ba6f85e711c8f7deb31a00ca84ddf0daaa60086c1c8353460685c5 |
| reproduction/aristotle-prior-analytics-i11/argument-review/README.zh-CN.md | 76d66676d52ec040d2eafcc6eead5b147d9928730358f6d0f5eda6f67a2c5db1 |
| reproduction/aristotle-prior-analytics-i11/argument-review/check_argument.py | a1c205c542b4a237f9e0b90ae5f618dd36f16985c5c2bac3040a782679b5eaf9 |
| reproduction/aristotle-prior-analytics-i11/argument-review/double-optimized.log | f4af472013f4c6e735086f43ad2fae7bbf6d21d44f21f19a53a6a9bd6adb407f |
| reproduction/aristotle-prior-analytics-i11/argument-review/environment.json | 28c79547f092b62e6d1cafeddbb92043a28dba621dfe9cd920a2ec0a120dfde7 |
| reproduction/aristotle-prior-analytics-i11/argument-review/normal.log | f4af472013f4c6e735086f43ad2fae7bbf6d21d44f21f19a53a6a9bd6adb407f |
| reproduction/aristotle-prior-analytics-i11/argument-review/optimized.log | f4af472013f4c6e735086f43ad2fae7bbf6d21d44f21f19a53a6a9bd6adb407f |
