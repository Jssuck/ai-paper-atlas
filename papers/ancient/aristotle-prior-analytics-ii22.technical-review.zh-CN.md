# II.22 独立技术核验

## 审查范围和结论

独立审阅了正文的集合证明、偏好重构、算例、删条件反例及八道练习答案；另读 Jenkinson II.22 全章及注90–96，并查看 Owen 1853 印页228–230，以核对形式化是否越过原文条件。史源版本的系统核验另见[史源审查](aristotle-prior-analytics-ii22.source-audit.zh-CN.md)。本报告不把程序运行当作希腊文校勘或经验事实验证。

**最终判定：通过限定范围内的技术核验。** 此判定只覆盖下列哈希所绑定的材料；后续改变正文、前提、源码或运行证据，须重新检查。没有声称古代全文得到唯一正确的现代形式化。

## 逐项检查

| 项目 | 独立检查 |
|---|---|
| 肯定链 | 反向极端包含加正向夹链给三项相等；分别用C、A作中项的两次证明方向正确。无非空见证需求。 |
| 否定段 | 排斥关系对称但不等类、不自动互补；从小类否定恢复大类否定必须补反向小前提。正文没有把英文conversion一律写成等号。 |
| 两个二分 | 互斥与穷尽均显式，D到B与B到D分别证明；删覆盖/删互斥反模型确实满足剩余条件。 |
| only覆盖 | 说明把原文作对象域穷尽解释才得A=B∪C，再用C⊆B得相等；“除A自身”及对象/谓词层次没有被静默删去。 |
| 共主项桥梁 | C⊆A且B⊆C足以得B⊆A；C⊆B是解释互换而非最后两步必需条件。反模型确实阻断无条件推广。 |
| 偏好 | 定性论证补充相反程度对应、同优替换、组合单调和比较完备性；数值对称与加法只作为足够的现代教学模型。两组去对称反例计算正确。 |
| 目的和关系 | 未把爱情例、生成/毁灭或目的论写成代码证明的事实。 |
| 练习 | 八题答案均与前提范围一致，尤其第7题AC=−3、BD=3并不满足原始组合优先前提。 |

## 与生产代码独立的核验

[独立oracle](../../reproduction/aristotle-prior-analytics-ii22/audit/independent_oracle.py) 不导入生产实现，以单个对象的布尔隶属位写七个蕴涵，分别覆盖8或16种赋值，并检查六种删假设见证；还用100组有理数正参数核对对称可加偏好，另检查去对称和加入交互项的两个反模型。

[交叉比较器](../../reproduction/aristotle-prior-analytics-ii22/audit/compare_production.py) 导入生产接口仅作为被测对象。它不是调用生产函数生成期望：世界由逐对象四布尔位生成，预期由逐点逻辑及全称聚合计算，与生产powerset生成和集合操作不同。

- n=0、1、2、3共有1+16+256+4096=4369个四词项世界。
- 每个世界逐项比较七条规则的完整 `(前提,结论)`，合计30583对；不仅检查“未找到违规”。全部一致。
- 另对2401组整数偏好赋值，以差值不等式独立重排比较生产结果，全部一致。
- 单对象满足前提的四位型数为4、8、6、2、2、6、6。独立对象组合给出这些数的n次方，与生产输出一致。自由D使三词项规则的每个实质型加倍；未混淆这两种口径。
- 普通、`-O`、`-OO`分别运行两份审计脚本，六份保存JSON均记录PASS及真实优化级别0、1、2。显式异常检查不受优化关闭断言影响。生产另有三模式各9项unittest通过，三份生产JSON逐字相同。

重跑命令、真实日志与校验清单见[复现说明](../../reproduction/aristotle-prior-analytics-ii22/README.md)。有限检查不替代正文的一般证明；空域与空项只是明示的现代语义选项，不是历史立场断言。

## 修订闭环

独审确认否定恢复规则不能把原大前提预先写回，否则只是检查已有事实；生产最终采用B=C且A与C不交推出B与A不交。正文的日志一致性表述明确限定为生产JSON，避免误称优化级别与耗时不同的日志也逐字一致；数值模型明确正参数范围并区分生产反例单测与独立oracle反例输出。复现返链已检查为从二级目录返回仓库的两层相对路径。

史源审查进一步将共主项段精确定位为68a21–25、偏好段起点定位至68a25行中部；重核这些定位修订，未改变任何数学前提、证明、算例或运行结论，并已重新绑定正文和来源台账。

未发现数学或程序方面的剩余发布阻断。页面实际渲染、main提交、远端文件逐字比对、全站链接和冲突保护由发布验证另行完成，不属于本报告已经完成的断言。

## 最终内容绑定（SHA-256）

| 仓库相对路径 | SHA-256 |
|---|---|
| `papers/ancient/aristotle-prior-analytics-ii22.zh-CN.md` | `3dc4f49f559d82f2f9316f51a5064fdec974a21f21d3c4d26d9c13b506b7ea8b` |
| `papers/ancient/aristotle-prior-analytics-ii22.sources.zh-CN.md` | `ebd7de2073c9bc7bafb490620cf15d4be7bde44baa3bbfe689ba318be3278b8e` |
| `README.md` | `b8596c1447c845bde5d2c0169367ac3c34db637cb197a0cad6de736a5bbac471` |
| `reproduction/aristotle-prior-analytics-ii22/README.md` | `bc74d9778fcf9f9007cc66b8856571bb316a6e4c1c7275a3113ff8af3990134f` |
| `reproduction/aristotle-prior-analytics-ii22/SHA256SUMS` | `f7dcbfcc2036fc0c9aece4f9db91d629f2e52697fb1035b731e1284cda2d3d73` |
| `reproduction/aristotle-prior-analytics-ii22/audit/compare_production.py` | `7a456c69ad7fb7e6e9588dc78a0587ec8590298baa896fe786b1a62aae10d57e` |
| `reproduction/aristotle-prior-analytics-ii22/audit/comparison-O.json` | `357867789e6fbfcd78b5433650b68a98372e1bce8fc4b6d7cfc3554137e88f20` |
| `reproduction/aristotle-prior-analytics-ii22/audit/comparison-OO.json` | `5dc56129b4f848922b872d3d9174661dee2971165a7edcfa58029a236782c038` |
| `reproduction/aristotle-prior-analytics-ii22/audit/comparison-normal.json` | `5f893ec7405afe41ece58a1600cb50ab1f6200591470f7be1661f9bbd40432c0` |
| `reproduction/aristotle-prior-analytics-ii22/audit/independent_oracle.py` | `d430d5b4bea817457136ac4bf6c649ec8f7c6c14bec5c49cfa6f28cf552178e9` |
| `reproduction/aristotle-prior-analytics-ii22/audit/oracle-O.json` | `3375e375a5b399313406f15471cd5fb90bf9363d3449381f196f8407c89d0945` |
| `reproduction/aristotle-prior-analytics-ii22/audit/oracle-OO.json` | `e0e69f8ebc3bef52b04eef737471673eb319c3e89333fa2c801eceb4b966e281` |
| `reproduction/aristotle-prior-analytics-ii22/audit/oracle-normal.json` | `1b7e1f1758866ca52224fff020dfcfbf1d744a66e746fcde9e016ff08a7be5b7` |
| `reproduction/aristotle-prior-analytics-ii22/audit/run-audit.sh` | `146ea066d4623334194287e47d37d2b1c0efb856dd022722e8c5e22c221b17e7` |
| `reproduction/aristotle-prior-analytics-ii22/relations.py` | `7efa929b4dfa3296c8fb465b773b226f1503dfa21966fa65d4caad8a369bcebf` |
| `reproduction/aristotle-prior-analytics-ii22/results/comparison.log` | `52ab5f85ee92f67faf345c465de439e49bd9bebd0656f21274a84131a60f2a2d` |
| `reproduction/aristotle-prior-analytics-ii22/results/double_optimized.json` | `3d517eaae7dfffd9d54450cf901683b718452f63d2dff9ee737688347ec13627` |
| `reproduction/aristotle-prior-analytics-ii22/results/double_optimized.tests.log` | `020b7da0f66fdf1c98616a21a97ae3316c6f9f2946488c61f331d096c992c9ba` |
| `reproduction/aristotle-prior-analytics-ii22/results/environment.txt` | `15843db78ca0d6b0c93256c442b7fb653119cb8fc4565e224126f4ed2a7e52a0` |
| `reproduction/aristotle-prior-analytics-ii22/results/normal.json` | `3d517eaae7dfffd9d54450cf901683b718452f63d2dff9ee737688347ec13627` |
| `reproduction/aristotle-prior-analytics-ii22/results/normal.tests.log` | `734bbf13200e5dd20d6c840c1d15cc01ee4bccc7b4ee94060d28643d13b76f18` |
| `reproduction/aristotle-prior-analytics-ii22/results/optimized.json` | `3d517eaae7dfffd9d54450cf901683b718452f63d2dff9ee737688347ec13627` |
| `reproduction/aristotle-prior-analytics-ii22/results/optimized.tests.log` | `e3a91b8ff8d1f10b6ab765d1367e02f7ba9e4f0cdad2aa18c5a907499ee6d113` |
| `reproduction/aristotle-prior-analytics-ii22/run.sh` | `f51e61ad2587affbe5124562bd3642145d02e82e19b5f2d7802e626a373efc5a` |
| `reproduction/aristotle-prior-analytics-ii22/test_relations.py` | `e5a867186f8d0cc88a640f18a81794e067934d28c2ed061b8581c7a40f4cdbdd` |
