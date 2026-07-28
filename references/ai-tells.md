# AI-tell checklist

第 1 轮先做诊断，不直接重写。这个词表是提示器，不是禁词表；专业语境里确实需要的词不能为了分数被删掉。

## 中文信号

`在……背景下`、`旨在`、`全面提升`、`高效闭环`、`赋能`、`打造`、`值得注意的是`、`综上所述`、`从而`、`此外`、`需要指出的是`、`多维度`、`系统化`、`标准化流程`。

## English signals

`delve`、`leverage`、`furthermore`、`moreover`、`crucial`、`robust`、`holistic`、`in conclusion`、`it is important to note`、`navigate the landscape`。

## 结构信号

- 每段都严格“观点 → 解释 → 例子 → 总结”。
- 连续句子长度接近，连接词密度过高。
- 开头和结尾重复同一个摘要。
- 没有具体的人、动作、时间或未决点。
- 过度平衡，不做选择，只列优点。

## 不能误删

代码、API 字段、法律/医疗术语、引用原文、产品名称和用户明确要求保留的词不参与机械替换。诊断报告应列出命中位置，供主模型判断。

## Round-1 输出

```text
AI tell report
- filler: 2
- hedging: 1
- uniform paragraphs: medium
- vague claims: 1
decision: strip 3 phrases; preserve 2 domain terms
```
