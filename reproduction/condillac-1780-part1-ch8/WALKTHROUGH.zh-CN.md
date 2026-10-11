# 逐步读懂演示：同一种欲望，为什么可以有不同判断？

先在本目录运行：

```sh
python demo.py
```

输出是JSON；已运行的版本见[演示结果](results/demo.json)。这不是训练模型，也不需要安装包。完整定义与一般证明见[MODEL.zh-CN.md](MODEL.zh-CN.md)。以下编号对应输出的九个案例。

## 1. 先认识四个世界

`World`只记录一个名字与两个独立布尔值。`obtains`是随后能否获得对象，`obstacle_free`是过程中是否无障碍；它们都不等于当前是否已经拥有。

| 世界名 | 将获得G | 无障碍O | 这个赋值用于什么 |
|---|---:|---:|---|
| failure_obstacle | 0 | 0 | 失败且有阻碍 |
| failure_clear | 0 | 1 | 检查未设置成功桥梁的形式边界 |
| success_obstacle | 1 | 0 | 最后得到，但过程有障碍 |
| success_clear | 1 | 1 | 得到且无障碍 |

第四列是教学解释，不是作者给出的世界表。特别是`failure_clear`不声称原文真的支持“全部条件协同却不成功”；它逼迫我们交代从“没有障碍”到“会获得”是否需要另加条件。

## 2. 案例01：缺少并不自动成为需要

```python
Affect(lacking=True)
```

只有当前缺少为真；认识、享用习惯、想象快乐背景都还没有。即使信念支持集是`success_clear`，结果仍是：

- objective_lack = true
- deprivation = false
- need = false
- desire = false
- hope = false
- narrow_will = false

这里主体可以被标注为“判断会得到”，但没有相应欲望，就不满足本模型中希望的组合条件。判断与欲望是两部分。此处将未知对象与判断输入搭配，是接口独立性测试；程序未强制这些层之间的完整心理连贯性，并非主张人能对全无认识的对象形成有内容的判断。

## 3. 案例02：从未享用，也可以想象其乐

```python
Affect(
    lacking=True,
    known=True,
    habitual_imagination=True,
    faculties_directed=True,
)
```

`habitual_enjoyment`仍为false。按照这里的约定，认识对象、具有想象快乐的背景、当前缺少它，足以进入被剥夺及需要；再有方向记录，当前欲望为真。

`habitual_imagination`表示原文习惯语境中的快乐想象，没有暗定“想过几次才算习惯”。`need`在这里不是测量值；它来自明确写出的“这种剥夺导致受苦”的约定。用想象分支正是为了避免把“先前真的享有”误设为必要条件。

本案例候选集只有`success_clear`，实际世界也如此，经验习惯两个标签都为真，所以希望和狭义意志都为真。

## 4. 案例03：希望可以与有障碍相容

保持上面的欲望，只将候选集改为：

```python
frozenset(["success_obstacle"])
```

所有候选世界都将获得，所以`judges_obtaining=true`。但候选世界并非无障碍，所以`judges_no_obstacle=false`。结果：

- hope = true
- narrow_will = false

这不是降低一个成功概率。代码没有概率。它比较的是两种不同的命题内容。

## 5. 案例04：没有隐含的“无障碍必成功”桥梁

候选集改为`failure_clear`，欲望与经验习惯不变：

- judges_obtaining = false
- judges_no_obstacle = true
- hope = false
- narrow_will = true
- bridge_holds_on_support = false

这个案例专门显示最小形式语义的欠规定处。若你认为“无障碍”的强含义已经包含足以获得的一切条件，就应加上$`O\Rightarrow G`$，排除该赋值。加了这一桥梁后可以证明狭义意志蕴涵希望；不要在解释时既不声明桥梁，又悄悄使用它。

## 6. 案例05：信念与事实各放一处

```python
Beliefs(
    worlds=WORLDS,
    support=frozenset(["success_clear"]),
    actual="failure_obstacle",
)
```

支持集是主体保留的情境，实际世界是另一个字段。于是希望、狭义意志都为true，但`actual_obtaining`和`actual_no_obstacle`都为false。

这不表示程序断言所有自信都错误。它只是允许错误，而不是一开始就强制实际世界在信念中。若已知实际世界确在支持集，针对G或O的全称判断就能实例化到实际世界；这是一个有前提的证明。

## 7. 案例06：不确定不等于判断失败

候选集同时包含成功且无障碍、失败且有障碍两个世界。两个全称判断都不成立，故希望与狭义意志都为false，即使实际世界后来是成功的。

这也不等于已经断言“不会得到”，更不能直接把结果叫作绝望或恐惧。本项目没有为这些原文列举但未展开的概念另设公式。

## 8. 案例07：经验来源标签不自动造出习惯

```python
JudgmentHabit(established=False, from_experience=True)
```

即使主体的候选集只有`success_clear`，经验来源标签为真也不等于习惯已经建立。结果希望为true、狭义意志为false。

反过来，仅有`established=True`而经验来源为false也不够。代码只核对两个注释条件，没有发明“两次成功就形成习惯”的学习规则。`experience_backed`不等于判断可靠或正当。

## 9. 案例08与09：激情可以暂停

案例08只有`desire_habit=True`，当前没有相应缺少、需要或欲望：

- passion_disposition = true
- passion_active = false

案例09把当前欲望的条件也设为真，两项便同时为true。两种状态都保留激情倾向；这是对原文“暂停后可被轻微契机再唤起”的最小表示。

模型没有声称任何线索必会使案例08变成案例09，也没有实现线索、强度或时间衰减。若需要这些内容，须另建有明示假设的动力模型。

## 10. 最后的小实验：删掉候选不等于改变现实

演示末尾先用两个候选世界，再只保留`success_clear`：

```python
before = Beliefs(
    WORLDS,
    frozenset(["success_clear", "failure_obstacle"]),
    "failure_obstacle",
)
after = before.restrict(frozenset(["success_clear"]))
```

输出`before_judges_obtaining=false`、`after_judges_obtaining=true`，而实际仍未获得。操作改变的是支持集，没有偷偷改变实际世界。这里只演示集合限制，不表示删去失败候选就是合理学习。

再把支持集清空会收到`belief support must be nonempty`。这个拒绝是有意的：不能借空集上的全称空真，让没有候选解释的主体自动拥有一切肯定判断。

## 11. 怎么检查，而不只看打印结果

```sh
python test_model.py
python -O test_model.py
python -OO test_model.py
python mutation_check.py
```

每个测试模式都执行27个测试方法，方法内部还包含明确的有限穷举。`unittest`检查不会被`-O`删除。变异检查在临时副本植入11个语义错误，应全被行为检查发现；一个实际语法错误对照必须归入`harness_failure`，不能计成检出。

全套命令与独立审计入口见[README](README.md)。模型的一般结论来自文字证明，有限试验负责检查代码是否实现这些定义。两者各有作用，不能相互冒充。
