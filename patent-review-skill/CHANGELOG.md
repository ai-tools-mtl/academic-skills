# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added

- 初始版本发布
- 四阶段穿透式审查工作流
  - 阶段一：初步穿透筛查（6节点）
  - 阶段二：深度穿透审查（6节点）
  - 阶段三：锚定穿透验证（5节点）
  - 阶段四：案例穿透与结论生成（4节点）
- 量化分析模型
  - L1-L5 数据含义层级模型
  - G0-G4 领域关联度模型
  - L×G 判断矩阵
- 知识库
  - 最新审查指南（2024）法律依据
  - 权威案例库（12个案例）
  - 关键词库
- 案例匹配工具脚本
- 完整的文档
  - 快速入门
  - 工作流指南
  - API 参考
  - 使用示例

### Features

- 21个节点（17个AI处理 + 4个人工干预）
- 可配置的节点 Prompt 模板
- 结构化输出格式
- JSON 和 Text 两种输出格式支持

## [Unreleased]

### Planned

- [ ] 支持自定义工作流配置
- [ ] 添加更多审查示例
- [ ] Web 界面
- [ ] REST API
- [ ] 批量处理功能
