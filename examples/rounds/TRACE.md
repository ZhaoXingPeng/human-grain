# Canonical Three-round Trace

这是一个手工回放的 golden trace，不是假装某个 API 自动产出的日志。它把一次完整运行拆成四个可读文件，方便在换模型后复核：输入、Round 1、Round 2、Round 3。

| 阶段 | 输入/输出 | 检查 |
| --- | --- | --- |
| Round 1 | `01-round-1-strip.md` | AI-tell 命中减少，事实方向保留 |
| Round 2 | `01-round-2-friction.md` | 场景只来自输入，出现人的判断和停顿 |
| Round 3 | `01-round-3-grain.md` | 格式动作有位置/目的/回滚字段，噪声有台账 |

Round-3 参数：`profile=standard`，`typo_noise=on`（仅因为本例明确演示可回滚错别字）。

最终回归：Markdown 可解析；没有代码、链接、数字或关键字段；三轮没有新增来源或个人经历。
