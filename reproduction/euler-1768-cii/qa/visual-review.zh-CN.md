# 严格交叠图视觉验收

验收日：2026-10-10。输入为本项目原创生成的 `results/strict-overlap.svg`，不是原书图的扫描件。

## 实际执行

最初尝试 ImageMagick 默认 SVG 及 MSVG 路径均失败，原因是该安装调用的 `rsvg-convert` 可执行文件不存在。两次失败原样保留在 `logs/svg-render.log` 与 `logs/svg-render-fallback.log`；未把这些尝试记成成功。

实际成功路径：通过 Python 标准库 ctypes 调用已经安装的 `librsvg-2.so.2` 与 `libcairo.so.2`，生成900×500像素PNG。

```sh
XDG_CACHE_HOME=/tmp/euler-cii-font-cache python3 qa/render_svg.py
```

成功输出及退出码在 `logs/svg-render-success.log`。这些系统库仅用于可选的图像验收，不是 `python3 run.py` 的运行依赖；未安装任何新包。

## 看图核对

已实际打开 `results/strict-overlap.png`，核对：

- 三个点分别落在 S 独有区、交集、P 独有区，编号为1、0、2，与 JSON 模型相符。
- 右侧 S={0,1}、P={0,2} 及 A/E 假、I/O 真正确。
- 明示论域只有三个标出点，几何圆内的连续点不作对象计数。
- 明示 P 独有区非空是图示的额外条件，不是 I/O 的共同要求。
- 中文完整可读，无缺字方框；标题、圆、标签、说明均未截断或互相遮挡。

验收结论：图的语义与排版均通过。本记录是人工式视觉核对，独立代码审查另见 `review/`。
