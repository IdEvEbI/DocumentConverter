# DocumentConverter 环境设置 v1.0 设计文档

## 1. 文档目标

本文档定义 DocumentConverter 项目 v1.0 MVP 版本的环境设置方案，专注开发环境配置和依赖管理。

> **适用范围**：Python 项目开发，开发环境搭建。

---

**文档版本**：v1.0  
**最后更新**：2025-07-30  
**更新内容**：精简内容，专注环境配置，删除重复内容

## 2. 设计概述

### 2.1 设计目标

建立标准化的开发环境，确保：

- **环境一致性**：所有开发者使用相同的环境配置
- **快速部署**：一键搭建开发环境
- **依赖管理**：清晰的依赖版本控制
- **工具集成**：开发工具的最佳实践配置

### 2.2 设计原则

- **最小化原则**：只安装必要的工具和依赖
- **版本锁定**：固定依赖版本，确保稳定性
- **自动化优先**：脚本化环境搭建过程
- **文档驱动**：详细的环境配置文档

### 2.3 技术选型

#### 核心技术栈

- **Python 环境**：Python 3.12+ + venv + pip
- **开发工具**：VSCode + black + flake8 + mypy
- **版本控制**：Git + GitHub + 分支策略

> 详细技术选型请参考：01-mvp-design.md

## 3. 详细设计

### 3.1 环境架构设计

```text
┌─────────────────┐
│   IDE Layer     │  # 开发工具层
│                 │
│  - VSCode       │  # 代码编辑器
│  - Extensions   │  # 插件扩展
│  - Settings     │  # 编辑器配置
├─────────────────┤
│   Python Layer  │  # Python 环境层
│                 │
│  - Python 3.12+ │  # Python 解释器
│  - venv         │  # 虚拟环境
│  - pip          │  # 包管理器
├─────────────────┤
│   Project Layer │  # 项目层
│                 │
│  - src/         │  # 源代码
│  - tests/       │  # 测试代码
│  - docs/        │  # 文档
└─────────────────┘
```

### 3.2 依赖管理设计

#### 核心依赖（MVP 版本）

```python
# requirements.txt
# CLI 框架
click>=8.0.0
rich>=10.0.0

# PDF 处理
pdfplumber>=0.7.0
PyPDF2>=3.0.0

# Word 处理
python-docx>=0.8.11

# Markdown 处理
markdown>=3.3.0
markdownify>=0.11.0
```

#### 开发依赖

```python
# requirements-dev.txt
# 测试框架
pytest>=7.0.0
pytest-cov>=4.0.0

# 代码质量
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0

# 类型存根
types-Markdown>=0.1.0
types-flake8>=7.0.0

# 文档工具
sphinx>=7.0.0
sphinx-rtd-theme>=1.0.0
```

### 3.3 目录结构设计

```ini
DocumentConverter/
├── src/                     # 源代码目录
│   ├── __init__.py
│   ├── main.py              # 主入口
│   ├── cli/                 # 命令行接口
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── core/                # 核心功能
│   │   ├── __init__.py
│   │   ├── parser.py        # 解析器
│   │   ├── converter.py     # 转换器
│   │   ├── generator.py     # 生成器
│   │   └── models.py        # 数据模型
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── logger.py
│       └── file_utils.py
├── tests/                   # 测试目录
│   ├── __init__.py
│   ├── data/                # 测试数据
│   │   ├── sample.pdf
│   │   ├── sample.docx
│   │   └── sample.md
│   ├── test_parser.py
│   ├── test_converter.py
│   └── test_generator.py
├── docs/                    # 文档目录
├── scripts/                 # 脚本目录
│   ├── setup_env.sh         # 环境搭建脚本
│   └── run_tests.sh         # 测试运行脚本
├── .vscode/                 # VSCode 配置
│   ├── settings.json
│   └── extensions.json
├── requirements.txt         # 生产依赖
├── requirements-dev.txt     # 开发依赖
├── setup.py                 # 安装配置
├── pyproject.toml           # 项目配置
├── .gitignore               # Git 忽略文件
├── README.md                # 项目说明
└── .env.example             # 环境变量示例
```

## 4. 实现计划

### 4.1 环境搭建阶段

#### 第一步：基础环境检查

- [x] 检查 Python 版本（3.12+）
- [x] 检查 Git 版本
- [x] 检查 VSCode 安装

#### 第二步：项目结构创建

- [x] 创建项目目录结构
- [x] 创建虚拟环境
- [x] 安装基础依赖

#### 第三步：开发工具配置

- [x] 配置 VSCode 设置
- [x] 安装 VSCode 插件
- [x] 配置代码格式化

#### 第四步：测试环境验证

- [x] 运行基础测试
- [x] 验证环境功能
- [x] 检查代码质量工具

### 4.2 自动化脚本设计

#### 环境搭建脚本 (`scripts/setup_env.sh`)

**作用目的**：自动化环境搭建过程，确保所有开发者使用相同的环境配置。

**关键功能**：

- Python 版本检查（3.12+）
- 虚拟环境创建和依赖安装
- 项目目录结构创建
- VSCode 配置自动生成
- `pyproject.toml` 配置文件创建

**关键设置**：

- 使用现代 VSCode 配置格式（`[python]` 部分）
- 设置 Black 格式化器和 88 字符标尺
- 配置 pytest 测试框架
- 添加类型存根依赖支持

#### 测试运行脚本 (`scripts/run_tests.sh`)

**作用目的**：统一测试执行流程，包含单元测试和代码质量检查。

**关键功能**：

- 激活虚拟环境
- 运行 pytest 单元测试
- 执行 Black 格式检查
- 运行 Flake8 代码质量检查

### 4.3 配置文件设计

#### pyproject.toml

**作用目的**：现代 Python 项目的标准配置文件，定义项目元数据、依赖管理和工具配置。

**关键配置**：

- **项目信息**：名称、版本、描述、作者
- **依赖管理**：核心依赖和开发依赖分离
- **工具配置**：Black（88字符）、Flake8、Pytest 设置
- **入口点**：`documentconverter` 命令行工具

**重要设置**：

- Python 版本要求：`>=3.12`
- 代码格式化：Black 88字符行长
- 测试框架：Pytest 配置
- 类型检查：支持 mypy 和类型存根

#### setup.py

**作用目的**：传统的 Python 包安装配置，提供向后兼容性。

**关键配置**：

- 包发现和目录结构
- 依赖管理（与 pyproject.toml 保持一致）
- 命令行入口点定义
- 项目元数据和分类信息

> **注意**：现代项目优先使用 `pyproject.toml`，`setup.py` 主要用于向后兼容。

## 5. 风险评估

### 5.1 技术风险

#### 环境兼容性

- **风险**：不同操作系统环境差异
- **缓解措施**：使用跨平台工具，提供详细的环境要求

#### 依赖冲突

- **风险**：依赖包版本冲突
- **缓解措施**：固定依赖版本，使用虚拟环境隔离

#### 工具配置

- **风险**：开发工具配置复杂
- **缓解措施**：提供自动化脚本和详细文档

### 5.2 缓解措施

- 提供详细的环境要求文档
- 使用自动化脚本简化搭建过程
- 固定依赖版本确保稳定性
- 提供多种环境搭建方案

## 6. 核心要点

### 环境设计原则

- **最小化原则**：只安装必要的工具和依赖
- **版本锁定**：固定依赖版本，确保稳定性
- **自动化优先**：脚本化环境搭建过程
- **文档驱动**：详细的环境配置文档

### 技术约束

- **Python 版本**：3.12+
- **虚拟环境**：venv（Python 内置）
- **包管理**：pip
- **IDE**：VSCode

### 开发策略

- **脚本化搭建**：自动化环境搭建过程
- **版本控制**：固定依赖版本
- **文档驱动**：详细的环境配置文档
- **测试验证**：环境搭建后立即验证

> **一句话总结**：通过标准化的环境配置和自动化脚本，确保开发环境的一致性和可重现性。
