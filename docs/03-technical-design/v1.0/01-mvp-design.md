# DocumentConverter v1.0 MVP 设计文档

## 1. 文档目标

本文档定义 DocumentConverter 项目 v1.0 MVP 版本的整体设计，作为 v1.0 系列文档的入口和总览。

> **适用范围**：Python 项目开发，MVP 快速迭代场景。

---

**文档版本**：v1.0  
**最后更新**：2025-07-30  
**更新内容**：精简内容，专注 MVP 整体设计，删除重复内容

## 2. 设计概述

### 2.1 设计目标

基于 PRD 需求，设计一个简洁高效的文档转换系统，实现：

- **快速迭代**：MVP 优先，快速验证核心功能
- **函数式设计**：核心逻辑采用函数式编程范式
- **TDD 驱动**：测试先行，保证代码质量
- **渐进式演进**：从简单到复杂，避免过度设计

### 2.2 设计原则

- **YAGNI**：You Aren't Gonna Need It，不过度设计
- **KISS**：Keep It Simple, Stupid，保持简单
- **函数式优先**：纯函数，无副作用
- **测试驱动**：测试先行，快速反馈

### 2.3 技术选型

#### 核心技术栈

- **PDF 处理**：pdfplumber + pypdf
- **Word 处理**：python-docx
- **Markdown 处理**：markdown + markdownify
- **CLI 框架**：click + rich
- **开发工具**：pytest + black + flake8

> 详细技术选型请参考：02-environment-setup-v1.md

## 3. 详细设计

### 3.1 架构设计

#### MVP 阶段：3层架构

```text
┌─────────────────┐
│   CLI Layer     │  # 命令行接口层
│                 │
│  - Command      │  # 命令处理
│  - Interface    │  # 用户交互
│  - Validation   │  # 输入验证
├─────────────────┤
│   Core Layer    │  # 核心业务层（函数式）
│                 │
│  - Parser       │  # 文档解析（纯函数）
│  - Converter    │  # 格式转换（纯函数）
│  - Generator    │  # 文档生成（纯函数）
├─────────────────┤
│  Utility Layer  │  # 工具层
│                 │
│  - Logger       │  # 日志记录
│  - Error Handler│  # 错误处理
│  - File I/O     │  # 文件操作
└─────────────────┘
```

### 3.2 接口设计

#### 命令行接口

```python
# 主要命令
documentconverter convert <input_file> <output_file> [options]
documentconverter batch <input_dir> <output_dir> [options]

# 选项参数
--format, -f: 指定格式（pdf2md, word2md, md2word）
--verbose, -v: 详细输出
--quiet, -q: 静默模式
```

> 详细 CLI 设计请参考：03-cli-v1.md

### 3.3 数据流设计

#### 核心数据模型

```python
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class DocumentData:
    """简化的文档数据模型"""
    title: str
    content: str
    metadata: Dict[str, Any]
```

#### 数据流设计

```text
文件读取 → 解析 → 转换 → 生成
    ↓        ↓      ↓      ↓
  File I/O → Parser → Converter → Generator
```

## 4. 实现计划

### 4.1 开发阶段

#### 第一周：核心功能（MVP）

- [ ] 项目环境搭建
- [ ] PDF → Markdown 基础转换
- [ ] Word → Markdown 基础转换
- [ ] 命令行界面

#### 第二周：功能完善

- [ ] Markdown → Word 转换
- [ ] 错误处理机制
- [ ] 基础测试覆盖

#### 第三周：优化和文档

- [ ] 功能稳定和 bug 修复
- [ ] 文档完善
- [ ] 用户测试和反馈收集

### 4.2 测试策略

#### TDD 驱动开发

##### 第一步：写测试

```python
# test_converter.py
import pytest
from documentconverter.core import convert_pdf_to_markdown

def test_convert_pdf_to_markdown_basic():
    """测试PDF转Markdown基础功能"""
    # 准备测试数据
    input_file = "tests/data/sample.pdf"
    output_file = "tests/output/sample.md"
    
    # 执行转换
    convert_pdf_to_markdown(input_file, output_file)
    
    # 验证结果
    assert os.path.exists(output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert "# Sample Title" in content
        assert "Sample content" in content
```

##### 第二步：写代码

```python
# core.py
def parse_pdf(file_path: str) -> DocumentData:
    """解析PDF文件"""
    import pdfplumber
    
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        content = ""
        title = ""
        
        for page in pages:
            text = page.extract_text()
            if text:
                content += text + "\n"
        
        # 简单提取标题（第一行）
        lines = content.split('\n')
        title = lines[0] if lines else "Untitled"
        
        return DocumentData(
            title=title,
            content=content,
            metadata={"pages": len(pages)}
        )
```

##### 第三步：重构

```python
# 优化后的代码
def parse_pdf(file_path: str) -> DocumentData:
    """解析PDF文件（重构后）"""
    import pdfplumber
    
    with pdfplumber.open(file_path) as pdf:
        content = _extract_text_from_pages(pdf.pages)
        title = _extract_title_from_content(content)
        
        return DocumentData(
            title=title,
            content=content,
            metadata={"pages": len(pdf.pages)}
        )

def _extract_text_from_pages(pages) -> str:
    """提取页面文本"""
    return "\n".join(page.extract_text() or "" for page in pages)

def _extract_title_from_content(content: str) -> str:
    """从内容中提取标题"""
    lines = content.split('\n')
    return lines[0] if lines else "Untitled"
```

### 4.3 部署计划

#### 项目目录结构

```ini
DocumentConverter/
├── src/
│   ├── __init__.py
│   ├── main.py              # 主入口
│   ├── cli/                 # 命令行接口
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── core/                # 核心功能（函数式）
│   │   ├── __init__.py
│   │   ├── parser.py        # 解析函数
│   │   ├── converter.py     # 转换函数
│   │   ├── generator.py     # 生成函数
│   │   └── models.py        # 数据模型
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── logger.py
│       └── file_utils.py
├── tests/                   # 测试目录
│   ├── __init__.py
│   ├── data/                # 测试数据
│   ├── test_parser.py
│   ├── test_converter.py
│   └── test_generator.py
├── docs/                    # 文档目录
├── requirements.txt         # 依赖文件
├── setup.py                 # 安装配置
└── README.md                # 项目说明
```

## 5. 风险评估

### 5.1 技术风险

#### PDF 解析复杂性

- **风险**：PDF 格式复杂，解析可能不完整
- **缓解措施**：使用成熟的 PDF 解析库，充分测试不同格式

#### 格式兼容性

- **风险**：不同 Word 版本格式差异
- **缓解措施**：充分测试不同格式的兼容性

#### 性能瓶颈

- **风险**：大文件处理可能影响性能
- **缓解措施**：实现分块处理和内存优化

### 5.2 缓解措施

- 使用成熟的 PDF 解析库
- 充分测试不同格式的兼容性
- 实现分块处理和内存优化
- 建立完善的测试覆盖

## 6. 核心要点

### MVP 开发边界

- **功能边界**：严格控制在核心转换功能
- **性能边界**：基础性能，无高级优化
- **架构边界**：3 层架构，避免过度设计
- **依赖边界**：最小依赖集，避免技术债务

### 技术约束

- **1.0 约束**：同步处理，无缓存，无监控，最小依赖
- **架构演进**：3 层 → 4 层 → 5 层，避免过度设计
- **性能边界**：基础性能 → 功能完善 → 性能优化

### 开发原则

- **功能边界**：严格控制在版本定义的功能范围内
- **TDD 驱动**：测试先行，保证代码质量
- **渐进式演进**：从简单到复杂的平滑过渡
- **向后兼容**：新版本保持 API 兼容性

> **一句话总结**：通过明确的版本边界和渐进式架构演进，实现可控的文档转换工具开发。
