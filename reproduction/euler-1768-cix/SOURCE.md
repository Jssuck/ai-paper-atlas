# 来源与教学构造说明

## 1. 历史文献

Leonhard Euler，*Lettres à une princesse d'Allemagne sur divers sujets de physique & de philosophie*，Tome second。Saint-Pétersbourg：Imprimerie de l'Académie Impériale des Sciences，1768。**第 CIX 信，印 144–148 页；信末署 1761 年 3 月 10 日。**

- [1768 主底本扫描，PDF 第 165 页／印 144 页](https://archive.org/download/lettresuneprinc01eulegoog/lettresuneprinc01eulegoog.pdf#page=165)
- [1768 扫描，PDF 第 169 页／印 148 页及署日](https://archive.org/download/lettresuneprinc01eulegoog/lettresuneprinc01eulegoog.pdf#page=169)
- [太平洋大学整卷学术书目，E344](https://scholarlycommons.pacific.edu/euler-works/344/)
- [配套完整精读](../../papers/1768/euler-letter-cix.zh-CN.md)
- [逐页、版本与有界检索账本](../../papers/1768/euler-letter-cix.sources.zh-CN.md)

E344 标识整卷，不是名为第 CIX 信的一篇独立期刊论文。1768 是此卷出版年；1761 是本信署日。

## 2. 本程序实际核读了什么

程序作者阅读了覆盖本信及署日的 OCR 辅助文本，并逐图检查了全部五页原书图像：**PDF 第 165–169 页，对应印 144–148 页**。OCR 用于定位；页图用于确认文字边界与印出的日期。

印 144 页上部是前信结尾，本信从 CIX 标题开始。印 148 页 CIX 的署日之后，CX 标题开启下一信。这两个相邻信件的文字不属于本程序的来源范围。

- **印 144–145 页：** 感知、观念、当前外部存在确信、愉快／不快；感觉刺激停止后的保持；不持续出现在心灵面前的观念。
- **印 145–146 页：** 回想内容与当前感觉／确信的区别；回想火灾的例子。
- **印 146 页：** 几乎遗忘与从未接触的区别、重新呈现时的再认，以及作者所说的更容易把握。
- **印 146–147 页：** Euler 对唯物论印痕解释的报告与质疑。
- **印 147–148 页：** 脑变化、判断、抽象、意志、自由与恶的更广论述。本项目说明其存在，但不对它们建模。

程序作者没有独立声称对校了所有版本或穷尽检查勘误。配套来源账本另行说明实际完成的有界版本与文献核查。本复现目录不复制原书扫描、OCR 全文或完整译文。

## 3. 明确属于现代教学创作的内容

状态四元组、两个内容标签、转移规则、访问开关、布尔再认、输入／确信报告、完整复位、证明、测试与原文到代码的对应说明，均为本项目的现代教学设计；不是原文抽出的算法、历史伪代码或估计得到的认知机制。

火是原信例子；铃是另加的对照标签。原文提供问题与概念区分，代码规定一种很小的结构，让这些规定的后果可以核查。测试检验实现是否符合规定，不验证 Euler 的观察或形而上学结论。

本项目没有从程序推断学习速度、反应时间、再认概率、记忆分数或主观体验。完整模型状态只有 `State` 的四个明示字段；结果文件是外部观察者记录，`erase_all` 后机器不能读取它作为额外记忆。
