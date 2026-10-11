# 原始页与边界核对

本实验逐图核对 1768 年版第 CVIII 封信所在的六个页面，范围从 CVIII 标题到信末署日。完整出版书目信息、扫描来源与定位依据见[主来源账本](../../papers/1768/euler-letter-cviii.sources.zh-CN.md)。下表记录实现所用的精确扫描文件名和校验值，便于复核；扫描图像未重复放入本代码目录。

| 扫描文件 | 印刷页 | 本实验范围 | SHA-256 |
|---|---:|---|---|
| original-160.png | 139 | 仅下部 CVIII 标题以后；排除前信 3 月 3 日日期 | `aee5a26ac87874b9cdb6e325172b50f6d6ea5377a850bfb28e1b350fd898d35a` |
| original-161.png | 140 | 本页全文 | `ffd1d7563b521f08b58f2d7dff8e19fd5c5dc6bddddb9e0d9abe14659efe2a38` |
| original-162.png | 141 | 本页全文 | `6e91581b136333672a80689de96c98d616ca636c0125a3ec5272031cdf35096d` |
| original-163.png | 142 | 本页全文 | `11024fe694c0cbbd804080a0a0aba0299b444297a73d19c2b3adc33a2bee633a` |
| original-164.png | 143 | 本页全文 | `89bb92b393016bdef50648633bebed6fb5917818014cf31a778032dd1f1d2659` |
| original-165.png | 144 | 仅上部至 7 Mars 1761；排除 CIX | `6f34bfdaece869a93f3e4c67e5a3e4ca35eb5113348b02f5db1933c0966684d2` |

## 核对重点

- p.140 的 « conséquence nécessaire » 提醒我们：作者讨论的不只是某次赋值上真值函数为真。
- p.141 的 « Outre cette condition on n’avance rien » 对应条件本身不额外断言其组成命题。
- p.143 将 « A est B » 整体称为前件，不能把 $`A`$ 这个项误当作完整命题。
- p.144 同时给出“非物体，因此精神”与“物体，因此非精神”；本实现区分穷尽性与互斥性各自承担的推理作用。

模型、算法、实验与测试均为本次新写的现代教学材料；历史原文没有给出此 Python 接口或有限允许世界数据结构。
