# Strict Test Record

当前严格检查验证四件事：技能契约存在、20 个早期样本有审计记录、固定反模板话术不会进入 fixture、Markdown 保护对象在安全改写中不丢。另有一组 `extreme` 回归，专门检查继承来的章节骨架是否真的被拆掉。

七组 fixture 覆盖：

| 编号 | 场景 | 重点 |
| --- | --- | --- |
| 01 | 直接生产初稿 | 信息少时不补产品故事 |
| 02 | 成稿重写 | 结构和开头变化，不只换同义词 |
| 03 | 局部修正 | front matter、版本号、负责人和范围外原话不动 |
| 04 | 同文档变体 | 换读者入口，不增加能力或承诺 |
| 05 | 会议碎片整理 | 保留人名、建议和未决状态 |
| 06 | 受保护 Markdown | 参考链接、脚注、可变围栏、Mermaid、任务项和步骤原样保留 |
| 07 | safe profile | 配置代码块、顺序和数值不变 |
| 08 | extreme 结构 | 标题骨架减少，段落密度不再平均，未决信息保留 |

运行：

```bash
./scripts/check_skill.sh
./scripts/strict_audit.sh
python3 scripts/validate_metadata.py
python3 scripts/validate_markdown.py
```
