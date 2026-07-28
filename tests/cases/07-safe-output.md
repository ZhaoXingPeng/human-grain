模式：rewrite｜profile：safe｜粗糙度：1/5｜typo_noise=off

# 配置变更说明

这次只改配置，顺序和数值不动。

```yaml
timeout: 30
retries: 2
```

处理记录：第 1 轮删掉“标准化流程”套话，第 2 轮不补场景，第 3 轮保持代码块原样。
噪声台账：无。
格式台账：轮次 3｜no-op｜代码块和顺序｜safe profile 不改结构｜可回滚：是。
