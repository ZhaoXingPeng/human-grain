# Asset Provenance

README 的视觉方向是“编辑工作台”：深炭黑 `#0d0f0e`、灰白 `#f4f1e8`、荧光绿 `#b8f04a`、橙红 `#ff6b4a`、冷蓝 `#8fb8ff`。hero、前后对照和流程图先按本地 `frontend-design`、`ui-design-system`、`imagegen` 规则设计，再保留 SVG 源和 PNG 预览。

## Generated transparent cutout

`paper-transparent.png` 是一次公开图像生成回退的结果：

- Endpoint：`https://image.pollinations.ai/prompt/...`
- Prompt：isolated off-white Markdown paper, lime highlight, flat magenta background, no desk or extra objects
- Post-process：本地 `remove_chroma_key.py` 去背景，再用几何 mask 只保留纸张主体
- 输出：510×655 RGBA，透明背景

这张图只作为 README 的小型透明主体，不承担 hero 背景。生成源文件放在被 `.gitignore` 忽略的 `assets/generated/`，避免把带背景的实验图混入正式素材。

项目根目录 `生图.txt` 中的接口也曾尝试调用，但返回 `missing api key` 并发生超时；没有把密钥写进脚本、日志或 Git 历史。接口恢复并提供有效凭证后，可以替换同名 PNG。

## Vector-to-raster assets

当前正式素材：

| 文件 | 尺寸 | 用途 |
| --- | ---: | --- |
| `cover.png` | 1600×900 | README hero |
| `compare.png` | 1600×650 | before/after 解释图 |
| `three-rounds.png` | 1600×360 | 三轮流程图 |
| `paper-transparent.png` | 510×655 RGBA | 透明主体小图 |

脱敏 prompts（接口恢复后可重试）：

```text
Minimal premium editorial raster cover for Human Grain, an open-source Markdown writing skill: a marked-up paper sheet on a charcoal field, fluorescent green correction line, small orange mark, no text, no logo, wide composition.
```

```text
Editorial before-and-after comparison for a Markdown writing tool: left side rigid uniform gray text bars, right side a dark document with uneven short lines, a lime highlight, a small coral TODO note, no logo, no extra decoration.
```

```text
Minimal dark editorial process diagram for Human Grain: three connected stages labeled STRIP, FRICTION, GRAIN, coral blue and lime blocks, thin rules, no gradients, no logo.
```

本地 SVG 栅格化命令（macOS）：

```bash
mkdir -p /tmp/human-grain-preview
qlmanage -t -s 1600 -o /tmp/human-grain-preview assets/cover.svg assets/three-rounds.svg assets/compare.svg
sips --cropToHeightWidth 900 1600 --cropOffset 350 0 /tmp/human-grain-preview/cover.svg.png --out assets/cover.png
sips --cropToHeightWidth 360 1600 --cropOffset 620 0 /tmp/human-grain-preview/three-rounds.svg.png --out assets/three-rounds.png
sips --cropToHeightWidth 650 1600 --cropOffset 475 0 /tmp/human-grain-preview/compare.svg.png --out assets/compare.png
```
