# 专利客体适格性审查工作流使用指南

## 概述

本工作流将专利客体适格性审查的"穿透式审查"理念，编排为四阶段可视化工作流。本指南说明工作流的结构、节点配置和使用方法。

## 工作流架构

```
工作流ID: patent-eligibility-review
版本: 1.0.0
阶段数: 4
节点总数: 18 (含5个人工干预节点)
```

## 阶段总览

| 阶段 | 名称 | AI节点 | 人工节点 | 退出条件 |
|------|------|--------|----------|----------|
| 阶段一 | 初步穿透筛查 | 5 | 1 | 低风险结案/进入阶段二 |
| 阶段二 | 深度穿透审查 | 5 | 1 | 不授权终止/进入阶段三 |
| 阶段三 | 锚定穿透验证 | 4 | 1 | 失败终止/进入阶段四 |
| 阶段四 | 案例穿透与结论生成 | 3 | 1 | 工作流结束 |

## 节点详解

### 阶段一节点

| 节点ID | 节点名称 | 类型 | 输入 | 输出 |
|--------|----------|------|------|------|
| stage1_node1 | 特征提取与标注 | AI | patent_application, claims | feature_list |
| stage1_node2 | 名实分离风险识别 | AI | feature_list, claims | name_real_separation_risks |
| stage1_node3 | 数据含义初判 | AI | patent_application, feature_list | data_level_initial |
| stage1_node4 | 问题性质初判 | AI | patent_application | problem_nature |
| stage1_node5 | 风险报告生成 | AI | 阶段一中间结果 | screening_report, risk_level |
| stage1_node6 | 审查员复核 | 人工 | screening_report | reviewer_decision_stage1 |

### 阶段二节点

| 节点ID | 节点名称 | 类型 | 输入 | 输出 |
|--------|----------|------|------|------|
| stage2_node1 | 技术问题穿透-删除测试 | AI | screening_report, patent_application | deletion_test_result |
| stage2_node2 | 技术手段穿透-特定关联检索 | AI | patent_application | tech_correlation_signals |
| stage2_node3 | 技术效果穿透-指标匹配 | AI | patent_application | effect_indicators |
| stage2_node4 | 闭环断层检测 | AI | 阶段二中间结果 | triple_element_graph |
| stage2_node5 | 三要素报告生成 | AI | 阶段二中间结果 | triple_element_report, element_tech_attr |
| stage2_node6 | 疑点确认 | 人工 | triple_element_report | reviewer_decision_stage2 |

### 阶段三节点

| 节点ID | 节点名称 | 类型 | 输入 | 输出 |
|--------|----------|------|------|------|
| stage3_node1 | 数据含义量化 | AI | triple_element_report | data_level_quantified |
| stage3_node2 | 关联度量化 | AI | triple_element_report, tech_correlation_signals | domain_correlation_quantified |
| stage3_node3 | 综合矩阵判断 | AI | data_level_quantified, domain_correlation_quantified | matrix_result |
| stage3_node4 | 验证报告生成 | AI | 阶段三中间结果 | verification_report, anchor_result |
| stage3_node5 | 存疑分析 | 人工 | verification_report, anchor_result | reviewer_decision_stage3 |

### 阶段四节点

| 节点ID | 节点名称 | 类型 | 输入 | 输出 |
|--------|----------|------|------|------|
| stage4_node1 | 类案匹配 | AI | triple_element_report, verification_report | similar_cases |
| stage4_node2 | 比对分析 | AI | similar_cases, triple_element_report, verification_report | comparison_table |
| stage4_node3 | 意见生成 | AI | 比对分析结果 | final_opinion, final_decision |
| stage4_node4 | 最终审核 | 人工 | final_opinion | reviewer_final_decision |

## 变量流转

### 阶段一 → 阶段二

```
screening_report → triple_element_report (部分引用)
risk_level → 决定是否进入阶段二
```

### 阶段二 → 阶段三

```
triple_element_report → 锚定验证输入
element_tech_attr → 决定是否进入阶段三
```

### 阶段三 → 阶段四

```
verification_report → 类案匹配输入
anchor_result → 决定是否进入阶段四
```

## 人工干预节点配置

### 节点1.6: 审查员复核

- **操作类型**: approve_or_reject
- **选项**:
  - 通过-进入下一阶段
  - 通过-结案(低风险)
  - 驳回-补充材料
  - 终止-不符合条件

### 节点2.6: 疑点确认

- **操作类型**: confirm
- **选项**:
  - 确认三要素具备技术属性
  - 确认任一要素非技术-终止
  - 存疑-继续分析

### 节点3.5: 存疑分析

- **操作类型**: decision
- **选项**:
  - 锚定成功-进入下一阶段
  - 锚定失败-终止

### 节点4.4: 最终审核

- **操作类型**: approve_or_edit
- **选项**:
  - 确认发出
  - 修改后发出
  - 驳回重写

## 工作流执行策略

### 策略一：全流程执行

适用场景：全面审查

```
阶段一 → 阶段二 → 阶段三 → 阶段四 → 结束
```

### 策略二：快速筛查

适用场景：初步筛查，快速判断

```
阶段一(全节点) → 结案/进入阶段二
```

### 策略三：聚焦审查

适用场景：已有初步结论，进一步验证

```
阶段二 → 阶段三 → 阶段四 → 结束
```

### 策略四：仅结论生成

适用场景：已有完整分析，仅需生成结论

```
阶段四 → 结束
```

## 平台导入说明

### JSON Schema验证

```bash
python -c "
import json
schema = json.load(open('workflow/patent-review-workflow.json'))
# 验证结构
required_keys = ['workflow', 'id', 'name', 'stages']
for key in required_keys:
    assert key in schema, f'Missing key: {key}'
print('Schema validation passed')
"
```

### 平台兼容性

工作流定义遵循标准JSON格式，可导入以下平台：
- 自研工作流平台
- Flowise
- LangFlow
- n8n
- 其他支持JSON定义的可视化工作流平台

### 图形化展示建议

| 节点类型 | 颜色建议 | 形状建议 |
|----------|----------|----------|
| AI处理节点 | 蓝色 | 圆角矩形 |
| 人工干预节点 | 橙色 | 菱形 |
| 阶段边界 | 灰色 | 虚线框 |
| 流程线 | 绿色(通过)/红色(拒绝) | 实线箭头 |

## 关键词库使用

关键词库位于 `keyword-libraries.json`，包含：

- 算法问题关键词
- 商业规则关键词
- 技术问题关键词
- 算法效果指标
- 技术效果指标

在节点执行时，AI会自动使用这些关键词库进行模式匹配。

## 常见问题

### Q: 人工节点可以跳过吗？

A: 不可以。人工干预节点必须由审查员操作，这是强制要求。

### Q: 阶段可以单独执行吗？

A: 可以，但需要确保前置变量已正确设置。

### Q: 决策变量如何设置？

A: 决策变量由AI节点生成，审查员可在人工节点中修改。

### Q: 如何处理存疑情形？

A: 在存疑分析节点，审查员需做出最终决策，选择进入下一阶段或终止。

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0.0 | 2024-01-01 | 初始版本 |
