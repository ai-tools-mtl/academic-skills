# Contributing to Patent Review Skill

感谢您对 Patent Review Skill 项目的贡献！

## 行为准则

请尊重所有参与项目的贡献者。保持友善、专业和包容。

## 如何贡献

### 报告 Bug

1. 在 GitHub Issues 中搜索是否已有相同的 bug 报告
2. 如无，请创建新的 Issue，包含：
   - 清晰的标题和描述
   - 复现步骤
   - 预期行为和实际行为
   - 环境信息（Python 版本、操作系统等）

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 代码风格
- 为新功能添加测试
- 确保所有测试通过
- 更新相关文档

## 开发设置

```bash
# 克隆仓库
git clone https://github.com/your-org/patent-review-skill.git
cd patent-review-skill

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# 安装开发依赖
pip install -r requirements.txt

# 安装 pre-commit 钩子
pip install pre-commit
pre-commit install

# 运行测试
pytest tests/
```

## 分支管理

- `main`: 稳定版本，只接受 PR 合并
- `develop`: 开发版本，用于集成测试
- `feature/*`: 特性分支
- `fix/*`: 修复分支

## 提交信息规范

使用清晰的提交信息：

```
feat: 添加新特性
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建或辅助工具更新
```

示例：
```
feat: 添加案例匹配模糊搜索功能

- 支持正则表达式匹配
- 添加相似度阈值参数
- 更新文档和测试
```

## Pull Request 流程

1. 确保代码通过所有 CI 检查
2. 更新相关文档
3. PR 描述应包含：
   - 更改的目的
   - 技术实现细节
   - 相关的 Issue 编号

## 许可

通过贡献代码，您同意您的代码将受 MIT 许可证保护。
