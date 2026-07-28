---
title: 受保护 Markdown
---

修正范围：只改第一段的语气。

这份说明先写得像工作稿，但结构不动。

[普通链接](https://example.com/docs) 和 [参考链接][docs]。

[docs]: https://example.com/reference

脚注内容[^one]要保留。

[^one]: 这是脚注定义。

<!-- keep this comment -->

~~~~mermaid
flowchart LR
  A --> B
~~~~

````python
print("keep")
````

```math
x^2 + y^2 = z^2
```

- [ ] 待确认
1. 第一步
2. 第二步
