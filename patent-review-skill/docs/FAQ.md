# 常见问题 (FAQ)

## 基础问题

### Q1: 这个项目是什么？

Patent Review Skill 是一个开源的专利客体适格性审查工具，通过四阶段穿透式审查工作流，帮助审查员快速、准确地判断专利申请是否属于技术方案。

### Q2: 这个项目适合谁使用？

- 专利审查员
- 专利代理人
- 企业知识产权工程师
- 专利律师
- 研究专利法的学者

### Q3: 如何引用这个项目？

```
Patent Review Skill. (2024). GitHub Repository. 
https://github.com/your-org/patent-review-skill
```

## 安装问题

### Q4: 安装失败怎么办？

确保满足以下条件：
- Python 3.8 或更高版本
- pip 已正确安装
- 有网络连接下载依赖

```bash
# 检查 Python 版本
python --version

# 如果使用的是代理网络
pip install --proxy http://proxy.example.com:8080 -r requirements.txt
```

### Q5: 是否支持 Windows/Mac/Linux？

是的，完全支持三大主流操作系统。

### Q6: 需要额外的硬件配置吗？

最低配置：
- 4GB RAM
- 2GB 可用磁盘空间

推荐配置：
- 8GB+ RAM
- 10GB+ 可用磁盘空间

## 使用问题

### Q7: 如何处理大文件？

```python
# 分批处理大文件
workflow = PatentReviewWorkflow()

result = workflow.execute(
    patent_application="./large_case.pdf",
    stage="all",
    chunk_size=1000  # 每批处理1000行
)
```

### Q8: 支持哪些文件格式？

当前版本支持：
- PDF 文件
- TXT 纯文本
- DOCX (需要额外依赖)

### Q9: 如何查看审查进度？

```python
result = workflow.execute(
    patent_application="./case.pdf",
    stage="all",
    progress_callback=lambda p: print(f"进度: {p}%")
)
```

### Q10: 审查结果保存在哪里？

默认保存在当前目录的 `output/` 文件夹：

```
output/
├── 2024-001/
│   ├── stage1_report.json
│   ├── stage2_report.json
│   └── final_opinion.json
```

## 准确性问题

### Q11: 审查结果是否具有法律效力？

**没有**。本工具仅作为辅助工具，提供的审查意见仅供参考。最终的审查结论应由具有执业资格的审查员或律师做出。

### Q12: 如何提高审查准确性？

1. **确保输入完整**：提供完整的权利要求书和说明书
2. **正确配置关键词库**：根据领域调整关键词
3. **认真复核人工节点**：AI 结果需要人工确认
4. **参考案例库**：善用相似案例辅助判断

### Q13: 出现错误结果怎么办？

1. 检查输入文件是否完整
2. 查看详细日志
3. 在 GitHub Issues 反馈问题
4. 附上相关的输入和输出文件

## 扩展问题

### Q14: 如何添加新的案例？

编辑 `workflow/knowledge/case-database.md`，按照格式添加案例：

```markdown
## 新增案例

| 字段 | 值 |
|------|-----|
| ID | case_new_001 |
| 类型 | 授权 |
| 标题 | 新案例名称 |
| ... | ... |
```

### Q15: 如何自定义审查流程？

1. 编辑 `workflow/patent-review-workflow.json` 修改节点
2. 编辑 `workflow/node-prompts.md` 修改 Prompt
3. 运行 `python scripts/validate_workflow.py` 验证配置

### Q16: 是否有 API 可以集成？

是的，支持 REST API 集成。详见 [API 参考](API_REFERENCE.md)。

## 贡献问题

### Q17: 如何贡献代码？

1. Fork 本仓库
2. 创建特性分支
3. 提交 Pull Request

详见 [CONTRIBUTING.md](../CONTRIBUTING.md)

### Q18: 可以提交新的审查案例吗？

可以！请通过 Pull Request 提交，并确保：
- 案例有明确的审查结论
- 包含完整的分析过程
- 不涉及商业机密

### Q19: 如何报告 bug？

请在 GitHub Issues 中报告，包含：
- 详细的问题描述
- 复现步骤
- 环境信息
- 相关的输入/输出文件（脱敏后）

## 其他问题

### Q20: 为什么不采用机器学习模型？

当前版本采用规则+案例匹配的方法，原因：
1. 可解释性强：每一步都有明确的推理过程
2. 稳定性高：结果可复现
3. 易于维护：规则和案例可独立更新

未来版本可能引入 ML 模型用于辅助判断。

### Q21: 知识库多久更新一次？

- 法律依据：根据官方发布实时更新
- 案例库：定期（每季度）补充新案例
- 关键词库：根据审查实践持续优化

### Q22: 如何联系我们？

- GitHub Issues: [提交 Issue](https://github.com/your-org/patent-review-skill/issues)
- Email: contact@example.com
- 微信公众号: [待添加]
