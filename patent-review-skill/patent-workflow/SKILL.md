---
name: patent-workflow
description: 专利客体适格性四阶段穿透式审查工作流；将筛查、深度审查、锚定验证、案例结论编排为可视化节点；适用于审查员与AI协同的专利审查场景
dependency:
  python:
    - json
---

# 专利客体适格性审查工作流

## 概述

本工作流将专利客体适格性审查的"穿透式审查"理念，编排为四阶段可视化工作流，支持平台图形化展示和执行。

**设计原则**：
- 每个阶段独立成节点组，支持单独执行
- AI处理节点与人工干预节点明确区分
- 节点间通过标准变量传递数据
- 支持条件分支和审批流程

## 工作流结构

```
阶段一：初步穿透筛查
├── 1.1 特征提取与标注 (AI)
├── 1.2 名实分离风险识别 (AI)
├── 1.3 数据含义初判 (AI)
├── 1.4 问题性质初判 (AI)
├── 1.5 风险报告生成 (AI)
└── 1.6 审查员复核 (人工) ──[低风险]──→ 结案
            │
            └──[中高风险]──→ 阶段二

阶段二：深度穿透审查
├── 2.1 技术问题穿透-删除测试 (AI)
├── 2.2 技术手段穿透-特定关联检索 (AI)
├── 2.3 技术效果穿透-指标匹配 (AI)
├── 2.4 闭环断层检测 (AI)
├── 2.5 三要素报告生成 (AI)
└── 2.6 疑点确认 (人工) ──[不授权]──→ 结案
            │
            └──[存疑/授权]──→ 阶段三

阶段三：锚定穿透验证
├── 3.1 数据含义量化 (AI)
├── 3.2 关联度量化 (AI)
├── 3.3 综合矩阵判断 (AI)
├── 3.4 验证报告生成 (AI)
└── 3.5 存疑分析 (人工) ──[失败]──→ 结案
            │
            └──[成功]──→ 阶段四

阶段四：案例穿透与结论生成
├── 4.1 类案匹配 (AI)
├── 4.2 比对分析 (AI)
├── 4.3 意见生成 (AI)
└── 4.4 最终审核 (人工) ──→ 审查意见通知书
```

## 节点类型说明

| 类型 | 标识 | 说明 |
|------|------|------|
| AI处理节点 | `ai_process` | 执行大模型任务，自动处理 |
| 人工干预节点 | `human_review` | 审查员复核、审批、决策 |

## 变量规范

### 全局变量

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `patent_application` | Object | 专利申请文件全文 |
| `claims` | Array | 权利要求列表 |
| `specification` | String | 说明书内容 |
| `drawings` | Array | 附图描述 |

### 阶段间变量

| 变量名 | 类型 | 来源 | 目标 |
|--------|------|------|------|
| `screening_report` | Object | 阶段一 | 阶段二 |
| `triple_element_report` | Object | 阶段二 | 阶段三 |
| `verification_report` | Object | 阶段三 | 阶段四 |
| `case_matching_result` | Object | 阶段四 | - |
| `final_opinion` | Object | 阶段四 | - |

### 决策变量

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `risk_level` | Enum | 低/中/高 |
| `element_tech_attr` | Boolean | 三要素是否具备技术属性 |
| `anchor_result` | Enum | 成功/失败/存疑 |
| `final_decision` | Enum | 授权/不授权/待定 |

## 资源索引

- 工作流定义：[workflow/patent-review-workflow.json](workflow/patent-review-workflow.json)
- 节点Prompt库：[workflow/node-prompts.md](workflow/node-prompts.md)
- 法律依据：[workflow/knowledge/patent-law-basis.md](workflow/knowledge/patent-law-basis.md)
- 案例库：[workflow/knowledge/case-database.md](workflow/knowledge/case-database.md)
- 关键词库：[workflow/keyword-libraries.json](workflow/keyword-libraries.json)
- 案例匹配脚本：[scripts/case_matcher.py](scripts/case_matcher.py)

## 知识库说明

### 法律依据库（patent-law-basis.md）

包含最新审查指南核心条款：
- 专利法第二条第二款（技术方案定义）
- 专利法第二十五条（不授权客体）
- 专利审查指南（2024）第二部分第九章
- 最高法知产法庭裁判要旨（2023）

### 权威案例库（case-database.md）

收录官方审查示例和典型案例：

**授权案例（6个）**：
- 深度神经网络训练方法（审查示例5）
- 电子券使用倾向度分析（审查示例6）
- 知识图谱推理方法（审查示例7）
- 去除图像噪声方法
- 物流配送方法（审查示例13）
- 适配神经网络参数方法（审查示例15）

**不授权案例（4个）**：
- 金融产品价格预测方法（审查示例10）
- 抽象算法
- 游戏规则/玩法
- 商业返利规则

### 案例匹配使用

```bash
# 根据技术特征检索相似案例
python scripts/case_matcher.py --features "深度学习,神经网络,硬件效率" --format text

# JSON格式输出
python scripts/case_matcher.py --features "图像处理,噪声去除" --format json
```
- 工作流使用指南：[workflow/workflow-guide.md](workflow/workflow-guide.md)
- 关键词库：[workflow/keyword-libraries.json](workflow/keyword-libraries.json)

## 使用方式

### 平台可视化

将 `patent-review-workflow.json` 导入工作流平台，即可在图形编辑器中查看和编辑工作流。

### 独立执行

可按阶段单独执行：
1. 仅执行阶段一 → 快速筛查
2. 执行阶段一二 → 中等深度审查
3. 完整执行 → 全流程审查

### 快速开始

```bash
# 查看工作流结构
cat workflow/patent-review-workflow.json | python -m json.tool

# 验证JSON结构
python -c "import json; json.load(open('workflow/patent-review-workflow.json'))"
```

## 注意事项

- 人工干预节点必须由审查员操作，AI无法自动跳过
- 决策变量决定工作流走向，必须正确设置
- 各阶段的Prompt已针对专利审查场景优化
- 关键词库需定期更新以保持准确性
