<p align="center">
  <img src="assets/cover.png" alt="Human Grain editorial workspace" width="960">
</p>

<h1 align="center">Human Grain｜人间颗粒</h1>

<p align="center">
  <strong>A Markdown skill for work that still looks worked on.</strong><br>
  让文档像人在当时的条件下写出来的，不像统一模板。
</p>

Human Grain 是给 Codex / Claude Code 用的 Markdown skill。它处理 draft、rewrite、repair、variant 和 notes-to-doc：先保住事实和语法，再按原文体裁重排入口、删掉空话、留下真实的未决和协作入口。

它不靠随机错别字，也不保证绕过任何检测。技术文档仍然是技术文档，README 仍然要能安装，接口和数字不能被“人味”改坏。

## 怎么用

```bash
git clone git@github.com:ZhaoXingPeng/human-grain.git ~/.codex/skills/human-grain-writer
cd ~/.codex/skills/human-grain-writer
./scripts/check_skill.sh
```

然后在 Codex 或 Claude Code 中说：

```text
使用 $human-grain-writer，把这份 Markdown 改成体裁不变、结构更像真实工作稿的版本。最大力度重排，但保留接口、数字、链接和代码。
```

普通工作稿用 `standard`；明确要实验级粗糙时用 `extreme`。医疗、法律、财务、安全、代码、配置和公开承诺会降到 `safe`。

## 它怎样改

技能内部做三次检查，但用户默认只看到正文：

1. 抽事实锚点，删模板和重复背景。
2. 按读者动作重排，保留输入中已有的犹豫、失败、名字和协作请求。
3. 复核 Markdown 保护对象、事实、顺序和可继续编辑性。

“最大力度”意味着可以合并章节、删除大段背景、调换入口和把未决项前置；不意味着每篇都放引用块、TODO、错字或临时标题。

## 保护边界

- 不改事实、数字、因果、引用、接口、字段、代码、命令、链接、许可证和 front matter。
- 保护反引号/波浪号代码围栏、参考链接、脚注、图片 destination、HTML 注释、Mermaid/LaTeX、任务项、有序步骤和表格语法。
- 不伪造个人经历、来源、用户反馈、姓名或数据。
- `repair` 没给范围时先确认；范围外内容不顺手重写。

## 仓库结构

```text
SKILL.md                 核心触发和改写流程
references/              体裁、AI 味、粗糙度和 20 个早期样本的证据
examples/                前后对照和一次内部回放
tests/cases/              五种入口 + 两组保护回归 + 一组 extreme 结构回归
scripts/                 元数据、Markdown 和 AI-tell 检查
```

## 检查

```bash
./scripts/check_skill.sh
./scripts/strict_audit.sh
python3 scripts/validate_metadata.py
python3 scripts/validate_markdown.py
```

公开样本和审计笔记见 [`references/pre-2019-corpus.md`](references/pre-2019-corpus.md)。设计取舍见 [`DESIGN.md`](DESIGN.md)。

## 非目标

- 不规避学术、平台或安全审查。
- 不把错误拼写当作主要的人味机制。
- 不把一个作者的幽默和口头禅复制成全库模板。

MIT，见 [`LICENSE`](LICENSE)。
