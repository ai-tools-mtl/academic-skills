# 使用示例

## 示例一：基础案例审查

```python
from workflow.patent_workflow import PatentReviewWorkflow

# 初始化工作流
workflow = PatentReviewWorkflow()

# 执行完整审查
result = workflow.execute(
    patent_application="./samples/case_deep_learning.pdf",
    stage="all"
)

print(f"风险等级: {result['result']['risk_level']}")
print(f"建议: {result['result']['recommendation']}")
```

## 示例二：快速筛查

```python
# 仅执行阶段一（快速筛查）
result = workflow.execute(
    patent_application="./samples/case_simple.pdf",
    stage="stage1"
)

# 检查结果
if result['result']['risk_level'] == '低':
    print("低风险案件，可直接结案")
else:
    print(f"需要进入{result['next_stage']}进一步审查")
```

## 示例三：自定义节点执行

```python
from workflow.nodes import FeatureExtractionNode, NameRealSeparationNode

# 单独执行特征提取
feature_node = FeatureExtractionNode()
features = feature_node.execute(
    patent_application="./case.pdf"
)

# 使用前一步结果执行后续节点
name_real_node = NameRealSeparationNode()
risks = name_real_node.execute(
    feature_list=features['feature_list']
)
```

## 示例四：批量案例处理

```python
import os
from workflow.patent_workflow import PatentReviewWorkflow

workflow = PatentReviewWorkflow()

# 批量处理目录中的所有PDF
input_dir = "./batch_input"
output_dir = "./batch_output"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith('.pdf'):
        case_path = os.path.join(input_dir, filename)
        result = workflow.execute(
            patent_application=case_path,
            stage="all"
        )
        
        # 保存结果
        output_file = os.path.join(output_dir, f"{filename}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"处理完成: {filename}")
```

## 示例五：案例匹配查询

### 命令行使用

```bash
# 搜索包含特定特征的案例
python scripts/case_matcher.py \
    --features "深度学习,神经网络,图像处理" \
    --format json \
    --limit 5

# 搜索仅授权案例
python scripts/case_matcher.py \
    --features "分类,聚类" \
    --format text \
    --case-type 授权
```

### Python API 使用

```python
from scripts.case_matcher import CaseMatcher

# 初始化匹配器
matcher = CaseMatcher()

# 搜索相似案例
features = ["深度学习", "神经网络", "训练"]
cases = matcher.search(features, limit=5)

# 打印结果
for case in cases:
    print(f"\n案例: {case['title']}")
    print(f"类型: {case['type']}")
    print(f"相似度: {case['similarity']:.2%}")
    print(f"结论: {case['conclusion']}")
```

## 示例六：自定义工作流配置

```python
from workflow.patent_workflow import PatentReviewWorkflow
import json

# 加载自定义配置
with open('custom_workflow.json', 'r') as f:
    config = json.load(f)

# 使用自定义配置初始化
workflow = PatentReviewWorkflow(
    config_path="custom_workflow.json",
    knowledge_base="./custom_knowledge/"
)

# 执行
result = workflow.execute(
    patent_application="./case.pdf",
    stage="all"
)
```

## 示例七：人机协同模式

```python
from workflow.patent_workflow import PatentReviewWorkflow
from workflow.nodes import HumanReviewNode

workflow = PatentReviewWorkflow()

# 执行到人工节点
result = workflow.execute(
    patent_application="./case.pdf",
    stage="stage1"
)

# 获取审查员复核任务
if 'review_required' in result:
    review_task = result['review_required']
    
    # 审查员操作
    decision = {
        "action": "approve",  # approve/reject/terminate
        "comment": "确认高风险，需进入深度审查",
        "next_stage": "stage2"
    }
    
    # 提交审查员决策
    workflow.submit_review(
        task_id=review_task['task_id'],
        decision=decision
    )
```

## 示例八：分析报告生成

```python
from workflow.report_generator import ReportGenerator

generator = ReportGenerator()

# 生成阶段报告
report = generator.generate_stage_report(
    case_id="2024-001",
    stage="stage2",
    data=triple_element_result
)

# 保存为HTML
report.save("output/stage2_report.html")

# 保存为PDF
report.save_pdf("output/stage2_report.pdf")

# 生成完整审查报告
full_report = generator.generate_full_report(
    case_id="2024-001",
    all_stage_results=all_results
)
```

## 示例九：调试模式

```python
from workflow.patent_workflow import PatentReviewWorkflow
import logging

# 开启调试模式
logging.basicConfig(level=logging.DEBUG)

workflow = PatentReviewWorkflow(debug=True)

# 执行并查看详细日志
result = workflow.execute(
    patent_application="./case.pdf",
    stage="stage1"
)

# 查看每个节点的执行时间
for node_exec in result['node_executions']:
    print(f"{node_exec['node_name']}: {node_exec['duration']}ms")
```

## 示例十：集成到现有系统

```python
from workflow.patent_workflow import PatentReviewWorkflow
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
workflow = PatentReviewWorkflow()

class ReviewRequest(BaseModel):
    patent_file: str
    stage: str = "all"

class ReviewResponse(BaseModel):
    case_id: str
    risk_level: str
    recommendation: str

@app.post("/review", response_model=ReviewResponse)
async def review_patent(request: ReviewRequest):
    result = workflow.execute(
        patent_application=request.patent_file,
        stage=request.stage
    )
    return ReviewResponse(
        case_id=result['case_id'],
        risk_level=result['result']['risk_level'],
        recommendation=result['result']['recommendation']
    )
```
