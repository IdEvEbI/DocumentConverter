# AI 指令集

## 1. 文档目标

本文档提供开发者与 AI 助手协作开发中的常用 AI 指令，确保操作的一致性和效率。

> **适用范围**：Python 项目开发，AI 辅助场景，快速操作指南。

## 2. 项目信息获取

### 2.1 了解项目背景

```bash
# 查看项目结构
list_dir

# 查看产品需求
read_file docs/01-product-requirements/prd.md

# 查看技术架构设计
read_file docs/03-technical-design/architecture.md

# 查看开发者与 AI 助手的协作规范
read_file docs/02-development-standards/01-collaboration-guide.md

# 查看文档格式规范
read_file docs/02-development-standards/02-doc-format-guide.md

# 查看当前任务
read_file docs/04-project-management/task-list.md
```

### 2.2 代码结构了解

```bash
# 查看代码文件
list_dir src/
list_dir tests/

# 查看主要代码文件
read_file src/main.py
read_file requirements.txt

# 查看文档目录
list_dir docs/

# 查看文档内容
read_file docs/README.md
```

### 2.3 代码搜索与阅读

```bash
# 读取文件内容
read_file target_file start_line end_line

# 读取整个文件
read_file target_file should_read_entire_file=True

# 语义搜索
codebase_search "搜索关键词"

# 精确搜索
grep_search "exact_pattern"

# 文件搜索
file_search "filename"

# 搜索文档内容
grep_search "关键词" include_pattern="*.md"
```

## 3. 开发环境管理

### 3.1 环境搭建

```bash
# 创建虚拟环境
run_terminal_cmd python -m venv venv

# 激活虚拟环境
run_terminal_cmd source venv/bin/activate

# 安装依赖
run_terminal_cmd pip install -r requirements.txt
```

### 3.2 依赖管理

```bash
# 查看已安装包
run_terminal_cmd pip list

# 安装新包
run_terminal_cmd pip install package_name

# 更新 requirements.txt
run_terminal_cmd pip freeze > requirements.txt
```

### 3.3 环境检查

```bash
# 检查 Python 版本
run_terminal_cmd python --version

# 检查 pip 版本
run_terminal_cmd pip --version

# 检查虚拟环境
run_terminal_cmd which python
```

## 4. 质量保证操作

### 4.1 测试执行

```bash
# 激活虚拟环境
run_terminal_cmd source venv/bin/activate

# 运行所有测试
run_terminal_cmd python -m pytest

# 运行特定测试
run_terminal_cmd python -m pytest tests/test_specific.py

# 运行测试并显示覆盖率
run_terminal_cmd python -m pytest --cov=src
```

### 4.2 代码质量检查

```bash
# 激活虚拟环境
run_terminal_cmd source venv/bin/activate

# 运行代码检查
run_terminal_cmd flake8 src/

# 运行类型检查
run_terminal_cmd mypy src/

# 运行格式化
run_terminal_cmd black src/
```

### 4.3 性能测试

```bash
# 激活虚拟环境
run_terminal_cmd source venv/bin/activate

# 测试大文件处理
run_terminal_cmd python src/main.py word2md large_file.docx large_output.md

# 测试转换速度
run_terminal_cmd time python src/main.py word2md test.docx test.md
```

## 5. 开发流程管理

### 5.1 里程碑完成流程

```bash
# 1. 推送所有内容到远程
run_terminal_cmd git push origin feature/current-branch

# 2. 检查当前分支名称
run_terminal_cmd git branch --show-current

# 3. 切换到 develop 分支
run_terminal_cmd git checkout develop

# 4. 从远程拉取最新代码并合并功能分支
run_terminal_cmd git pull origin develop
run_terminal_cmd git merge feature/current-branch --no-ff -m "feat: 合并功能分支到develop"
# 如果有冲突，解决后继续；如果没有冲突，直接合并

# 5. 删除功能分支并清理远程分支缓存
run_terminal_cmd git branch -d feature/current-branch
run_terminal_cmd git fetch --prune

# 可选：如果需要备份，在合并前执行
# run_terminal_cmd git diff develop..feature/current-branch > milestone_backup.patch
```

### 5.2 新里程碑开始流程

```bash
# 1. 确保在 develop 分支并拉取最新代码
run_terminal_cmd git checkout develop
run_terminal_cmd git pull origin develop

# 2. 切换身份为 Python 高级开发工程师
# 身份切换：从文档工程师切换到 Python 高级开发工程师

# 3. 阅读需求文档确保理解到位
read_file docs/04-project-management/task-list.md
read_file docs/01-product-requirements/prd.md
read_file docs/03-technical-design/architecture.md

# 4. 创建新功能分支
run_terminal_cmd git checkout -b feature/new-milestone

# 5. 确定里程碑版本和文档类型
# 根据当前开发阶段确定版本（v1.0、v2.0、v3.0）
# 根据功能类型确定文档名称（parser、converter、cli、testing等）

# 6. 创建版本化文档目录
run_terminal_cmd mkdir -p docs/03-technical-design/v1.0

# 7. 按照文档格式规范创建技术设计文档
edit_file docs/03-technical-design/v1.0/mvp-design.md
# 使用 docs/02-development-standards/02-doc-format-guide.md 中的模板
# 确保包含：文档目标、设计概述、详细设计、实现计划、风险评估、核心要点

# 8. 创建模块设计文档
edit_file docs/03-technical-design/v1.0/parser-v1.md
edit_file docs/03-technical-design/v1.0/converter-v1.md
edit_file docs/03-technical-design/v1.0/cli-v1.md
edit_file docs/03-technical-design/v1.0/testing-v1.md

# 9. 更新主架构文档
edit_file docs/03-technical-design/architecture.md

# 10. 更新任务清单明细
edit_file docs/04-project-management/task-list.md
# 根据技术设计文档更新具体任务

# 11. 提交技术设计文档
run_terminal_cmd git add docs/03-technical-design/
run_terminal_cmd git commit -m "docs: 添加 v1.0 里程碑技术设计文档"
run_terminal_cmd git push origin feature/new-milestone

# 8. 激活虚拟环境
run_terminal_cmd source venv/bin/activate

# 9. 按任务清单逐项推进
read_file docs/04-project-management/task-list.md
# 每个子任务完成后等待人工确认
```

### 5.3 分支状态检查

```bash
# 查看所有分支
run_terminal_cmd git branch -a

# 查看当前分支
run_terminal_cmd git branch --show-current

# 查看分支状态
run_terminal_cmd git status

# 查看提交历史
run_terminal_cmd git log --oneline -10
```

## 6. 文档管理操作

### 6.1 文档创建流程

```bash
# 新里程碑开始时的文档创建流程
# 1. 确定里程碑版本和文档类型
# 根据当前开发阶段确定版本（v1.0、v2.0、v3.0）
# 根据功能类型确定文档名称（parser、converter、cli、testing等）

# 2. 创建版本化文档目录
run_terminal_cmd mkdir -p docs/03-technical-design/v1.0

# 3. 按照文档格式规范创建技术设计文档
edit_file docs/03-technical-design/v1.0/mvp-design.md
# 使用 docs/02-development-standards/02-doc-format-guide.md 中的模板
# 确保包含：文档目标、设计概述、详细设计、实现计划、风险评估、核心要点

# 4. 创建模块设计文档
edit_file docs/03-technical-design/v1.0/parser-v1.md
edit_file docs/03-technical-design/v1.0/converter-v1.md
edit_file docs/03-technical-design/v1.0/cli-v1.md
edit_file docs/03-technical-design/v1.0/testing-v1.md

# 5. 更新主架构文档
edit_file docs/03-technical-design/architecture.md

# 6. 执行文档质量检查
# 检查文档结构完整性、内容准确性、可维护性
grep_search "TODO" include_pattern="docs/03-technical-design/v1.0/*.md"
```

### 6.2 文档同步机制

```bash
# 代码变更时的文档同步
# 1. 代码变更
edit_file src/core/parser.py

# 2. 更新相关文档
edit_file docs/03-technical-design/v1.0/parser-v1.md

# 3. 更新主架构文档
edit_file docs/03-technical-design/architecture.md

# 4. 提交文档变更
run_terminal_cmd git add docs/
run_terminal_cmd git commit -m "docs: 更新解析器设计文档"
```

### 6.3 版本化文档管理

```bash
# 版本升级时的文档管理
# 1. 创建新版本目录
run_terminal_cmd mkdir -p docs/03-technical-design/v2.0

# 2. 复制并升级相关文档
run_terminal_cmd cp docs/03-technical-design/v1.0/parser-v1.md docs/03-technical-design/v2.0/parser-v2.md

# 3. 更新版本信息
edit_file docs/03-technical-design/v2.0/parser-v2.md

# 4. 更新主架构文档
edit_file docs/03-technical-design/architecture.md
```

### 6.4 文档质量检查

```bash
# 定期文档审查
# 1. 检查文档完整性
grep_search "TODO" include_pattern="docs/**/*.md"

# 2. 检查文档一致性
grep_search "v1.0" include_pattern="docs/**/*.md"

# 3. 检查文档结构
list_dir docs/03-technical-design/

# 4. 更新文档状态
edit_file docs/03-technical-design/architecture.md
```

### 6.5 里程碑文档创建质量保证

```bash
# 新里程碑文档创建前的质量保证流程
# 1. 确认里程碑版本和文档类型
read_file docs/04-project-management/task-list.md
read_file docs/03-technical-design/architecture.md

# 2. 检查文档格式规范
read_file docs/02-development-standards/02-doc-format-guide.md

# 3. 创建文档时确保包含以下要素：
# - 文档目标：明确文档目的和适用范围
# - 版本信息：文档版本、最后更新、更新内容
# - 设计概述：设计目标、设计原则、技术选型
# - 详细设计：架构设计、接口设计、数据流设计
# - 实现计划：开发阶段、测试策略、部署计划
# - 风险评估：技术风险、缓解措施
# - 核心要点：一句话总结

# 4. 文档创建后的质量检查
# - 结构完整性：总分总结构，标题数量控制
# - 内容准确性：技术选型合理，设计原则明确
# - 可维护性：格式标准一致，版本控制清晰

# 5. 提交前最终检查
run_terminal_cmd git diff docs/03-technical-design/
# 确认文档变更符合预期
```

## 7. 核心要点

- **信息获取**：项目背景、代码结构、文档内容快速了解
- **环境管理**：虚拟环境、依赖安装、环境检查标准化操作
- **质量保证**：测试执行、代码检查、性能测试完整链路
- **流程管理**：里程碑完成、新阶段开始、分支状态检查
- **文档管理**：文档创建、同步、版本化、质量检查标准化操作
- **协作效率**：标准化的 AI 指令集，实现快速操作和高效协作

> **一句话总结**：通过标准化的 AI 指令集，实现项目开发的快速操作和高效协作。
