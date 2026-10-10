# Sylvester 1852：原刊、主张与校读账本

## 1. 书目与原件定位

- 作者：J. J. Sylvester；原刊署身份 Barrister-at-Law。
- 原题：*LVIII. On a simple Geometrical Problem illustrating a conjectured Principle in the Theory of Geometrical Method*。
- 刊物：*The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science*，第四辑第 4 卷，第 26 号，1852 年 11 月，366–369 页。
- 文末署日：1852-10-04；未见宣读日，确切发行日未核定。不要把署日写成刊发日。
- DOI：[10.1080/14786445208647142](https://doi.org/10.1080/14786445208647142)；其 Crossref 元数据题名把 simple 错排为 simpel，以原刊为准。
- [Internet Archive 完整合订卷](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf)，整卷 PDF 第 380–383 页对应本文原刊 366–369。
- 实际取得整卷的 SHA-256：`8d09201f20cc2f06903df54d72e1d913c8148e07aa832854636ff56ebc670c8b`。哈希用于辨认本次核读字节，不代表任何排印正确性。
- 卷首题名页见 [PDF 7](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=7)；十一月分册标志见 [PDF 335](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=335)；本文末页下栏也直接印第 26 号、November 1852。

本文、唯一示意图、两条脚注及末注全部读核；字形冲突处另提高渲染分辨率核看。OCR 仅用来检索，公式与页界以扫描为依据。公开包不含整卷、抽页 PDF 或扫描图，只保留链接、原创分析、原创图和运行证据。

## 2. 四页主张账本

| 原刊页 / PDF | 实际内容与作者地位 | 本篇怎样使用 | 必须保留的边界 |
| --- | --- | --- | --- |
| [366 / 380](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=380) | 内角平分线等长命题；Cambridge 约一年前的来源叙述；B. L. Smith 证明；作者自己的证明开头；唯一图 | 主文 §2–4 重建点位、平行截线与角比较 | 作者的首次出现回忆不是穷尽优先权调查；图画的是反证假设的辅助配置，不能直接量尺验证 |
| [367 / 381](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=381) | 相似比、角度和垂距推论；按比例分角的推广；正弦等式、正切商式；正与负参数讨论 | §5 逐步由交点参数到交叉相乘再到商式 | 有向角、射线正向、零分母、正切极点和等腰的 0/0 都要分开处理 |
| [368 / 382](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=382) | 宣称区间外成立、区间内失效；正负半参数例子；轨迹和根数脚注；关于归谬必要性的第一层猜想 | §6 具体反例和字形校核；§8 区分存在证明与全部证明量词 | 特殊式可辨字形与前页不一致；任给角差的存在说法需限定且半参数有反例；原文没有完整根数分类；不能把猜想写成已证方法论 |
| [369 / 383](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=383) | 圆弦问题、二次式与逆向一次式；同弧角推逆命题的隐藏间接性；更强的必要/充分式愿望；署日与末注 | §7 补全相似与正根条件；§8 分析未定义的证明类别 | 圆弦负根是不满足顺序的实根，不是无实根；末注关于知名分析家的传闻不作为独立历史证据 |

## 3. 关键字形：原印与分析式分开

### 3.0 第 366 页点名的校核

原扫描末段两处字形可辨为 FBA、FB，但原图和论证涉及的是角 EBA 与线段 EB：已知相等的是 AD 与 BE，并没有 AD=BF 的假设。本文以 EBA、EB 重建证明，同时保留此字形观察；不据单一扫描判定印刷或褪色原因。

### 3.1 第 367 页可靠主公式

原刊正弦式的两个分母分别为 $`\sin2n\alpha`$、$`\sin2n\beta`$，不能按 OCR 把两者都写成前者。其后正切式为

```math
\frac{\tan((n-1)(\alpha-\beta))}{\tan(n(\alpha-\beta))}
=
\frac{\tan((n+1)(\alpha+\beta))}{\tan(n(\alpha+\beta))}.
```

正文紧接着提到恢复整式形式后 $`\alpha=\beta`$ 可满足；这也是作者自己承认商式不能直接覆盖等腰解的证据。

### 3.2 第 368 页两处特殊式

对同一原刊图及较高分辨率渲染作独立重复核查后，观察如下：

- $`n=1/2`$ 的展示式右端可辨为 $`1`$，没有可辨的负号。
- $`n=-1/2`$ 的展示式右端也可辨为 $`1`$；分子角的字形为 $`(3\alpha-\beta)/2`$，而非明确的 $`3(\alpha-\beta)/2`$。
- 接着作者称 $`\alpha+\beta=90^\circ`$ 和 $`\alpha-\beta=\pm90^\circ`$ 给出非等腰解。

把参数代回 367 页主公式，分别得到

```math
\frac{\tan(3(\alpha+\beta)/2)}{\tan((\alpha+\beta)/2)}=-1,
\qquad
\frac{\tan(3(\alpha-\beta)/2)}{\tan((\alpha-\beta)/2)}=-1.
```

90° 例子也独立支持 $`-1`$，不是 $`+1`$。因此本文使用「扫描可辨字形与前页代数一致式冲突」这一有界结论；校核式明确标作教学修复。当前只有该扫描底本，不能由扫描断定作者手稿、排字过程或褪色的原因，也不把本文核查改称历史正式勘误。

### 3.3 第 369 页常见 OCR 陷阱

两式依次是

```math
x^2+ax=b^2,\qquad a(a+x)=b^2.
```

第二式右端绝不是 $`0`$；两式中的 $`a`$ 在各自问题里表示已知段，所固定的近/远位置不同。将逆向式误读成零会同时破坏几何意义与作者的次数比较。

## 4. 勘误检查与版本边界

[同卷印刷 viii 页 / PDF 14](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=14) 的勘误只针对 359 页第 7 行，与 366–369 无关。本文四页未见 Addition、Postscript 或替换段标志。这个核查范围只能支持「本次所查同卷勘误不适用于本文」，不能支持「作者从未发表过任何更正」。十二月的 De Morgan 与 Drach 是另作者的回应，不是 Sylvester 自行修订。

本次没有搜尽所有重印本、手稿或后期版本，没有以这四页的完成关闭其他论文的版本缺口。

## 5. 同时代回应：只作有限比较

### De Morgan

A. De Morgan, *LXIX. On Indirect Demonstration*, 同刊第四辑 4，第 27 号，December 1852，435–438；文末署 1852-11-01。DOI：[10.1080/14786445208647158](https://doi.org/10.1080/14786445208647158)。[原刊 PDF 449 起](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=449)。438 页余下是另一篇文章，不能混入范围。

- 435 页：区分四种证明形式，尤其直接肯定与直接逆否。
- 436 页：批评把逻辑转换再包成一个不必要的反证；以 Euclid I.6 等为背景。
- 437 页：明确回应上期 Sylvester，说明自己对其多数内容同意，分歧在间接证明的解释。
- 438 页开头至署日：形式与材料之区别，并不要求全部改写 Euclid。

这里实际阅读用于分析其回应的针对性；尚未为该文单独做完整结构研究、独立教学复现与发布验收，因此候选表不标记它「深读完成」。

### Drach

S. M. Drach, *Remark on Art. LVIII. (of Phil. Mag. for November) by Mr. Sylvester…*, 同卷 479 页，December 1852；文末署 1852-11-22。[原页 / PDF 493](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf#page=493)。同页其余部分为气象观察，不属于该短评。

其虚数抵消类比只用来展示同时代接受，既不是普遍判据的证明，也不是正式更正。本次没有单独展开该短评的全部思想背景或作为第二篇任务发布。

## 6. 证据等级与复现等级

| 层级 | 本次实际做了什么 | 没有据此声称什么 |
| --- | --- | --- |
| 原刊内容 | 全四页及图、脚注逐页阅读与原图核查 | 没有镜像原文或提供全译 |
| 书目 | 合订卷、分册标志、末页、DOI 相互校对 | 不猜确切发行日或未印出的宣读日 |
| 教学重构 | 展开截线证明、正弦化简、正性与圆弦相似 | 不说这些展开公式逐字印在原刊 |
| 批判分析 | 区分角域、带符号解、表示变化与证明量词 | 不把现代形式逻辑术语冒称作者已经定义 |
| 程序 | 确切命令、输入、日志与 Notebook 范围见运行附件 | 不用有限计算证明全部实数几何或普遍方法猜想 |
| 独立审计 | 审计者重新看原图和公式，再查文字与代码 | 不把同一 OCR 的重复读取算独立底本 |

正文与代码如有冲突，以明确数学定义与原刊证据重新核查；不得仅因测试通过而覆盖来源差异。
