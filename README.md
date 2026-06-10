# Academic Skills

面向 Claude Code（及兼容 Agent 框架）的学术技能集合，覆盖论文写作、润色、引文、图表、数据、全文阅读、审稿回复、文献检索和科研计算。

## 安装

```bash
# 克隆仓库
git clone https://github.com/ai-tools-mtl/academic-skills.git

# 安装单个 skill
cp -R skills/nature-polishing ~/.claude/skills/

# 安装全部 skill
cp -R skills/* ~/.claude/skills/
```

Codex 用户：
```bash
cp -R skills/* ~/.codex/skills/
```

---

## Skill 索引

### Nature 学术写作系列

| Skill | 状态 | 说明 | 触发关键词 |
|-------|------|------|-----------|
| [`nature-polishing`](skills/nature-polishing/SKILL.md) | Stable | Nature 风格学术润色（含中译英） | polish, Nature style, academic writing |
| [`nature-writing`](skills/nature-writing/SKILL.md) | Draft | Nature 风格论文章节起草与论证重构 | write abstract, write introduction, manuscript draft |
| [`nature-figure`](skills/nature-figure/SKILL.md) | Stable | Nature 级 Python/R 科研图表生成 | Nature figure, publication plot, scientific figure |
| [`nature-citation`](skills/nature-citation/SKILL.md) | Beta | Nature / CNS 引文检索与导出（ENW/RIS/Zotero RDF） | citation, supporting references, Zotero |
| [`nature-data`](skills/nature-data/SKILL.md) | Draft | Data Availability 声明、仓库规划与 FAIR 检查 | Data Availability, repository, FAIR metadata |
| [`nature-reader`](skills/nature-reader/SKILL.md) | Beta | 全文双语 Markdown 阅读器（图文对应） | nature reader, full markdown, paper md, 全文翻译 |
| [`nature-response`](skills/nature-response/SKILL.md) | Beta | 逐条审稿意见回复信 | response to reviewers, rebuttal, 审稿意见回复 |
| [`nature-paper2ppt`](skills/nature-paper2ppt/SKILL.md) | Beta | 论文转中文 PPT（journal club / 组会） | paper PPT, journal club, paper to slides |
| [`nature-academic-search`](skills/nature-academic-search/SKILL.md) | Beta | 多源文献检索、引文验证与参考文献管理 | search papers, academic search, verify DOI |

### 科研工具系列

| Skill | 说明 | 触发关键词 |
|-------|------|-----------|
| [`scientific-toolkit-skill`](skills/scientific-toolkit-skill/SKILL.md) | 科研计算工具包（MATLAB/Python 科学分析/信号处理/统计分析/可视化） | MATLAB, scientific Python, data analysis, simulation |
| [`research-writing-skill`](skills/research-writing-skill/SKILL.md) | 科研写作辅助 | research writing, manuscript |
| [`office-academic-skill`](skills/office-academic-skill/SKILL.md) | Word/PPT 学术文档处理 | docx, pptx, office, academic document |

---

## 仓库结构

```
academic-skills/
├── skills/                                    # 所有 skill 的统一目录
│   ├── nature-polishing/SKILL.md              # 学术润色
│   ├── nature-writing/SKILL.md                # 论文写作
│   ├── nature-figure/SKILL.md                 # 科研图表
│   ├── nature-citation/SKILL.md               # 引文检索
│   ├── nature-data/SKILL.md                   # 数据声明
│   ├── nature-reader/SKILL.md                 # 全文阅读器
│   ├── nature-response/SKILL.md               # 审稿回复
│   ├── nature-paper2ppt/SKILL.md              # 论文转PPT
│   ├── nature-academic-search/SKILL.md        # 文献检索
│   ├── scientific-toolkit-skill/SKILL.md      # 科研计算工具包
│   ├── research-writing-skill/SKILL.md        # 科研写作
│   └── office-academic-skill/SKILL.md         # Office 文档处理
├── package.json
└── README.md
```

---

## 设计原则

1. **原始来源优先**：规则基于已发表 Nature 内容或官方期刊指南
2. **显式优于隐式**：每条规则都附有理由说明
3. **章节感知**：学术写作和图表均需要上下文敏感性
4. **输出优先**：每个 skill 返回可直接使用的结果
5. **可扩展**：每个 skill 自包含在独立目录中，互不干扰

## License

MIT
