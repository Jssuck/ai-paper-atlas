# I.43：独立数学与代码核验

## 结论与范围

**核验通过，限于下述教学语义与最终文件。** 第5节交集包含的分解/合并、带背景的剩余义务等价、双向外延相等及反模型方向正确。第6–8节明确同一见证、空类、析取/否定不可任意投影，未把包含当成完整定义。允许空论域是程序范围，不裁定历史语义；正文空合取约定与至少二元AST的实现边界已明示。

证书是精确语法目标匹配加当前有限模型真值检查，不是任意背景下的演绎证明。语法不同但语义等价的目标不会自动共享证书；重复同一成分不能补漏。穷举计数不是历史解释的概率，有限测试不替代正文的一般论证。

## 发现与修正

原实现对请求目标的语义校验不够一致：空证书列表可令未解释目标直接返回False；错配证书可令未解释的请求目标不被检查。这不会导致错误接受证书，但与输入契约不一致。已在verify_components和verify_certificate入口对请求目标进行提前模型校验，并加入独立回归测试。作者18项测试和作者枚举在修正后的源码上重新执行，保存覆盖后的真实日志；所有模式通过，计数未变。正文和复现README另明确空合取数学约定不是现有AST支持的语法。

## 独立方法和真实结果

[independent_check.py](independent_check.py)以整数位掩码枚举W/L/P，不调用作者powerset或集合推导来生成预期值。对论域大小0至4的每个赋值独立计算包含、交、定义相等和反例，再与作者集合实现和组件记录检查逐项交叉比较。额外测试同一见证、空论域、漏成分/重复、精确目标语法、合取投影边界、空证据无效目标、错配未知原子、迟到无效证据和空合取拒绝。

三种模式各10项独立测试通过；每模式独立检查4681个模型，其中背景成立1555，局部真而全体假774，全体包含真而外延定义假440。作者18项测试三模式均通过。逐规模计数为1、8、64、512、4096；总和4681。并未把多次运行包装成更多独立模型。

|模式|独立真实日志|修正后作者测试|修正后作者枚举|
|---|---|---|---|
|普通|[10项](logs/independent-normal.txt)|[18项](logs/tests-normal.txt)|[4681模型](logs/experiment-normal.txt)|
|-O|[10项](logs/independent-optimized.txt)|[18项](logs/tests-optimized.txt)|[4681模型](logs/experiment-optimized.txt)|
|-OO|[10项](logs/independent-double-optimized.txt)|[18项](logs/tests-double-optimized.txt)|[4681模型](logs/experiment-double-optimized.txt)|

运行命令为在本目录执行python3（或python3 -O、python3 -OO）independent_check.py，作者命令见各日志首行和[README](README.md)。环境为[Python标准库记录](logs/environment.txt)，无新增第三方依赖。关键运行检查使用显式异常；测试unittest断言不会被优化选项删除。

## 最终SHA-256绑定

下表绑定实际审查及实跑版本。任何后续正文、源码、说明或日志改动均应重新核验相关部分并重新绑定；本审查文件自身不循环哈希。来源解读由独立来源审查负责，本审查不冒充原文校勘。

|文件（相对发布根）|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-i43.zh-CN.md`|`83e4d4598d55387b2f6a06e1e7ae1433fdc316fb1881fe2303f88e0525262733`|
|`reproduction/aristotle-prior-analytics-i43/independent_check.py`|`8c6e2b9a6b684651d3369566bf89e44795ba3b8b55380288ff1d78502a90c4ba`|
|`reproduction/aristotle-prior-analytics-i43/model.py`|`1cccafbd6a926e37d5acf5d95b54fadc46536d1ebc9e13065915e42ece4846f0`|
|`reproduction/aristotle-prior-analytics-i43/run_experiment.py`|`b7eac5bd46972b27399e74a3afc6f9f31c3abd64c002b64b3380e6deb37e5944`|
|`reproduction/aristotle-prior-analytics-i43/test_model.py`|`d041c551ef033b5cb38c1c3d9b0f8ff3dad6b9a3c5b5f973554286ec9621681b`|
|`reproduction/aristotle-prior-analytics-i43/README.md`|`70d548cd0e532e607a8e8793ec53adef3d1dff52441375b84b81168322b0ed01`|
|`reproduction/aristotle-prior-analytics-i43/logs/environment.txt`|`7885035d92fbbc4d38c1e412a8c4deb7943e6dfc676e64b94bfad0e08f1b1697`|
|`reproduction/aristotle-prior-analytics-i43/logs/experiment-double-optimized.txt`|`6fa76b15f2902fbf98adbf3798689bbaa5ea11a7b9b464d0f84128d520b5e8cb`|
|`reproduction/aristotle-prior-analytics-i43/logs/experiment-normal.txt`|`05f2e0373d3d8e866076f8c57e07cb7bcf8a05cfb2d161320a1a8beb27b1cd35`|
|`reproduction/aristotle-prior-analytics-i43/logs/experiment-optimized.txt`|`86139a0a27e2c05ef420a26dda854bc8920252d7eadea99990cbcd612d0b39ce`|
|`reproduction/aristotle-prior-analytics-i43/logs/independent-double-optimized.txt`|`7278c2770a2a812d963df7acc5f1e4ba6b35d0a2965c9cea6edfea6f5435b4af`|
|`reproduction/aristotle-prior-analytics-i43/logs/independent-normal.txt`|`feed98b4e8d6468e51fb8659e76028cef1b082c60e6a992abeea1e7ea1dbd69a`|
|`reproduction/aristotle-prior-analytics-i43/logs/independent-optimized.txt`|`3f7ec5f593125b2a69ce4a8b446e530ca9b20cb15a4bb055e625479ec68a39ee`|
|`reproduction/aristotle-prior-analytics-i43/logs/tests-double-optimized.txt`|`9d100e29db3d9a89e736d3362f1fa1056bab25abe562d480884bc54834ef4067`|
|`reproduction/aristotle-prior-analytics-i43/logs/tests-normal.txt`|`e8ec45fb512b9e10e25f9d40f93c96e3dfa015711acc039332fe4b2aca1242eb`|
|`reproduction/aristotle-prior-analytics-i43/logs/tests-optimized.txt`|`cbca746f8a5269cfe9e3d753dc94238511da1b87e8094e6445de8a5b711203d6`|
