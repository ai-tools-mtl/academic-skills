# API 参考

## 模块结构

```
patent_review_skill/
├── workflow/
│   ├── __init__.py
│   ├── patent_workflow.py      # 主工作流类
│   ├── nodes.py               # 节点定义
│   └── models.py             # 数据模型
├── scripts/
│   └── case_matcher.py        # 案例匹配器
└── knowledge/
    └── case_database.py       # 案例数据库
```

## PatentReviewWorkflow

主工作流类，负责协调整个审查流程。

### 初始化

```python
from workflow.patent_workflow import PatentReviewWorkflow

workflow = PatentReviewWorkflow(
    config_path: str = "workflow/patent-review-workflow.json",
    knowledge_base: str = "workflow/knowledge/"
)
```

### 方法

#### execute()

执行审查工作流。

```python
def execute(
    self,
    patent_application: str,
    stage: str = "all"
) -> dict
```

**参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `patent_application` | str | 是 | 专利申请文件路径 |
| `stage` | str | 否 | 执行阶段：all/stage1/stage2/stage3/stage4 |

**返回值**：

```python
{
    "case_id": str,
    "stage": str,
    "result": {
        "risk_level": str,           # 低/中/高
        "report": dict,              # 阶段报告
        "recommendation": str         # 建议
    },
    "next_stage": str,               # 下一阶段
    "output_files": list             # 输出文件列表
}
```

#### get_stage_result()

获取特定阶段的结果。

```python
def get_stage_result(
    self,
    case_id: str,
    stage: str
) -> dict
```

## BaseNode

节点基类，所有审查节点都继承自此类。

```python
from workflow.nodes import BaseNode

class MyCustomNode(BaseNode):
    node_type = "ai_process"
    
    def process(self, inputs: dict) -> dict:
        # 处理逻辑
        return {"output_key": "output_value"}
```

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `node_id` | str | 节点唯一标识 |
| `node_name` | str | 节点名称 |
| `node_type` | str | 节点类型：ai_process/human_review |
| `input_variables` | list | 输入变量列表 |
| `output_variables` | list | 输出变量列表 |

### 方法

#### execute()

执行节点。

```python
def execute(self, **kwargs) -> dict
```

#### validate_inputs()

验证输入参数。

```python
def validate_inputs(self, inputs: dict) -> bool
```

## CaseMatcher

案例匹配器，用于检索相似案例。

```python
from scripts.case_matcher import CaseMatcher

matcher = CaseMatcher(
    case_database: str = "workflow/knowledge/case-database.md"
)
```

### 方法

#### search()

搜索相似案例。

```python
def search(
    self,
    features: list,
    limit: int = 10,
    case_type: str = None
) -> list
```

**参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `features` | list | 是 | 技术特征列表 |
| `limit` | int | 否 | 返回数量限制 |
| `case_type` | str | 否 | 案例类型过滤：授权/不授权/边界 |

**返回值**：

```python
[
    {
        "id": str,
        "type": str,
        "title": str,
        "source": str,
        "similarity": float,
        "key_features": list,
        "conclusion": str
    }
]
```

## 数据模型

### ScreeningReport

阶段一筛查报告。

```python
from workflow.models import ScreeningReport

report = ScreeningReport(
    case_id: str,
    risk_level: str,          # 低/中/高
    risk_points: list,        # 风险点列表
    feature_list: list,       # 特征列表
    data_level_initial: str,  # L1-L5
    problem_nature: str       # 技术/算法/商业
)
```

### TripleElementReport

阶段二三要素分析报告。

```python
from workflow.models import TripleElementReport

report = TripleElementReport(
    case_id: str,
    problem_analysis: dict,
    means_analysis: dict,
    effect_analysis: dict,
    correlation_graph: dict,
    element_tech_attr: bool
)
```

### VerificationReport

阶段三验证报告。

```python
from workflow.models import VerificationReport

report = VerificationReport(
    case_id: str,
    data_level: str,           # L1-L5
    domain_correlation: str,   # G0-G4
    matrix_result: str,        # 成功/失败/存疑
    anchor_result: str
)
```

## 异常类

### WorkflowError

工作流执行异常。

```python
from workflow.exceptions import WorkflowError

raise WorkflowError("节点执行失败")
```

### NodeValidationError

节点输入验证异常。

```python
from workflow.exceptions import NodeValidationError

raise NodeValidationError("缺少必需参数")
```

## 常量

### 节点类型

```python
from workflow.constants import NodeType

NodeType.AI_PROCESS    # AI处理节点
NodeType.HUMAN_REVIEW  # 人工审查节点
```

### 风险等级

```python
from workflow.constants import RiskLevel

RiskLevel.LOW   # 低风险
RiskLevel.MEDIUM # 中风险
RiskLevel.HIGH  # 高风险
```

### 阶段标识

```python
from workflow.constants import Stage

Stage.STAGE_1  # 初步穿透筛查
Stage.STAGE_2  # 深度穿透审查
Stage.STAGE_3  # 锚定穿透验证
Stage.STAGE_4  # 案例穿透与结论生成
```
