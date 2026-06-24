# 快速入门指南

## 环境准备

### 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- 4GB+ RAM（推荐）

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/patent-review-skill.git
cd patent-review-skill

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 验证安装
python -c "from workflow.patent_workflow import PatentReviewWorkflow; print('OK')"
```

## 快速开始

### 方式一：使用命令行工具

#### 案例匹配

```bash
# 基本用法
python scripts/case_matcher.py --features "深度学习,神经网络"

# 指定输出格式
python scripts/case_matcher.py --features "图像处理,分类" --format json

# 限制返回数量
python scripts/case_matcher.py --features "算法优化" --limit 5 --format text
```

#### 参数说明

| 参数 | 必选 | 说明 | 示例 |
|------|------|------|------|
| `--features` | 是 | 技术特征（逗号分隔） | "深度学习,分类" |
| `--format` | 否 | 输出格式：text/json | text |
| `--limit` | 否 | 返回结果数量 | 5 |

### 方式二：Python API

```python
from workflow.patent_workflow import PatentReviewWorkflow

# 初始化工作流
workflow = PatentReviewWorkflow()

# 执行完整审查
result = workflow.execute(
    patent_application="./sample_case.pdf",
    stage="all"
)

print(result)

# 执行特定阶段
result = workflow.execute(
    patent_application="./sample_case.pdf",
    stage="stage1"  # 或 "stage2", "stage3", "stage4"
)
```

## 示例输出

### 案例匹配输出示例

```json
{
  "query": "深度学习,神经网络",
  "total_cases": 12,
  "returned": 3,
  "cases": [
    {
      "id": "case_001",
      "type": "授权",
      "title": "深度神经网络模型的训练方法",
      "similarity": 0.92,
      "source": "审查指南示例5"
    }
  ]
}
```

### 审查结果输出示例

```json
{
  "case_id": "2024-001",
  "stage": "stage1",
  "result": {
    "risk_level": "高",
    "risk_points": [
      {
        "type": "名实分离",
        "severity": "高",
        "description": "技术特征仅为算法规则的通用运行载体"
      }
    ]
  },
  "recommendation": "进入阶段二深度审查"
}
```

## 目录结构说明

```
patent-review-skill/
├── patent-workflow/              # 主工作流目录
│   ├── SKILL.md                 # Skill 入口文件
│   ├── workflow/                 # 工作流配置
│   │   ├── patent-review-workflow.json
│   │   ├── node-prompts.md
│   │   └── knowledge/
│   └── scripts/
│       └── case_matcher.py
├── docs/                         # 文档目录
├── tests/                        # 测试目录
└── scripts/                      # 项目脚本
```

## 下一步

- 详细阅读 [工作流使用指南](WORKFLOW_GUIDE.md)
- 查看 [API 参考](API_REFERENCE.md)
- 浏览 [使用示例](EXAMPLES.md)

## 常见问题

### Q: 安装失败怎么办？

确保 Python 版本 >= 3.8：
```bash
python --version
```

### Q: 如何运行测试？

```bash
pytest tests/ -v
```

### Q: 如何查看详细日志？

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
