# 《后分析篇》I.16：独立技术核验

## 1. 结论与范围

对下列SHA-256绑定版本的正文、来源台账、模型、测试、运行脚本、结果与日志作独立技术审查；经两处修订后通过。审查涵盖项序、四种全称论式的逐元素证明、非空预设、普通假/完全假/部分假、正文数集例子、练习答案，以及有限枚举与科学直接性的边界。

这是数学和实现核验，不替代独立来源审查，也不声称已经完成远端提交验证或GitHub公式实际显示检查。源码中的集合解释只模拟外延关系，不认证历史科学中的合适中项、因果优先或心理信念。

## 2. 发现、修正及复核

1. 初稿将一个Camestres混合双假例同时用于Cesare；实际Cesare小前提为真。修订后分别采用C={1}与C={2}，固定A={1,2}、B={1}，两种论式分别得到大前提部分假、小前提完全假。已独立重算。
2. 初稿的“反质”可能被误读为保持等值的换质法。现改为保持主谓项不变、仅互换全称肯否；附件明确它不是改变谓项的等值换质法。
3. 全称肯定和全称否定只在主项非空时不可能同真；正文、程序和练习都分开处理空项。`status`优先判断真，故空主项不会被误标为完全假。
4. 第一格肯定错误的受限分类没有被当成无条件集合定理。程序保留大前提假、小前提真的外延反例，并将小前提假筛选明标为额外情景约束。
5. 第二格双完全假不可的证明使用任意非空B对象和真实B包含于A，不依赖测试规模；双部分假与混合双假均可实现。它没有把原文列举宣称为任意集合解释的互斥穷尽分类。
6. 正文不借“共同子项”强迫任意两个集合可比较，亦不隐去原文局部肯否张力。教学数集和现代系统启示均有范围标示。

## 3. 实际独立运行

审查者在单独输出位置运行普通、`-O`、`-OO`三模式的同一测试，各14项通过；未覆盖作者保存的日志。独立重新运行`model.py`，输出与公开`results.json`逐字节一致。

另外用独立位掩码实现（而非调用作者的真假分类函数构造期望值）交叉检查四对象论域的全部4096个有序三项解释、四条论式，共16384次比较，作者模型输出全部匹配；真前提假结论检查与第二格限制检查均通过。这个扩大范围的有限检查仍不是一般定理的证明。

公开结果中的计数亦可独立核算：三对象论域下，互不相交的非空有序A、B对为12对，每对有7个非空C，故Barbara背景共84种；非空B包含于A的有序对为19对，每对7个非空C，故另三式各133种。512与343分别对应允许空项和三项均非空的有序解释总数。计数不是古代作者报告的经验频率。

## 4. 文件绑定

以下路径相对于仓库根目录。若任一文件变更，应重新核验相应内容并更新绑定；浏览器排版修订也不例外。

| 文件 | SHA-256 |
|---|---|
| `papers/ancient/aristotle-posterior-analytics-i16.zh-CN.md` | `107a7547b4ee4963f662db49af8f992d111201bb5c078519d3eb974e4340c3a3` |
| `papers/ancient/aristotle-posterior-analytics-i16.sources.zh-CN.md` | `d986697c638f72d0b0845b083db15f4bfd29ea6e6e5c43f608e771b6f73a5b88` |
| `reproduction/aristotle-posterior-analytics-i16/README.md` | `03c83907a725f38be71f79787cd38dde763c0322b2ced45d70b8d937dd3ada00` |
| `reproduction/aristotle-posterior-analytics-i16/logs/environment.log` | `ce1f8f09e1a7338d1540b5c6ccb84ec8fc54874890784d76ae8802e3feafb343` |
| `reproduction/aristotle-posterior-analytics-i16/logs/tests-O.log` | `1cca6b763089f585cdc8e081421745b1116b6e329c289633133bdec0db8b8850` |
| `reproduction/aristotle-posterior-analytics-i16/logs/tests-OO.log` | `55e724a3b7148197e53e7e42f0a1764653847565a98f9f3769cb4abaa5c4b1f8` |
| `reproduction/aristotle-posterior-analytics-i16/logs/tests-normal.log` | `7874345fa2108d2f08bdcc58f23e2e55ca76992e8e29c54e212aae6bf2a35559` |
| `reproduction/aristotle-posterior-analytics-i16/model.py` | `1f9c432418c3418e7cc490420798a761cdd6a870946bd3d0838c7f27f8442648` |
| `reproduction/aristotle-posterior-analytics-i16/results.json` | `edd5f889819a8966cdd72314e066f579b7cbf84e8990be27c11d957d7784af4f` |
| `reproduction/aristotle-posterior-analytics-i16/run.sh` | `4035ab0342ea63e4901a20b41855dc369dd29f4fa6ac09472b208ab91fae99a6` |
| `reproduction/aristotle-posterior-analytics-i16/test_model.py` | `5eda2a7857ab331807cd56ec95c5377ee5c6dac4bca53a95daf08020a5148994` |
