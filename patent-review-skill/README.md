# Patent Review Skill

四阶段穿透式专利客体适格性审查工作流 —— 开源实现

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-green.svg)](requirements.txt)
[![Last Updated](https://img.shields.io/badge/last%20updated-2024-blue.svg)]()

## 项目简介

Patent Review Skill 是一个基于穿透式审查理念的专利客体适格性判断工具。它将专业审查员的审查经验转化为可执行的四阶段工作流，通过 AI 辅助与人工介入的结合，实现专利申请的快速、准确审查。

### 核心特性

- **四阶段审查流程**：初步筛查 → 深度审查 → 锚定验证 → 案例结论
- **量化分析模型**：L1-L5 数据含义层级 + G0-G4 领域关联度矩阵
- **丰富的知识库**：最新审查指南（2024）+ 权威案例库
- **灵活的扩展性**：模块化设计，支持自定义节点和工作流
- **人机协同**：AI 处理 + 人工复核，确保审查质量

## 功能架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Patent Review Skill                           │
├─────────────────────────────────────────────────────────────────┤
│  阶段一：初步穿透筛查                                              │
│  ├── 特征提取与标注                                                │
│  ├── 名实分离风险识别                                              │
│  ├── 数据含义初判                                                  │
│  ├── 问题性质初判                                                  │
│  └── 审查员复核（人工）                                            │
├─────────────────────────────────────────────────────────────────┤
│  阶段二：深度穿透审查                                              │
│  ├── 技术问题穿透（删除测试）                                       │
│  ├── 技术手段穿透（特定关联检索）                                    │
│  ├── 技术效果穿透（指标匹配）                                       │
│  ├── 闭环断层检测                                                  │
│  └── 疑点确认（人工）                                              │
├─────────────────────────────────────────────────────────────────┤
│  阶段三：锚定穿透验证                                              │
│  ├── 数据含义量化                                                  │
│  ├── 关联度量化                                                    │
│  ├── 综合矩阵判断                                                  │
│  └── 存疑分析（人工）                                              │
├─────────────────────────────────────────────────────────────────┤
│  阶段四：案例穿透与结论生成                                        │
│  ├── 类案匹配                                                      │
│  ├── 比对分析                                                      │
│  ├── 意见生成                                                      │
│  └── 最终审核（人工）                                              │
└─────────────────────────────────────────────────────────────────┘
```

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-org/patent-review-skill.git
cd patent-review-skill

# 安装依赖
pip install -r requirements.txt

# 验证安装
python -m pytest tests/
```

### 基本使用

#### 1. 案例匹配

```bash
# 根据技术特征检索相似案例
python scripts/case_matcher.py --features "深度学习,神经网络,硬件效率" --format text
```

#### 2. 工作流执行

```python
from workflow.patent_workflow import PatentReviewWorkflow

# 初始化工作流
workflow = PatentReviewWorkflow()

# 执行审查
result = workflow.execute(
    patent_application="path/to/patent_application.pdf",
    stage="all"  # 或 "stage1", "stage2", "stage3", "stage4"
)

# 输出结果
print(result)
```

## 项目结构

```
patent-review-skill/
├── README.md                      # 项目说明
├── LICENSE                        # MIT 许可证
├── requirements.txt               # Python 依赖
├── docs/                          # 详细文档
│   ├── GETTING_STARTED.md        # 快速入门
│   ├── WORKFLOW_GUIDE.md         # 工作流指南
│   ├── API_REFERENCE.md          # API 参考
│   └── EXAMPLES.md               # 使用示例
├── patent-workflow/               # 主 Skill 目录
│   ├── SKILL.md                  # Skill 入口
│   ├── workflow/                 # 工作流定义
│   │   ├── patent-review-workflow.json  # 工作流配置
│   │   ├── node-prompts.md       # 节点 Prompt 库
│   │   ├── workflow-guide.md     # 工作流说明
│   │   ├── keyword-libraries.json # 关键词库
│   │   └── knowledge/            # 知识库
│   │       ├── patent-law-basis.md    # 法律依据
│   │       └── case-database.md        # 案例库
│   └── scripts/                   # 工具脚本
│       └── case_matcher.py        # 案例匹配脚本
└── tests/                         # 测试用例
    ├── test_workflow.py
    └── test_case_matcher.py
```

## 量化分析模型

### L1-L5 数据含义层级

| 层级 | 名称 | 描述 | 示例 |
|------|------|------|------|
| L1 | 原始观测数据 | 传感器读数、用户输入 | 温度传感器数据 |
| L2 | 预处理数据 | 清洗、标准化后的数据 | 去噪后的信号 |
| L3 | 提取特征 | 统计量、频域特征 | 均值、方差 |
| L4 | 模型输出 | 预测值、分类结果 | 置信度分数 |
| L5 | 决策/控制 | 基于输出的动作 | 控制指令 |

### G0-G4 领域关联度

| 梯度 | 名称 | 描述 | 示例 |
|------|------|------|------|
| G0 | 领域无关 | 通用数学/逻辑 | 排序算法 |
| G1 | 弱关联 | 跨领域通用方法 | 通用优化算法 |
| G2 | 中等关联 | 某技术领域通用 | 图像处理算法 |
| G3 | 强关联 | 特定应用领域 | 医学影像分析 |
| G4 | 极强关联 | 具体产品/场景专用 | 特定设备参数 |

### L×G 判断矩阵

| L×G 组合 | 判断 | 说明 |
|----------|------|------|
| L4 且 G3+ | 锚定成功 | 具备技术属性 |
| L3 且 G2- | 锚定失败 | 不具备技术属性 |
| 其他 | 存疑 | 需人工分析 |

## 知识库

### 法律依据

- 《专利法》第2条第2款（技术方案定义）
- 《专利法》第25条第1款第(二)项（智力活动规则除外）
- 《专利审查指南（2024）》第二部分第九章
- 最高人民法院知识产权法庭裁判要旨

### 权威案例库

| 类型 | 数量 | 来源 |
|------|------|------|
| 授权案例 | 6个 | 审查指南官方示例 |
| 不授权案例 | 4个 | 审查实践典型 |
| 边界案例 | 2个 | 审查实践总结 |

详见 [docs/KNOWLEDGE_BASE.md](docs/KNOWLEDGE_BASE.md)

## 文档

- [快速入门](docs/GETTING_STARTED.md)
- [工作流使用指南](docs/WORKFLOW_GUIDE.md)
- [API 参考](docs/API_REFERENCE.md)
- [使用示例](docs/EXAMPLES.md)
- [常见问题](docs/FAQ.md)

## 贡献

欢迎提交 Issue 和 Pull Request！

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

本项目基于以下开源项目和技术：

- [Patent Examination Guidelines (2024)](https://www.cnipa.gov.cn)
- 最高人民法院知识产权法庭案例库

## 联系方式

- GitHub Issues: [https://github.com/your-org/patent-review-skill/issues](https://github.com/your-org/patent-review-skill/issues)
- Email: contact@example.com
