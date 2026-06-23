---
name: patent-disclosure-pro
description: 专利技术交底书的完整生成与迭代。覆盖技术背景撰写、专利点挖掘、现有技术查新、交底书结构化生成、四章节强制对齐、有益效果严谨化、公式与图示渲染、自检完善全流程。当用户涉及专利挖掘、专利点、技术交底书、交底书、查新、现有技术对比、有益效果等时启用。是 patent-disclosure-skill 的升级版，包含其全部能力并强化了结构对齐、效果严谨性与渲染可靠性。
version: 1.0.0
---

# 专利技术交底书生成（专业版）

本技能覆盖 **专利点挖掘 → 查新与差异化 → 交底书生成 → 四章节对齐 → 效果严谨化 → 自检完善** 全流程。分步指令在 **`prompts/`**，每步执行前 **`Read`** 对应文件。

## 核心原则（贯穿全流程，不可违背）

1. **四章节强制对齐**：技术背景的难题、现有技术缺点、本发明技术问题、有益效果、保护点——这五方必须**严格一一对应**，形成闭环。详见 [章节对齐规则](references/section-alignment.md)。
2. **有益效果禁臆测**：性能/效率类数值**必须有实测数据或数学证明（复杂度分析）支撑**，禁止凭空写绝对时间值（如"约 10 μs""约 5 ms"）。详见 [有益效果写法规则](references/effect-writing.md)。
3. **通俗易懂**：交底书面向代理人（可能非本领域专家），须简洁明了；技术方案用 S1-Sn 步骤式编号，公式集中定义、编号引用不重复本体。详见 [流程与公式规则](references/flow-formula.md)。
4. **定稿必须渲染**：mermaid 图与公式必须转为 PNG 嵌入 docx，不留 ASCII 文字图或 LaTeX 文本。渲染环境配置见 [渲染环境配置](references/render-env.md)。

## 触发条件

- 明确提及：专利挖掘、专利点、技术交底书、交底书、查新、现有技术对比、有益效果等
- **迭代模式（按意图识别）**：当用户意图是在**已有交底书**上继续工作（改章节、补实施例、修正参数、调整表述等），**`Read`** **`prompts/iteration_context.md`**，再 **`Read`** `prompts/merger.md`（扩展合并）或 `prompts/correction_handler.md`（纠错），**另存为新文件** `案件名_YYYYMMDDHHmmss.md/.docx`，**不覆盖**旧稿，追加 `交底书修订对话记录.md`。

## 工具与数据来源

| 任务 | 方式 |
|------|------|
| 加载分步指令 | **`Read`** → `${SKILL_DIR}/prompts/*.md`，见下表 |
| 读代码、设计文档、PDF、图片 | 文件读取工具 |
| Word（.docx）→ Markdown | `python ${SKILL_DIR}/tools/docx_to_md.py --input {path}.docx --output {dir}/{name}.md` |
| PowerPoint → Markdown | `python ${SKILL_DIR}/tools/pptx_to_md.py --input {path}.pptx --output {dir}/{name}.md` |
| 联网查新（Step 5） | **`Read`** `prompts/prior_art_search.md`；优先 `cnipa_epub_search.py`（分多次调用、每轮一词，自行合并 `EPUB_HITS_JSON`）；异常或无果再 WebSearch |
| 交底书定稿交付 | **3.2/3.4** 用 fenced mermaid；定稿执行 `tools/mermaid_render.py`（mermaid→PNG + 公式→PNG + 生成 .docx）。详见 [渲染环境配置](references/render-env.md) 与 `tools/README.md` |
| 保存路径 | 用户指定路径；未指定时建议 `./outputs/{案件标识}/`；**凡交付均含时间戳后缀** `{案件名}_{YYYYMMDDHHmmss}` |

## Prompt 文件映射

| 步骤 | 文件 | 用途 |
|------|------|------|
| Step 1 | `prompts/intake.md` | 边界与输入问题 |
| Step 2 | `prompts/project_scan.md` | 项目文档扫描；.docx/.pptx 须先转换再读 |
| Step 3–4 | `prompts/patent_points_analyzer.md` | 候选专利点、融合与选定 |
| Step 5 | `prompts/prior_art_search.md` | 联网查新与分析 |
| Step 6 | `prompts/disclosure_preview.md` | 全文前的摘要预览 |
| Step 7 | `prompts/disclosure_builder.md` + `prompts/template_reference.md` | 交底书结构、脱敏、符号公式体例、图示规范 |
| Step 8 | `prompts/disclosure_self_check.md` | 内部自检（不写入正文） |
| 迭代 | `prompts/iteration_context.md` | 迭代意图、落盘命名、修订对话记录 |
| 迭代 | `prompts/merger.md` | 新材料增量合并 |
| 迭代 | `prompts/correction_handler.md` | 对话纠正 |

## 主流程（执行顺序）

1. **`Read`** `intake.md` → Step 1
2. **`Read`** `project_scan.md` → Step 2
3. **`Read`** `patent_points_analyzer.md` → Step 3–4
4. **`Read`** `prior_art_search.md` → Step 5
5. **`Read`** `disclosure_preview.md` → Step 6（可跳过）
6. **`Read`** `disclosure_builder.md` 与 `template_reference.md` → Step 7（首次交付亦须带时间戳）
7. **`Read`** `disclosure_self_check.md` → Step 8 内部执行，修订后交付

## 升级版强化的经验规则（本次实战提炼，原版无）

以下规则是本技能区别于原版的核心增量，执行 Step 7/8 及迭代时**必须遵守**：

### A. 技术背景叙事结构
技术背景（1.0 节）按 **"场景 → 发现问题 → 解决问题的预期结果 → 现有技术不支持 → 提出新方法"** 叙事，**分段叙述、不分点**。每段承担一个叙事环节，末段点明本发明针对的难题类别（与四章节主线对应）。详见 [技术背景写法](references/tech-background.md)。

### B. 四章节强制对齐
进入 Step 7 生成正文前，先确定**主线数量**（通常 4~6 条，对应核心发明点）。每条主线贯穿：技术背景难题 → 缺点 → 技术问题 → 有益效果 → 保护点，**五方一一对齐**。若保护点数 ≠ 缺点/问题/效果数，须整合主线（合并同源点、拆分复合点）直至对齐。详见 [章节对齐规则](references/section-alignment.md)。

### C. 有益效果严谨化
- 每条效果统一**对比结构**："现有技术如何 → 本申请如何 → 因此获益多少"。
- **性能/效率数值必须有依据**：实测数据 > 公开文献引用 > 复杂度分析。**禁止臆测绝对值**（μs/ms/数量级倍数）。无数据时用复杂度表述（如 \(O(k)\) vs \(O(|S|)\)），或数据量对比（GB vs 数百字节）。详见 [有益效果写法规则](references/effect-writing.md)。
- **技术论证不入效果**：CDH 假设、双线性对证明等属技术方案论证（归第三章），不写入有益效果。
- **删主观词**："首次提出""大幅"等改为量化或定性事实。

### D. 系统流程 S1-Sn 步骤式
3.4 系统流程说明采用专利常规 **S1/S11/S12… 主-子步骤编号**。每子步骤单一动作。公式用**编号引用**（"式 (n)"），**不在步骤内重复公式本体**——公式集中放 3.4.1 符号与公式节（基于"一处定义、多处引用"的网状结构，集中优于拆散）。详见 [流程与公式规则](references/flow-formula.md)。

### E. 渲染可靠性
- 运行 `mermaid_render.py` 前，若 mmdc 报 "Could not find Chrome"，设置环境变量 `PUPPETEER_EXECUTABLE_PATH` 指向已有 Chrome headless shell（详见 [渲染环境配置](references/render-env.md)）。
- **块级公式须独占行**：`\[` 和 `\]` 各占一行（`line.strip()=="\\["`），否则 md_to_docx 不识别、公式以文本残留。
- **嵌套括号行内公式**（如 `\(H(r \| H(Attr))\)`）math_render 无法生成 PNG，须改为编号引用或文本表述。

## Agent 自用工作流检查清单

```
□ 已按步骤 Read 对应 prompts；Step 2 若目录含 Office，已转换并读产出 .md
□ 识别"在已有交底书上修改"意图时，已 Read iteration_context.md 并选用 merger/correction_handler；交付为新 带时间戳 .md/.docx，未无故覆盖
□ 执行 merger/correction_handler 后，已输出留档摘要；案件目录已追加 交底书修订对话记录.md
□ 技术背景按"场景→问题→结果→不支持→新方法"分段叙事（不分点）
□ 四章节（背景难题/缺点/问题/效果/保护点）已强制对齐，主线数一致
□ 有益效果：对比结构 + 无臆测绝对值（无实测时用复杂度/数据量表述）+ 无技术论证混入
□ 系统流程用 S1-Sn 步骤式；公式编号引用、本体集中放符号公式节
□ mermaid 与公式定稿已渲染为 PNG 嵌入 docx；块级公式独占行；无嵌套括号文本残留
□ 文末无技能/示例仓库类脚注；正文无自检清单章节
□ 凡交付 .md/.docx 均含时间戳后缀
```

## References

- [章节对齐规则](references/section-alignment.md) — 四章节/五方对齐的方法与整合原则
- [有益效果写法规则](references/effect-writing.md) — 对比结构、禁臆测、量化依据分级
- [技术背景写法](references/tech-background.md) — 叙事结构与分段规范
- [流程与公式规则](references/flow-formula.md) — S1-Sn 步骤式与公式位置决策
- [渲染环境配置](references/render-env.md) — mmdc/Chrome 环境陷阱与公式渲染修复

## Scripts / Tools

工具脚本复用 `tools/` 目录（与原版共用），详见 `tools/README.md`：
- [mermaid_render.py](tools/mermaid_render.py) — mermaid + 公式 → PNG + docx
- [md_to_docx.py](tools/md_to_docx.py) — Markdown → Word
- [math_render.py](tools/math_render.py) — LaTeX 公式 → PNG
- [docx_to_md.py](tools/docx_to_md.py) / [pptx_to_md.py](tools/pptx_to_md.py) — Office → Markdown
- [iteration_dialog_log.py](tools/iteration_dialog_log.py) — 修订对话记录追加
- [cnipa_epub_search.py](tools/cnipa_epub_search.py) — 国知局查新
