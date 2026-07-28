# Strict Test Record

这份记录对应一次额外的三轮 loop。每轮检查不同的东西，避免只重复阅读同一段说明。

## Loop 1：功能契约

检查五种入口、默认粗糙度、三轮处理顺序、内容/格式双轴和事实保护。脚本结果：通过。

## Loop 2：边界与攻击性输入

检查 Markdown 围栏、链接、表格、敏感领域和随机乱码禁用规则。脚本结果：通过。

## Loop 3：真实场景回放

用五组固定材料回放 `draft`、`rewrite`、`repair`、`variant`、`notes-to-doc`，再加两组 Markdown 保护回归（`protected`、`safe`）。每组都有输入、输出和三轮处理记录。脚本结果：通过。

## 五组文档测试

| 编号 | 场景 | 重点 |
| --- | --- | --- |
| 01 | 直接生产初稿 | 从 2 条笔记生成带颗粒的 Markdown |
| 02 | 成稿重写 | 去套话但不改变判断 |
| 03 | 局部修正 | 范围外版本号、负责人、原话保持不变 |
| 04 | 同文档变体 | 换读者和场景，不只是换同义词 |
| 05 | 会议碎片整理 | 保留来源感，不补不存在的结论 |
| 06 | 受保护 Markdown | front matter、链接、脚注、Mermaid、LaTeX、任务项和步骤原样保留 |
| 07 | safe profile | 配置代码块、顺序和数值不变 |

运行：

```bash
./scripts/strict_audit.sh
```

预期输出：`RESULT: 3 audit loops, 5 core document cases, 2 protection regressions passed`
