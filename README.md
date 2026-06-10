# Academic Skills

面向 AI 编码 Agent 的学术技能集合。将论文写作、润色、引文、图表、数据、全文阅读、审稿回复、文献检索和科研计算转化为 Agent 可执行的决策指导。

所有技能遵循 [Agent Skills](https://agentskills.io/) 开放标准。

## 可用技能

### nature-polishing

使用写作策略原则、精选 Nature/Nature Communications 文章模式和 Academic Phrasebank 短语级支持，将学术散文润色、重构或翻译为 Nature 风格英文。

**适用场景：**
- 润色学术稿件文本
- 中文学术文本翻译为英文
- 按 Nature 期刊标准提升文笔质量
- 重构句子以提升清晰度和影响力

### nature-writing

从作者提供的研究结论、实验结果、图表、笔记或中文草稿出发，起草、重构或规划 Nature 风格论文章节。

**适用场景：**
- 撰写或重构摘要、引言、结果、讨论或结论
- 规划论文论证结构
- 从研究笔记起草论文章节

### nature-figure

面向 Python 或 R 的 Nature 级/高影响力期刊图表工作流。创建、修改、审计或打磨稿件图表和多面板科研绘图。

**适用场景：**
- 创建出版级科研图表
- 生成多面板稿件插图
- 导出 SVG/PDF/TIFF 供期刊投稿
- 审计图表是否符合 Nature 规范

### nature-citation

通过检索 Nature Portfolio、AAAS Science 家族和 Cell Press 的旗舰及子刊，为稿件添加严格的 Nature/CNS 引文，并导出参考文献管理器格式。

**适用场景：**
- 为稿件添加支撑性参考文献
- 检索 CNS 级期刊引文
- 导出引文供 Zotero 等文献管理器使用

### nature-data

准备、审计或修改符合 Nature 规范的 Data Availability 声明、数据仓库规划、数据集引用和 FAIR 元数据检查清单。

**适用场景：**
- 撰写 Data Availability 声明
- 规划数据仓库上传
- 检查 FAIR 元数据合规性
- 准备数据集引用

### nature-reader

构建全文中英对照、图表对应的 Markdown 阅读器，适用于期刊或会议论文。

**适用场景：**
- 将论文转换为双语 Markdown
- 带图表引用的全文阅读
- 逐章节翻译论文

### nature-response

起草、审计或修改 Nature 系列期刊稿件的逐条审稿意见回复信。

**适用场景：**
- 撰写审稿人回复
- 准备反驳信（rebuttal）
- 根据审稿意见修改稿件

### nature-paper2ppt

从科研论文生成完整的 Nature 风格中文 PPTX 演示文稿，输出包含中文幻灯片内容和演讲者备注的真实 .pptx 文件。

**适用场景：**
- 将论文转换为演示幻灯片
- 准备 journal club 或组会报告
- 从 PDF 或文章文本生成 PPT

### nature-academic-search

通过 MCP 工具进行多源文献检索、引文验证、MeSH 检索策略、引文文件管理和参考文献管理。

**适用场景：**
- 跨 PubMed、CrossRef、arXiv 检索论文
- 验证 DOI 和引文准确性
- 管理参考文献（.nbib/.ris/.bib 转换）
- 协调多步骤文献工作流

### scientific-toolkit-skill

面向 MATLAB/Octave 和 Python 的科研计算工具包，覆盖信号处理、图像处理、统计分析、仿真优化和出版级图表。

**适用场景：**
- 运行 MATLAB 或 Python 科学计算
- 处理信号、图像或时间序列数据
- 统计分析与仿真
- 生成出版级图表

### research-writing-skill

中文优先的科研论文写作、修改、润色、章节起草、反驳信、同行评审回复和论文论证规划。

**适用场景：**
- 中文科研论文写作
- 起草或修改论文章节
- 准备同行评审回复

### office-academic-skill

中文优先的学术 Word 和 PowerPoint 工作流，覆盖论文读书报告、学位论文 PPT、可编辑 DOCX/PPTX 生成和排版质量检查。

**适用场景：**
- 生成学术 DOCX 或 PPTX 文档
- 创建论文读书报告
- 制作毕业答辩演示文稿

## 安装

```bash
npx add-skill ai-tools-mtl/academic-skills
```

## 使用

安装后技能自动生效。Agent 会在检测到相关任务时自动调用。

**示例：**
```
用 Nature 风格润色这段摘要
```
```
用这些数据生成出版级图表
```
```
针对这些审稿意见撰写回复信
```

## 技能结构

每个技能包含：
- `SKILL.md` - Agent 指令文件
- `scripts/` - 辅助自动化脚本（可选）
- `references/` - 补充参考文档（可选）

## License

MIT
