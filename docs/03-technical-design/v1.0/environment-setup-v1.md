# DocumentConverter 环境设置 v1.0 设计文档

## 1. 文档目标

本文档定义 DocumentConverter 项目 v1.0 MVP 版本的环境设置方案，确保开发环境的一致性和可重现性。

> **适用范围**：Python 项目开发，开发环境搭建，MVP 快速迭代场景。

---

**文档版本**：v1.0  
**最后更新**：2025-07-29  
**更新内容**：创建环境设置设计文档，定义开发环境配置方案

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

#### Python 环境

- **Python 版本**：3.12+
- **虚拟环境**：venv（Python 内置）
- **包管理**：pip

#### 开发工具

- **IDE**：VSCode
- **代码格式化**：black
- **代码检查**：flake8
- **类型检查**：mypy（可选）

#### 版本控制

- **Git**：版本控制
- **GitHub**：远程仓库
- **分支策略**：main + develop + feature

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

# 开发工具
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
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

- [ ] 检查 Python 版本（3.12+）
- [ ] 检查 Git 版本
- [ ] 检查 VSCode 安装

#### 第二步：项目结构创建

- [ ] 创建项目目录结构
- [ ] 创建虚拟环境
- [ ] 安装基础依赖

#### 第三步：开发工具配置

- [ ] 配置 VSCode 设置
- [ ] 安装 VSCode 插件
- [ ] 配置代码格式化

#### 第四步：测试环境验证

- [ ] 运行基础测试
- [ ] 验证环境功能
- [ ] 检查代码质量工具

### 4.2 自动化脚本设计

#### 环境搭建脚本

```bash
#!/bin/bash
# scripts/setup_env.sh

echo "🚀 开始搭建 DocumentConverter 开发环境..."

# 1. 检查 Python 版本
echo "📋 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | grep -o '3\.[0-9]\+')
if [[ "$python_version" < "3.12" ]]; then
    echo "❌ Python 版本过低，需要 3.12+"
    exit 1
fi
echo "✅ Python 版本检查通过: $(python3 --version)"

# 2. 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 3. 升级 pip
echo "⬆️ 升级 pip..."
pip install --upgrade pip

# 4. 安装依赖
echo "📚 安装项目依赖..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. 创建项目目录结构
echo "📁 创建项目目录结构..."
mkdir -p src/{cli,core,utils}
mkdir -p tests/data
mkdir -p scripts
mkdir -p .vscode

# 6. 创建基础文件
echo "📄 创建基础文件..."
touch src/__init__.py
touch src/cli/__init__.py
touch src/core/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

# 7. 配置 VSCode
echo "⚙️ 配置 VSCode..."
cat > .vscode/settings.json << EOF
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
EOF

cat > .vscode/extensions.json << EOF
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.mypy-type-checker"
    ]
}
EOF

echo "✅ 环境搭建完成！"
echo "📝 使用说明："
echo "   1. 激活虚拟环境: source venv/bin/activate"
echo "   2. 运行测试: python -m pytest"
echo "   3. 格式化代码: black src/"
echo "   4. 检查代码: flake8 src/"
```

#### 测试运行脚本

```bash
#!/bin/bash
# scripts/run_tests.sh

echo "🧪 运行测试套件..."

# 激活虚拟环境
source venv/bin/activate

# 运行测试
echo "📋 运行单元测试..."
python -m pytest tests/ -v

# 运行代码质量检查
echo "🔍 运行代码质量检查..."
black --check src/
flake8 src/

echo "✅ 测试完成！"
```

### 4.3 配置文件设计

#### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "documentconverter"
version = "1.0.0"
description = "A document conversion tool"
authors = [{name = "DocumentConverter Team"}]
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "click>=8.0.0",
    "rich>=10.0.0",
    "pdfplumber>=0.7.0",
    "python-docx>=0.8.11",
    "markdown>=3.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

[project.scripts]
documentconverter = "src.main:main"

[tool.black]
line-length = 88
target-version = ['py312']

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

#### setup.py

```python
from setuptools import setup, find_packages

setup(
    name="documentconverter",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "pdfplumber>=0.7.0",
        "python-docx>=0.8.11",
        "markdown>=3.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "documentconverter=main:main",
        ],
    },
    python_requires=">=3.12",
    author="DocumentConverter Team",
    description="A document conversion tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)
```

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
