---
name: patent-review-skill
description: 专利客体适格性四阶段穿透式审查工作流；将筛查、深度审查、锚定验证、案例结论编排为可视化节点；内置自我进化机制持续完善审查能力
dependency:
  python:
    - pytest>=7.0.0
---

# 专利客体适格性审查技能

## 概述

本技能提供完整的专利客体适格性审查能力，通过四阶段穿透式审查工作流，帮助审查员准确判断专利申请是否构成《专利法》意义上的"技术方案"。

**内置自我进化机制**：通过用户反馈和定期追踪最新审查案例，持续完善审查能力，确保与最新法律标准和审查实践保持同步。

## 核心能力

| 能力 | 说明 |
|------|------|
| 四阶段审查 | 初步筛查 -> 深度审查 -> 锚定验证 -> 案例结论 |
| 人工介入 | 4个人工干预节点，确保审查质量 |
| 量化锚定 | L1-L5数据含义层级 + G0-G4领域关联度模型 |
| 案例匹配 | 权威案例库 + 智能匹配算法 |
| **自我进化** | 用户反馈驱动 + 定期追踪 + 第一性原理验证 |

## 目录结构

```
patent-review-skill/
├── SKILL.md                           # 本文件
├── patent-workflow/                   # 工作流核心
│   ├── workflow/                      # 工作流配置
│   │   ├── patent-review-workflow.json
│   │   ├── node-prompts.md
│   │   ├── keyword-libraries.json
│   │   └── knowledge/
│   │       ├── patent-law-basis.md    # 法律依据
│   │       └── case-database.md      # 案例库
│   └── scripts/
│       └── case_matcher.py            # 案例匹配脚本
├── evolution/                         # 自我进化模块
│   ├── EVOLUTION_GUIDE.md            # 进化机制指南
│   ├── evolution_engine.py           # 进化引擎
│   ├── feedback_collector.py         # 反馈收集器
│   ├── case_tracker.py               # 案例追踪器
│   ├── knowledge_updater.py          # 知识更新器
│   ├── version_manager.py            # 版本管理器
│   └── config.py                     # 进化配置
├── validation/                        # 验证模块
│   ├── test_knowledge_update.py      # 知识更新测试
│   └── regression_tests.py           # 回归测试
└── docs/                             # 文档
```

## 快速开始

### 基本使用

```bash
# 使用案例匹配
python patent-workflow/scripts/case_matcher.py --features "深度学习,神经网络,硬件效率"

# 查看工作流结构
cat patent-workflow/workflow/patent-review-workflow.json
```

### 自我进化操作

```bash
# 提交用户反馈
python evolution/feedback_collector.py submit \
  --type case_addition \
  --content "新增案例描述"

# 触发进化流程
python evolution/evolution_engine.py run

# 检查最新案例
python evolution/case_tracker.py update

# 查看版本历史
python evolution/version_manager.py list

# 运行回归测试
python -m pytest validation/ -v
```

## 第一性原理

所有审查判断和知识更新必须从专利法核心定义出发：

> **专利法第二条第二款**：技术方案是对要解决的技术问题所采取的技术手段构成了技术特征，并且能够产生相应的技术效果。

**三要素标准**：
1. **技术问题**：利用自然规律解决技术问题
2. **技术手段**：与技术特征功能上相互支持
3. **技术效果**：获得符合自然规律的技术效果

## 自我进化机制

### 进化原则

1. **第一性原理约束**：所有更新必须符合专利法第二条技术方案定义
2. **严格流程**：反馈收集 -> 分类验证 -> 知识更新 -> 版本发布
3. **验证测试**：每次更新后自动运行单元测试和回归测试
4. **版本管理**：完整的版本控制和回滚机制

### 进化流程

```
用户反馈/最新案例
       ↓
   反馈收集器 ←→ 案例追踪器
       ↓
  第一性原理验证
       ↓
   知识更新器
       ↓
   验证测试
       ↓
   版本管理器
       ↓
   发布新版本
```

### 反馈类型

| 类型 | 优先级 | 说明 |
|------|--------|------|
| 规则修正 | P0 | 审查标准错误 |
| 错误纠正 | P0 | 事实性错误 |
| 案例补充 | P1 | 缺失重要案例 |
| 边界澄清 | P2 | 边界案例说明 |
| 体验改进 | P3 | 流程优化建议 |

## 案例匹配

### 内置案例库

| 类型 | 数量 | 说明 |
|------|------|------|
| 授权案例 | 6+ | 审查指南官方示例 |
| 不授权案例 | 4+ | 审查实践典型 |
| 边界案例 | 2+ | 边界情况分析 |

### 使用示例

```bash
# 检索相似案例
python patent-workflow/scripts/case_matcher.py \
  --features "图像处理,深度学习,分类" \
  --format text

# JSON格式输出
python patent-workflow/scripts/case_matcher.py \
  --features "内存优化,训练速度" \
  --format json
```

## 版本管理

```bash
# 查看当前版本
python evolution/version_manager.py current

# 列出所有版本
python evolution/version_manager.py list

# 回滚到指定版本
python evolution/version_manager.py rollback --version v1.0.0

# 发布新版本
python evolution/version_manager.py release --version v1.2.0
```

## 测试验证

```bash
# 运行知识更新测试
python validation/test_knowledge_update.py

# 运行回归测试
python validation/regression_tests.py

# 运行完整验证
python -m pytest validation/ -v
```

## 参考文档

- [工作流指南](docs/WORKFLOW_GUIDE.md)
- [API参考](docs/API_REFERENCE.md)
- [使用示例](docs/EXAMPLES.md)
- [常见问题](docs/FAQ.md)
- [进化机制指南](evolution/EVOLUTION_GUIDE.md)
- [法律依据](patent-workflow/workflow/knowledge/patent-law-basis.md)
- [案例数据库](patent-workflow/workflow/knowledge/case-database.md)
