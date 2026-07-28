# Research Notes

Human Grain 的基础做法参考了本地 `content-humanizer` skill 的三段式 Detect / Humanize / Voice Injection，以及公开仓库中常见的“AI tell 检测 + 结构重写”做法。

公开参考（访问日期：2026-07-28；以链接当前默认分支为准）：

| 来源 | 观察 | Human Grain 的取舍 | 许可/使用方式 |
| --- | --- | --- | --- |
| [humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | AI tell 检测、分数和多声音色 | 采用“先诊断再改写”，不采用分数承诺 | 公开仓库；未复制代码，仅引用工作流思路 |
| [humanizer-stack](https://github.com/NulightJens/humanizer-stack) | 表层 + 结构两阶段 | 改为三轮，并增加 Markdown 动作预算 | 公开仓库；未复制代码 |
| [humanizer-zh-next](https://github.com/Hyacehila/humanizer-zh-next) | 中文痕迹和中文场景 | 采用中文优先，补充安全错别字台账 | 公开仓库；未复制代码 |
| [LaTeXSnipper](https://github.com/SakuraMathcraft/LaTeXSnipper) | hero、示例、功能分区、快速开始 | 采用简洁首页骨架，减少装饰性 emoji | 仅参考公开 README 组织方式 |

Human Grain 在这些做法上增加了三点：格式动作预算、noise ledger、repair 的范围锁定。它不追求检测分数，也不承诺绕过任何平台检测。

本仓库没有复制这些项目的代码或大段文本；只借鉴公开描述的工作流思想。Human Grain 自己的实现以 MIT 发布，本地 `content-humanizer` 为 MIT，`tool-note-and-vote` 为 Apache-2.0；外部仓库的许可证以各自仓库当前声明为准，发布前不把其文件直接打包进本仓库。
