# 渲染环境配置

mermaid 图与公式渲染为 PNG 的环境配置与常见陷阱修复。基于实战经验（puppeteer/Chrome 版本不匹配问题）。

## mmdc 与 Chrome 版本不匹配（最常见陷阱）

### 问题现象
运行 `mermaid_render.py` 时，mmdc 报错：
```
Error: Could not find Chrome (ver. 131.0.6778.204). This can occur if either
 1. you did not perform an installation before running the script
 2. your cache path is incorrectly configured
```

### 根因
mermaid-cli 11.x 内置的 puppeteer-core 期望特定 Chrome 版本（如 131），但本机 puppeteer 缓存中该版本可能：
- 仅下载了截断的 zip（不完整）
- 或只有其他版本（如 147/148）

### 解决方案：环境变量指向已有 Chrome

**mermaid_render.py 不暴露 `-p`（puppeteerConfigFile）参数**，无法通过命令行传配置文件。但 puppeteer 会读取环境变量 `PUPPETEER_EXECUTABLE_PATH`，优先于版本检查。

**步骤**：
1. 查找本机已有的 Chrome headless shell：
   ```bash
   ls ~/.cache/puppeteer/chrome-headless-shell/
   # 找到可用版本，如 win64-147.0.7727.57
   ```
2. 设置环境变量后运行渲染：
   ```bash
   export PUPPETEER_EXECUTABLE_PATH='C:\Users\{user}\.cache\puppeteer\chrome-headless-shell\win64-147.0.7727.57\chrome-headless-shell-win64\chrome-headless-shell.exe'
   python tools/mermaid_render.py -i input.md -o output.md
   ```

3. **验证**：渲染日志应显示 "mermaid：N 处已转为 PNG" 且无 mmdc 错误。

### 清理截断的下载
若缓存中有截断的 zip（文件明显偏小，如 20MB 而 headless shell 完整约 150MB+），删除它避免混淆：
```bash
rm ~/.cache/puppeteer/chrome-headless-shell/131.0.6778.204-*.zip
```

## 渲染流水线

`mermaid_render.py` 一步完成全部渲染：

```
mermaid_render.py
├── math_render.py（先跑）：LaTeX 公式 → PNG（行内 $...$/\(...\)、块级 $$...$$/\[...\]）
├── mmdc（后跑）：mermaid 围栏 → PNG
└── md_to_docx.py（最后）：Markdown → Word（嵌入所有 PNG）
```

### 关键行为
- **math_render 对已有隐藏注释的公式跳过**（正则含 `(?!\s*<!--)` 负向先行断言），重跑安全、不重排编号
- **mermaid 围栏保留源码** + 追加 `<!-- ![图示 n](mermaid_figures/...) -->` 隐藏注释（.md 预览不显示图，docx 嵌 PNG）
- **失败降级**：某块 mmdc 失败不中断，该块保留围栏源码，其余照常出图

## 常见渲染问题速查

| 问题 | 原因 | 修复 |
|------|------|------|
| 块级公式以 LaTeX 文本残留 | `\[\dots\]` 单行书写，解析器只识别独占行的 `\[` | 改为多行：`\[` + 公式体 + `\]` |
| 行内公式含嵌套括号无法渲染 | 正则在内层 `)` 截断 | 改为编号引用或文本表述 |
| mermaid 图在 docx 中显示为代码块 | `mermaid_figures/` 为空，未渲染 | 检查 mmdc/Chrome 环境（见上） |
| docx 公式图过小/过大 | md_to_docx 公式图默认 0.17 英寸高 | 一般无需调；特殊需求用 `--image-max-height-inches` |
| 重跑后公式编号错乱 | math_render 对已有注释跳过则安全；若强制重渲染会重排 | 默认安全；勿删隐藏注释后重跑 |

## 交付前渲染检查

定稿交付前，确认：
```
□ mermaid_figures/ 非空（含 fig_001.png 等）
□ math_figures/ 含 eq_00X.png（块级）+ inline_NNN.png（行内）
□ .docx 中 w:drawing 占位数 = 公式数 + mermaid 数（可用 python-docx 计数验证）
□ .docx 中无残留 LaTeX 文本（搜 "\\[" "\\arg" "mathit{" 等关键词）
```
