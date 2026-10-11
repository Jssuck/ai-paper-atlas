# 原创见证图的像素核验

2026-10-11实际执行make_diagram.py生成SVG，再用已安装的librsvg/cairo经Python标准库ctypes渲染1140×500PNG，并直接打开PNG逐面板检查。第一次渲染字体缓存目录警告未影响输出；以可写XDG_CACHE_HOME重跑后日志清洁，最终图亦重新看图。未安装第三方软件。

图示为原创教学重构，不复制原版十九配置。三个面板有相同U={a,b,c}、A={a}、B={a,b}，C依次为{b}、{c}、{b,c}。点成员资格、A/B/C轮廓和正文反模型一致；红色a始终属于B、不属于C，故O(B,C)始终真。三个C布局分别为全在B中、全在B外、部分在B中。仅标明的点是对象；面积和未标点区域不补出其他存在假设。

检查结果：标题、三面板、A/B/C标签、点标签与底部说明均完整；无裁切或文字重叠。首版左面板C标签贴近B轮廓，已右移再渲染复核。SVG和PNG显示相同内容；原图英文短标由正文中文图注解释。

运行命令（从附件目录）：

```sh
python3 qa/make_diagram.py
XDG_CACHE_HOME=/tmp/euler-civ-fontcache python3 qa/render_svg.py
```

第二条是可选图形QA，依赖系统已有librsvg-2.so.2、libcairo.so.2、libgobject-2.0.so.0；数学复现和测试只需Python标准库，不依赖这些图形库。图形运行日志见[diagram-run.log](../results/diagram-run.log)。

本记录只证明本地图像已实际检查，不冒称GitHub远端页面已验证；发布后的图像/公式/链接检查另行执行。
