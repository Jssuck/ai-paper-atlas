# III.7 独立技术审查

结论：通过。审查对象为[正文](../../papers/ancient/euclid-elements-iii7.zh-CN.md)与本目录精确有理教学实现；不是古典系统的形式化认证。

## 版本绑定

- 正文 SHA256：`c5f2db7a0c7373d06ad10a396624eb438132132f652538eb024a8b210f64619b`
- geometry.py SHA256：`7fc50ab38b3f56ae4f6177d526ffa6d3e1915024ac0266a58f42edba81ebfe27`
- 审查日期：2026-10-29。

## 论证核验

1. 最长/最短两处I.20均要求非退化三角形，正文将轴端点另列。E—F—D及0<d<r保证减去EF后得到正FD；d=0退化已排除。
2. 独立重算F处角α的导数：分子(r cosθ−d)r cosθ−r sinθ(−r sinθ)=r²−rd cosθ，分母为FP²且不为零。r>d>0令导数严格正。α在上半圆连续而不跨分支，故角序桥步有效；相对FA角为π−α的反向也正确。正文明确现代微积分重构，并未冒充原文。
3. 伙伴存在使用反射/SAS，至多性分别覆盖G侧、H侧及轴端点。非极值才有两个不同点；中心等距无限、极值唯一，范围外无解的区别保留。
4. 平方距离余量、固定q解x及y²分类核算正确。例r=5、d=2的9、17、29、41、49及余量8、32正确；q=5的±√24确实超出有理坐标域。平方比较使用非负长度，不混用负长度。

## 实现与独立运行

实读geometry.py、test_geometry.py、Notebook生成/回放器及图源码。证书使用Fraction，拒绝bool/float等非法标量；验证器重新计算规范JSON，数值1不能伪装布尔true，附加/缺失/篡改字段不能混过比较。compare要求两个不同点位于同一开半圆。circle_point只是参数生成器，不声称通用求交或求所有距离根。

审查者独立执行以下命令，均真实返回0：

```sh
python3 -m unittest -v
python3 -O -m unittest -v
python3 -OO -m unittest -v
python3 verify_notebook.py --read-only
python3 independent_review_checks.py
```

前三次各24项测试通过，网格各504构形。Notebook五格输出与保存值逐字相同，execution_count为null；属于标准库compile/exec顺序回放，不是Jupyter kernel。未据此宣称一般定理获得机器证明。

另写[独立检查代码](independent_review_checks.py)，不使用证书中的距离计算结果作为预期值：从坐标重新算镜像的圆周方程、两点到F的距离、两项余量，并检查两种轴方向下19点的两两排序。实际504个反射/余量实例及342个同半圆点对通过，见[真实输出](logs/independent-review.log)。这些仍是有限检查，不能替代正文证明。

## 图与修订

实际查看本地SVG渲染图：同尺度圆、O/F位置、近远端、镜像P/H、9<17<49标注正确，无标签截断或遮挡。图像不是历史原图；GitHub远端实际渲染须由发布后核验另行确认。

初稿练习10把样本数写成“六百”，已改为504，正文补充24×3及五格实际统计；核对修订后与日志一致。本审查未发现其他阻止发布的技术问题。独立来源审查另见对应报告，不能由本技术审查代替。
