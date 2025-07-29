# AI 指令集

## 1. 文档目标

本文档提供刘凡与小克协作开发中的常用 AI 指令，确保操作的一致性和效率。

> **适用范围**：Python 项目开发，AI 辅助场景，快速操作指南。

## 2. 项目信息获取

### 2.1 项目背景了解

```bash
# 查看项目结构
list_dir

# 查看当前任务
read_file docs/04-project-management/task-list.md

# 查看产品需求
read_file docs/01-product-requirements/prd.md

# 查看项目计划
read_file docs/04-project-management/project-plan.md
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
run_terminal_cmd git add .
run_terminal_cmd git commit -m "feat: 完成阶段里程碑"
run_terminal_cmd git push origin feature/current-branch

# 2. 检查当前分支名称
run_terminal_cmd git branch --show-current

# 3. 切换到 develop 分支
run_terminal_cmd git checkout develop

# 4. 从远程拉取最新代码
run_terminal_cmd git pull origin develop

# 5. 从本地分支做 diff 合并（安全备份）
run_terminal_cmd git diff develop..feature/current-branch > milestone_backup.patch

# 6. 删除功能分支
run_terminal_cmd git branch -d feature/current-branch

# 7. 更新远程分支缓存
run_terminal_cmd git fetch --prune
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

# 5. 编写技术设计文档并等待确认
edit_file docs/03-technical-design/new-feature-design.md
# 等待用户确认技术设计文档

# 6. 更新任务清单明细
edit_file docs/04-project-management/task-list.md
# 根据技术设计文档更新具体任务

# 7. 提交技术设计文档
run_terminal_cmd git add docs/03-technical-design/new-feature-design.md
run_terminal_cmd git commit -m "docs: 添加新里程碑技术设计文档"
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

## 6. 核心要点

- **信息获取**：项目背景、代码结构、文档内容快速了解
- **环境管理**：虚拟环境、依赖安装、环境检查标准化操作
- **质量保证**：测试执行、代码检查、性能测试完整链路
- **流程管理**：里程碑完成、新阶段开始、分支状态检查
- **协作效率**：标准化的 AI 指令集，实现快速操作和高效协作

> **一句话总结**：通过标准化的 AI 指令集，实现项目开发的快速操作和高效协作。
