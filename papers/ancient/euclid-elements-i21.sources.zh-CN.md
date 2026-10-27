# Euclid《几何原本》I.21：来源、版本与证据位置

对应[中文深读](euclid-elements-i21.zh-CN.md)。约公元前300年是作品的传统年代估计，不是本命题的独立发表日期；这里是几何与推理前史补读，不是现代AI论文。书内依赖次序不等于发现次序，也不声称穷尽前史。

## 实际阅读范围

| 来源 | 实读位置 | 边界 |
|---|---|---|
| [Heath1908第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908，印289–292上，PDF310–313，逐页目视 | 印289为完整I.21及翻译注；290–291及292上为评论，292的I.22标题以下不计本单元。档案标识02不是卷号。 |
| [Fitzpatrick2008希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick, *Euclid’s Elements of Geometry*, 2008修订纠正本，印/PDF24下–25上，实际文本读取并排印目视 | 24下题面、构造及长度证明，25上完成角度证明和结论；不含Heath长篇史注。现代排印不是直接核读古代手稿。 |
| [TCD Heath I.21转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp21_Heath1908.php) | 完整题面与证明、I.20和I.16引据 | 用于检索和对照，不是独立古代见证，不含Heath评论。 |

**勘误。** 已目视Heath扫描PDF16的ERRATA，未见印289–292的条目。此结论只限所读勘误表，不保证所有版本无误。Fitzpatrick修订标记不能代替逐项校核。

## 原证定位

| 主张 | 证据位置 | 解读约束 |
|---|---|---|
| 两线从底边B、C出发，在三角形内部相遇D | Heath289题面与设定；Fitzpatrick24下 | 必须保留共同底边端点及严格内部位置；不是任意两条内部线段。 |
| BD延长至AC上的E | Heath289构造句和图；Fitzpatrick24下 | 文字简写未单独证明交点存在；须辨明B-D-E及A-E-C点序。现代重心参数补证是教学重构。 |
| AB+AE>BE，加入EC得BA+AC>BE+EC | Heath289长度证明前段，标I.20；Fitzpatrick24下 | 用三角形ABE、同加保序及AE+EC=AC。不是从AB>BD、AC>DC逐边比较而来。 |
| CE+ED>CD，加入DB得CE+EB>CD+DB | Heath289长度证明后段；Fitzpatrick24下 | 用三角形CED、ED+DB=EB。两次局部严格界通过同一中间折线总长连接。 |
| BDC>CED，CEB>BAC，所以BDC>BAC | Heath289角度段，标I.16；Fitzpatrick24下–25上 | 分别取三角形CDE和ABE的外角；CED与CEB相同因为ED、EB为同向射线。长度论证不能直接替代角度论证。 |
| 英文“meeting”的补明 | Heath289脚注2 | Heath说明希腊用语已表示构成于一点或三角形，英文补词使相遇明确；不能据此声称他给古代命题增添了任意新条件。 |

## 评论和历史关系

Heath印290首先强调“从底边端点出发”的必要性，并转述Proclus p.327的反例。它不是对I.21的反驳，而是对删掉端点条件后错误推广的反驳：在直角三角形ABC中取BC内部点D，连接AD；从D沿DA截DE=AB，取AE中点F，连接FC。由FA=FE及三角形AFC的严格三角不等式，有CF+FE>CA；加入ED=AB，且F-E-D顺序给FE+ED=FD，遂得CF+FD>CA+AB。这两条线段的底边出发点是C、D，不是B、C。点序及截取可行性仍是构造条件，不应只依图断言。

印290–291，Heath报告Pappus继而讨论与Erycinus所谓悖论有关的构造。其概述涉及某些三角形中内部折线的长度和可以等于或大于另外两边和、各段长度比较、以及小于2:1的比例范围；这些都必须连同各自构形和条件阅读。印291给出底边大于腰的等腰三角形的一个样例证明，使用圆、平行线、截取和I.21。其中AF+FC<AB+BC一句Heath标注I.21，但F在BC边上，不能无条件当作严格内部点版本；可在ABF中用I.20后加FC独立补足这个边界型长度比较。它不是欧几里得I.21原证，也不是“固定B、C而D在内部时可以突破I.21”的反例。本单元如只概述其意义，不声称完成全部Pappus构造复现。

印291下–292上，Heath按De Morgan的建议引入垂线和斜线的比较：垂线最短；同侧斜足离垂足更远的斜线更长；等长斜线的斜足关于垂足对称。其证明先将线外点A关于底线反射到A′，利用全等和I.20比较斜线与垂线，再以I.21比较不同斜线，最后用对称全等得到另一等长斜线。它是后世编排建议和推论，不是I.21题面。最近点或坐标距离平方的现代证明须另行标注，不能倒置为原证明的依据。

## 收录与公开边界

- 本单元完整读I.21原证，并读上述评论以识别命题适用条件及后续用途；不宣称实读或完整复现Proclus、Pappus、De Morgan的原著。
- 现代向量、重心参数、精确根式符号判定、JSON证书和有限测试属于教学重构；执行结果不是一般定理的证明，也不认证所有古代空间公理。
- 内部扫描与PDF只作阅读证据，不作为公开附件，不提供原文全文翻译。
- 本次不计I.22及以后、全书或AI前史完成；暂缓项目不被计为完成。

最终正文绑定见[独立来源审查](euclid-elements-i21.source-audit.zh-CN.md)。
